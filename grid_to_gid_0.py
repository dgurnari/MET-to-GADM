import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pickle

from sys import argv

import psycopg2

import netCDF4




def create_grid_to_gid_dict(adm_0, grid, start_idx):
    # THIS IS QUITE SLOW
    adm_to_grid = {}

    print("there are {} points to check".format(len(grid)))

    # enumerate starts from 0
    # I want to keep the original idx
    for p_idx, point in enumerate(grid.geometry):
        for c_idx, country in adm_0.iterrows():
            if country.geometry.contains(point):
                adm_to_grid.setdefault(country.gid, []).append([p_idx+start_idx, point])
                # we assume each point is in only one GID
                break

    return adm_to_grid



if __name__ == "__main__":
    if len(argv) < 2:
        raise ValueError('please specify the start ')

    START = int(argv[1])
    STOP = START+125000

    print("intervals: ", START, STOP)

    # load the grid data
    met_data = netCDF4.Dataset("input/met_file.nc")

    lat = pd.Series(met_data.variables['latitude'][:].data)

    # lon are in [0, 360], we want it in [-180, +180]
    lon = pd.Series([l-360*(l>180) for l in met_data.variables['longitude'][:].data])

    index = pd.MultiIndex.from_product([lat, lon], names = ["lat", "lon"])
    grid = pd.DataFrame(index = index).reset_index()

    print(grid.shape)

    grid = grid[START:STOP]

    # convert it to a GeoPandas DataFrame
    grid = gpd.GeoDataFrame(
    grid, geometry=gpd.points_from_xy(grid.lon, grid.lat))



    # load the gid data
    with open('input/adm_0.pkl', 'rb') as f:
        adm_0 = pickle.load(f)

    print(adm_0.shape)

    adm_0_to_grid = create_grid_to_gid_dict(adm_0, grid, START)

    # dump dict to pickle file
    with open('out/level_0/adm_0_to_grid_{}.pkl'.format(START), 'wb') as handle:
        pickle.dump(adm_0_to_grid, handle)
