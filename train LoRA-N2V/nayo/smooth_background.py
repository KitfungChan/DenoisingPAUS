#!/usr/bin/env python

import os
import subprocess
import tempfile
from pathlib import Path
from astropy.stats import sigma_clip

import numpy as np
from astropy.io import fits

def _smooth_background(image_array, mesh_size=32, filter_size=5):
    """Smooth the image using sextractor."""
    
    # To avoid dealing with resources.
    nightly_conf = Path('/home/eriksen/source/dm/paudm.pipeline.nightly/paudm/pipeline/nightly/config')
    def resource_filename(pipeline, fname):
        return str(nightly_conf / fname)
    
    _, tmp_path_in = tempfile.mkstemp()
    _, tmp_path_out = tempfile.mkstemp()
    fits.writeto(tmp_path_in, image_array)
    
    sex_call = 'sextractor'
    cmd_call = (sex_call +" " + tmp_path_in + " -c " + resource_filename('paudm.pipeline.nightly.config','se4smooth.conf') +
                                        " -PARAMETERS_NAME " + resource_filename('paudm.pipeline.nightly.config','se_outs.basic.list') +
                                        " -FILTER_NAME " + resource_filename('paudm.pipeline.nightly.config','se_gauss_2.0_5x5.conv') +
                                        " -STARNNW_NAME " + resource_filename('paudm.pipeline.nightly.config','se_default.nnw') +
                                        " -CHECKIMAGE_NAME " + tmp_path_out +
                                        " -BACK_SIZE %f" % mesh_size +
                                        " -BACK_FILTERSIZE %f" % filter_size)
    
    subprocess.call(cmd_call, shell=True)
    smoothed = fits.getdata(tmp_path_out)

    os.remove(tmp_path_in)
    os.remove(tmp_path_out)
    
    return smoothed
    
    
    
def subtract_science(image_array, method='16-3-clip'):
    """Substract background from science image."""
    
    if method == '32-5':
        sci_ccd_smooth = _smooth_background(image_array, 32, 5)
        
    elif method == '16-3-clip':
        sl_border_limit = 200
        clipped_image_out = sigma_clip(image_array, sigma=4, iters=2)
        clipped_image_in = sigma_clip(image_array, sigma=2, iters=2)
        clipped_image_corrected = clipped_image_out.filled(fill_value=np.median(clipped_image_out))
    
        clipped_image_corrected[sl_border_limit:4096 - sl_border_limit, sl_border_limit:2048 - sl_border_limit] = clipped_image_in[sl_border_limit:4096 - sl_border_limit, sl_border_limit:2048 - sl_border_limit].filled(fill_value=np.median(clipped_image_out))
        sci_ccd_smooth = _smooth_background(clipped_image_corrected, 16, 3)
        
    else:
        raise NotImplemented(f'Not implemented: {method}')
      
    image_array = image_array - (sci_ccd_smooth - np.median(sci_ccd_smooth))

    return image_array
