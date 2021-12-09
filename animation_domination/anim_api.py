#!/usr/bin/env python
# coding: utf-8

import os
import sys
import shutil

sys.path.append('./mylib')

from anim import *

aoi_filename_geojson = "./siouxfalls2.geojson"

if sys.argv[1:]:
   aoi_filename_geojson = sys.argv[1]

nc_filename = aoi_filename_geojson.replace('.geojson', '.nc')
make_netcdf(aoi_filename_geojson, nc_filename)

gif_filename = nc_filename.replace('.nc','.gif')
make_animated_gif(nc_filename, gif_filename)


def rm_if(filename):
    if os.path.exists(filename):
        os.remove(filename)


ddir = './data'

full_nc = f'{ddir}/{nc_filename}'
full_gif = f'{ddir}/{gif_filename}'

rm_if(full_nc)
rm_if(full_gif)

shutil.move(nc_filename, full_nc)
shutil.move(gif_filename, full_gif)








