import geopandas as gpd
from shapely.geometry import mapping


def make_geom(aoi_filename):
    # read in AOI as a GeoDataFrame
    aoi = gpd.read_file(aoi_filename)

    # get the geometry of the AOI as a dictionary for use with PySTAC Client
    geom = mapping(aoi.to_dict()['geometry'][0])
    return geom
