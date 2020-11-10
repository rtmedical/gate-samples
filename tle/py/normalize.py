#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import SimpleITK as sitk

# -----------------------------------------------------------------------------
# Check command line arguments
if (len(sys.argv) <= 2):
    print("Please provide 2 arguments: <image.mhd> <output.mhd>")
    exit()
    # end if

# -----------------------------------------------------------------------------
# Get the filenames
input_filename = sys.argv[1]
output_filename = sys.argv[2]

# Read the input image
image = sitk.ReadImage(input_filename)
print('Reading image : ', input_filename)
print('Image size    : ', image.GetSize())
print('Image spacing : ', image.GetSpacing())
print('Image origin  : ', image.GetOrigin())

# Rescale the pixel values between 0 and 100
f = sitk.RescaleIntensityImageFilter()
f.SetOutputMaximum(100)
f.SetOutputMinimum(0)
image2 = f.Execute(image)

# Output the results
print('Output image   : ', output_filename)
sitk.WriteImage(image2, output_filename)
