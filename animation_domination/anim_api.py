#!/usr/bin/env python
# coding: utf-8

import sys

sys.path.append('./lib')

from anim import *




aoi_filename = "./siouxfalls2.geojson"

make_netcdf(aoi_filename)


#! conda install -y pystac-client

#! wget https://raw.githubusercontent.com/tonybutzer/data-curation/79323ea534ccce76bd8026454a013fb436395c6a/little-cloud/lib/notebookLib/notebookLib/nb_animate.py

#! mv nb_animate.py ./lib

#! jupyter nbextension enable --py jupyter-resource-usage --sys-prefix

#!conda install -y -c conda-forge jupyter-resource-usage





