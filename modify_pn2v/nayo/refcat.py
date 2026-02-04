#!/usr/bin/env python
# encoding: UTF8

# Reference catalogs for PAUS forced photometry. Add the
# catalogs which are actually in use.

import numpy as np
import pandas as pd

def COSMOS(conn, cosmos_pixel_scale = 0.03):
    """Reference catalogue in the COSMOS field."""
    
    query = """SELECT paudm_id as ref_id, ra, dec, type, r50, acs_a_image, acs_b_image, acs_theta_image,
               "I_auto", sersic_n_gim2d, "mod_gal"
               FROM paudm.COSMOS
               WHERE "I_auto" < 23
            """
    
    PIXEL_SCALE = 0.263
    refcat = pd.read_sql_query(query, conn)
    refcat = refcat.set_index('ref_id')
    
    source_type = np.where(refcat.type == 1, 'star', 'galaxy')
  
    # PAUdm still directly used the old r50 estimate.
    #r50_best_estimate = 1.2*np.sqrt(refcat.acs_a_image**2 + refcat.acs_b_image**2)
    r50_best_estimate = np.where(0 < refcat.r50, refcat.r50, 10 ** (2.75 - (0.06 * refcat.I_auto)))
    r50_best_estimate = np.where(source_type == 'galaxy', r50_best_estimate, 0.)
    
    # MEMBA 821 only approximated the sersic index.
    sersic_approx = np.where(refcat.mod_gal < 9, 4, 1)
    if False:
        sersic = np.where(refcat.sersic_n_gim2d > 0, refcat.sersic_n_gim2d, sersic_approx)
        sersic = pd.Series(sersic, index=refcat.index)
    else:
        sersic = sersic_approx
        
    scale_ratio = cosmos_pixel_scale / PIXEL_SCALE
    df_out = refcat[['ra', 'dec', 'I_auto']].copy()
    df_out['rE'] = r50_best_estimate * scale_ratio
    df_out['a'] = refcat.acs_a_image * scale_ratio
    df_out['b'] = refcat.acs_b_image * scale_ratio

    df_out['theta'] = refcat.acs_theta_image
    df_out['type'] = source_type
    df_out['sersic_index'] = sersic
    
    return df_out
