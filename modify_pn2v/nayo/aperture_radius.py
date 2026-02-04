#!/usr/bin/env python
# encoding: UTF8

from pathlib import Path
import json
import numpy as np
import pandas as pd

from scipy.interpolate import interp2d

def load_spline(path=None):
    """Load cached values for the optimal aperture."""

    basepath = Path('/home/eriksen/code/nayo/config')
    cached = json.load(open(basepath / 'aperture_estimator_62.5pc.json'))
    optim_aperture = interp2d(cached['fwhms'], cached['ns'], cached['apers'])

    return optim_aperture

def apertures(sources, path=None):
    """Determine the parameters for an elliptical aperture."""
    
    PIXEL_SCALE = 0.263
    optim_aperture = load_spline(path)

    # For the stars.
    aperture_star = 0.72*sources.psf_fwhm / PIXEL_SCALE

    # Major axis. 
    fwhm_r50 = sources.psf_fwhm / PIXEL_SCALE / sources.rE
    major_gal = [optim_aperture(*X) for X in zip(fwhm_r50, sources.sersic_index)]
    major_gal = np.hstack(major_gal) * sources.rE

    aperture_a = np.where(sources.type == 'galaxy', major_gal, aperture_star)
    aperture_a = pd.Series(aperture_a, index=sources.index)
    
    # Different scaling for stars and galaxies. 
    ell = 1 - sources.b / sources.a
    a50 = sources.rE
    b50 = a50 * (1 - ell)
    fwhm_r50 = sources.psf_fwhm / PIXEL_SCALE / b50
     
    minor_gal = [optim_aperture(*X) for X in zip(fwhm_r50, sources.sersic_index)]
    minor_gal = np.hstack(minor_gal) * b50
    
    #minor_gal = sources.aper_r50 * b50
    
    aperture_b = np.where(sources.type == 'galaxy', minor_gal, aperture_star)
    aperture_b = pd.Series(aperture_b, index=sources.index)
    
    # These are in pixels, while PAUdm store the values in arc.sec.
    aper = pd.DataFrame({'aperture_a': aperture_a, 'aperture_b': aperture_b})
    
    return aper
