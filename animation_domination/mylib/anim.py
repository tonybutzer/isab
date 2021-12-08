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
