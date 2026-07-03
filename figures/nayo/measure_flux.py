#!/usr/bin/env python
# encoding: UTF8

import time
import numpy as np
import pandas as pd

from IPython.core import debugger as ipdb
from astropy.stats import sigma_clip
from photutils.aperture import aperture_photometry
from photutils.aperture import CircularAnnulus, EllipticalAperture

#import bkgnet
from . import smooth_background

def background_annulus(data, mask, gal, r_in=30, r_out=45):
    """Measure background in an annulus."""
    
    # Mask data
    masked_data = np.ma.array(data=data, mask=mask != 0)
    masked_data = masked_data.filled(fill_value=0)

    # Create annulus mask
    center = (gal.aperture_x, gal.aperture_y)
    annulus_apertures = CircularAnnulus(center, r_in=r_in, r_out=r_out)
    masks = annulus_apertures.to_mask(method='center')

    # Changed from apply to cutout, after upgrading photoutils
    cutout_data = masks.cutout(masked_data)

    # Clip sources
    clip_annulus_array = sigma_clip(cutout_data[cutout_data != 0], sigma=3, maxiters=2)

    # Apply statistics to masked data
    S = pd.Series()
    S['annulus_mean'] = np.ma.mean(clip_annulus_array)
    S['annulus_median'] = np.ma.median(clip_annulus_array)
    S['annulus_std'] = np.ma.std(clip_annulus_array)
    S['annulus_samples'] = np.ma.count(clip_annulus_array)

    return S


def flux_elliptical(image, mask, gal):
    """Measure the flux withing an elliptical aperture."""
    
    PIXEL_SCALE = 0.263
    theta = -gal.aperture_theta * np.pi / 180.
    a = gal.aperture_a / PIXEL_SCALE
    b = gal.aperture_b / PIXEL_SCALE

    center = (gal.aperture_x, gal.aperture_y)
    source_aperture = EllipticalAperture(center, a, b, theta)

    xmask = mask != 0
    raw_flux = aperture_photometry(image, source_aperture, mask=xmask)
   
    S = pd.Series()
    S['raw_flux'] = float(raw_flux['aperture_sum'])
    S['area'] = source_aperture.area
    
    return S
    
def bkgnet_background(image, sources, net, interv, band):
    """Background estimationg with BKGnet."""
    
    # Here it would be better to use the PAUdm names within BKGnet.
    #net = bkgnet.BKGnet(model_path)
    sources = sources.rename(columns={'aperture_x': 'y', 'aperture_y': 'x'})
   
    # Notice the implicit rounding!
    coords_pix = sources[['x', 'y']].astype(np.int)
    X = net.background_img(image, coords_pix, sources.r50, sources.I_auto, band, interv)
    
    return X

def photometry(image, mask, sources, net, interv, band=None, smooth_method=False, \
               measure_flux=True): 
    """Measure the flux and background for all sources in the image."""
  
    # For being able to compare with MEMBA
    if smooth_method:
        image = smooth_background.subtract_science(image, smooth_method)
        
    # Background estimation with BKGnet. 
    assert not interv is None
    assert not band is None

# Only forced photometry for the time being.
#    bkgnn = bkgnet_background(image, sources, net, interv, band)    
    if measure_flux:
        L = []
        for i,(key, gal) in enumerate(sources.iterrows()):
            S1 = background_annulus(image, mask, gal)
            S2 = flux_elliptical(image, mask, gal)

            S = pd.concat([S1,S2])
            L.append(S)

        df = pd.concat(L, axis=1).T
        df.index = sources.index
        #df = df.join(bkgnn) 
    else:
        df = bkgnn

    return df
