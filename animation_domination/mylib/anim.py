import geopandas as gpd
from shapely.geometry import mapping
from pystac_client import Client
from pystac import ItemCollection



def make_geom(aoi_filename):
    # read in AOI as a GeoDataFrame
    aoi = gpd.read_file(aoi_filename)

    # get the geometry of the AOI as a dictionary for use with PySTAC Client
    geom = mapping(aoi.to_dict()['geometry'][0])
    return geom


def get_stac_records(geom):
    # STAC API - Landsat Collection 2
    url = "https://earth-search.aws.element84.com/v0"

    # Search parameters
    params = {
        "collections": ["sentinel-s2-l2a-cogs"],
        "intersects": geom,
        "datetime": "2020-05-01/2021-12-31",
        "limit": 100,
        "query": ["eo:cloud_cover<5"]
    }
    
    cat = Client.open(url)
    search = cat.search(**params)
    
    matched = search.matched()
    print(f"{search.matched()} scenes found")


# get all items found in search
    items_dict = []
    for item in search.get_all_items_as_dict()['features']:
        for a in item['assets']:
            if 'alternate' in item['assets'][a] and 's3' in item['assets'][a]['alternate']:
                item['assets'][a]['href'] = item['assets'][a]['alternate']['s3']['href']
            # item['assets'][a]['href'] = item['assets'][a]['href'].replace('usgs-landsat-ard', 'usgs-landsat')
        items_dict.append(item)

    # Create GeoDataFrame from resulting Items
    #items_gdf = items_to_geodataframe(items_dict)
    item_collection = ItemCollection(items_dict)

    items_dict_pruned = []
    cnt=0
    for my_item in items_dict:
        #print(cnt)
        #cnt=cnt+1
        if int(my_item['properties']['sentinel:data_coverage']) > 88:
            # print(my_item['assets']['B03']['proj:shape'][0])
            print(my_item['properties']['sentinel:data_coverage'])
            items_dict_pruned.append(my_item)

    return(items_dict_pruned)


import yaml

from odc import stac
from pyproj import CRS
from pystac.extensions.projection import ProjectionExtension

def open_odc(items, crs=None, resolution=None):
    configuration_str = """---
        landsat-c2l2-sr:
          measurements:
            '*':
              dtype: float32
              nodata: 0
              units: 'm'
        """
    configuration = yaml.load(configuration_str, Loader=yaml.CSafeLoader)
    datasets = list(stac.stac2ds(items, configuration))
    
    # print(type(items[0]))
    # print(dir(items[0].properties))
    crs_str = str(items[0].properties['proj:epsg'])
    crs = f'EPSG:{crs_str}'
#     proj = ProjectionExtension.ext(items[0])
#     if crs is None:
#         crs = CRS.from_epsg(proj.epsg)
#     if resolution is None:
#         resolution = (proj.transform[4], proj.transform[0])


    resolution=(-10, 10)
    data = stac.dc_load(datasets, bands=['B04', 'B03', 'B02', 'B09'], chunks={"x": 1024, "y": 1024}, output_crs=crs, resolution=resolution)
    #data = stac.dc_load(datasets, output_crs=crs, resolution=resolution)
    return data


import rioxarray

def dc(geom, items_dict_pruned):
    pruned_item_collection = ItemCollection(items_dict_pruned)
    _datacube = open_odc(pruned_item_collection)
    datacube = _datacube.rio.clip([geom], crs='epsg:4326')
    return(datacube)


def nc_from_ds(DS, filename):
    DS.time.attrs = {}  #this allowed the nc to be written
    #DS.SCL.attrs = {}
    ds1 = DS.drop(labels='spatial_ref')
    ds1.to_netcdf(filename)




import sys

sys.path.append('.')

import rioxarray
from nb_animate import nb_animated_timeseries


def make_animated_gif(nc_file, gif_file):

    rds = rioxarray.open_rasterio(nc_file)

    nb_animated_timeseries(rds,output_path=gif_file, bands = ['B04', 'B03', 'B02'], time_dim='time',  
      percentile_stretch=(.2,.85), interval=1200)



def make_netcdf(aoi_filename_geojson, nc_filename):
    geom = make_geom(aoi_filename_geojson)
    items = get_stac_records(geom)
    ds = dc(geom,items)
    nc_from_ds(ds, nc_filename)
