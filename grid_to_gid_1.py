import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pickle

from sys import argv


def create_grid_to_gid_1_dict(adm_0_to_grid, adm_1, country):
    adm_1_to_grid = {}

    subdict = {}

    for point in adm_0_to_grid[country] :
        for a_idx, area_1 in adm_1[adm_1.countrycode == country].iterrows():
            if area_1.geometry.contains(point[1]):
                subdict.setdefault(area_1.gid, []).append(point)
                # we assume each point is in only one GID
                break

    adm_1_to_grid[country] = subdict

    return adm_1_to_grid



if __name__ == "__main__":
    if len(argv) < 2:
        raise ValueError('please specify the start ')


    # load the level 0 dict
    with open('input/dicts/adm_0_to_grid.pkl', 'rb') as f:
        adm_0_to_grid = pickle.load(f)

    # load the gid level 1 data
    with open('input/adm_1.pkl', 'rb') as f:
        adm_1 = pickle.load(f)

    COUNTRY = argv[1]

    print(COUNTRY, len(adm_0_to_grid[COUNTRY]))



    adm_1_to_grid = create_grid_to_gid_1_dict(adm_0_to_grid, adm_1, COUNTRY)

    # dump dict to pickle file
    with open('out/level_1/adm_1_to_grid_{}.pkl'.format(COUNTRY), 'wb') as handle:
        pickle.dump(adm_1_to_grid, handle)
