#!/usr/bin/env python
# coding: utf-8

import sys

sys.path.append('./mylib')

from anim import *

aoi_filename_geojson = "./siouxfalls2.geojson"

nc_filename = aoi_filename_geojson.replace('.geojson', '.nc')
make_netcdf(aoi_filename_geojson, nc_filename)

gif_filename = nc_filename.replace('.nc','.gif')
make_animated_gif(nc_filename, gif_filename)






