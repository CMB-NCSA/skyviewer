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

    # We want this file: galactic_plane_fullrate_coadd1.g3
    g3file = sys.argv[1]
    g3 = core.G3File(g3file)

    for frame in g3:
        logger.info(f"Reading frame: {frame}")
        if frame.type == core.G3FrameType.Map:
            logger.info(f"Transforming to FITS: {frame.type} -- Id: {frame['Id']}")
            maps.RemoveWeights(frame, zero_nans=True)
            maps.MakeMapsUnpolarized(frame)
            remove_units(frame, units=core.G3Units.mK)
            weight = frame.get('Wpol', frame.get('Wunpol', None))
            band = frame['Id']
            fitsfile = f"galactic_plane_fullrate_{band}.fits"
            maps.fitsio.save_skymap_fits(fitsfile, frame['T'],
                                         overwrite=True,
                                         compress=None,
                                         W=weight)
            logger.info(f"Wrote file:{fitsfile}")
