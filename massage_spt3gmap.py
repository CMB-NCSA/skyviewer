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
    SCI = 1
    WGT = 2

    # Create the mask for weights == 0
    idx = numpy.where(hdul[WGT].data == 0)
    hdul[SCI].data[idx] = -99
    hdu = fits.PrimaryHDU(data=hdul[SCI].data, header=hdul[SCI].header)
    hdu.writeto(outname, overwrite=True)
    print(f"# Done with: {filename}")
