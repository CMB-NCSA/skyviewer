#!/usr/bin/env python3

from astropy.io import fits
import sys
import os
import numpy

filenames = sys.argv[1:]
if len(filenames) == 0:
    sys.exit(f"Usage: {os.path.basename(sys.argv[0])} <fitsfile>")

for filename in filenames:

    print(f"# Will process file: {filename}")
    fits.info(filename)

    basename = os.path.splitext(os.path.basename(filename))[0]
    outname = f"{basename}_SCI.fits"
    print(f"# Will write to:{outname}")
    # Open and get the hdu list
    hdul = fits.open(filename)
    if len(hdul) > 2:
        SCI = 1
        WGT = 2
    else:
        SCI = 0
        WGT = 1
    # Create the mask for weights == 0
    # For lowell winter the weights are weird
    # idx = numpy.where(hdul[WGT].data <= 800000)

    # For summer fields we want the following cuts:
    # 90GHz 0.002
    # 150GHz 0.002
    # 220GHz 0.0001

    # For the winter fields
    # 90GHz = 1e-4
    # 150GHz = 1e-4
    # 220GHz = 1e-4

    weight_limit = 1e-4
    idx = numpy.where(hdul[WGT].data <= weight_limit)
    hdul[SCI].data[idx] = -99
    hdu = fits.PrimaryHDU(data=hdul[SCI].data, header=hdul[SCI].header)
    hdu.writeto(outname, overwrite=True)
    print(f"# Done with: {filename}")
