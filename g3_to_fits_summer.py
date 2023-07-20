#!/usr/bin/env python3

from spt3g import core, maps
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)s.%(msecs)03d][%(levelname)s][%(name)s][%(funcName)s] %(message)s'
FORMAT_DATE = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(FORMAT, FORMAT_DATE)
handler.setFormatter(formatter)
logger.addHandler(handler)


def remove_units(frame, units):
    "Remove units for g3 frame"
    if frame.type != core.G3FrameType.Map:
        return frame
    t_scale = units if frame['T'].weighted else 1./units
    w_scale = units * units
    for k in ['T', 'Q', 'U']:
        if k in frame:
            frame[k] = frame.pop(k) * t_scale
    for k in ['Wunpol', 'Wpol']:
        if k in frame:
            frame[k] = frame.pop(k) * w_scale
    return frame


if __name__ == "__main__":

    # We want this file: 10oct2022_coadd_healpix_summer-all_sumdiff.g3
    g3file = sys.argv[1]
    g3 = core.G3File(g3file)

    # Summer field parameters
    res = 0.25  # arcmin
    weighted = False

    # Dictionaries for field params
    # Values taken from:
    # spt3g_software/std_processing/python/mapmakers/pole_summer_{field}_autoproc_config_2021.yaml
    alpha_center = {}
    delta_center = {}
    map_height = {}
    map_width = {}
    summer_fields = ['a', 'b', 'c']

    # Summer a field
    alpha_center['a'] = 75.0
    delta_center['a'] = -42.0
    map_height['a'] = 52
    map_width['a'] = 56

    # Summer b field
    alpha_center['b'] = 25
    delta_center['b'] = -36
    map_height['b'] = 23
    map_width['b'] = 51

    # Summer c field
    alpha_center['c'] = 187.5
    delta_center['c'] = -38.0
    map_height['c'] = 26
    map_width['c'] = 72

    # Create the projection for each summer summer field
    p = {}
    for field in summer_fields:
        p[field] = {'res': res*core.G3Units.arcmin,
                    'x_len': int((map_width[field]*core.G3Units.deg)/(res*core.G3Units.arcmin)),
                    'y_len': int((map_height[field]*core.G3Units.deg)/(res*core.G3Units.arcmin)),
                    'weighted': weighted,
                    'alpha_center': alpha_center[field]*core.G3Units.deg,
                    'delta_center': delta_center[field]*core.G3Units.deg,
                    'proj': maps.MapProjection.ProjZEA,
                    'pol_type': maps.MapPolType.T,
                    'pol_conv': maps.MapPolConv.IAU,
                    'coord_ref': maps.MapCoordReference.Equatorial}
        TT_field = 'TT'+field
        p[TT_field] = p[field]
        p[TT_field]['pol_type'] = maps.MapPolType.none

    for hp_frame in g3:
        logger.info(f"Reading frame: {hp_frame}")

        ID = hp_frame['Id']
        # We only want the sum (not diff)
        if ID not in ['sum_90GHz', 'sum_150GHz', 'sum_220GHz']:
            continue

        if hp_frame.type == core.G3FrameType.Map:

            maps.MakeMapsUnpolarized(hp_frame)
            maps.RemoveWeights(hp_frame, zero_nans=True)
            weight = hp_frame.get('Wpol', hp_frame.get('Wunpol', None))

            for field in summer_fields:

                fits_name = f"10oct2022_coadd_flat_summer_{field}_{ID}.fits"
                g3_name = f"10oct2022_coadd_flat_summer_{field}_{ID}.g3"

                logger.info(f"Transforming to Field:{field} FlatSky T -- Id: {hp_frame['Id']}")
                frameT = maps.healpix_to_flatsky(hp_frame['T'], **p[field])

                logger.info(f"Transforming to Field:{field} FlatSky weight.TT -- Id: {hp_frame['Id']}")
                weightTT = maps.healpix_to_flatsky(hp_frame['Wunpol'].TT, **p['TT'+field])

                frame = core.G3Frame(core.G3FrameType.Map)
                frame['T'] = frameT

                wgt_out = maps.G3SkyMapWeights(frame["T"], polarized=False)
                wgt_out.TT = weightTT
                frame["Wunpol"] = wgt_out

                # Write the g3 SkyFlat maps file
                # logger.info(f"Writing g3 file: {g3_name}")
                # core.G3Writer(filename=g3_name)(frame)

                # Write the FITS file
                logger.info(f"Writing FITS file: {fits_name}")
                maps.fitsio.save_skymap_fits(fits_name,
                                             frame['T'], W=frame['Wunpol'],
                                             compress=None, overwrite=True)
