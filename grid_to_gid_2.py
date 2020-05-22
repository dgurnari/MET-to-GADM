import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pickle

from sys import argv


def create_grid_to_gid_2_dict(adm_1_to_grid, adm_2, country):
    adm_2_to_grid = {}
    subdict = {}

    for area_1 in adm_1_to_grid[country].keys():
        sub2dict = {}

        for point in adm_1_to_grid[country][area_1]:
            for a_idx, area_2 in adm_2[adm_2.adm_area_1_code == area_1].iterrows():
                if area_2.geometry.contains(point[1]):
                    sub2dict.setdefault(area_2.gid, []).append(point)
                    # we assume each point is in only one GID
                    break
        subdict[area_1] = sub2dict

    adm_2_to_grid[country] = subdict

    return adm_2_to_grid



if __name__ == "__main__":
    if len(argv) < 2:
        raise ValueError('please specify the country ')


    # load the level 1 dict
    with open('input/dicts/adm_1_to_grid.pkl', 'rb') as f:
        adm_1_to_grid = pickle.load(f)

    # load the gid level 2 data
    with open('input/adm_2.pkl', 'rb') as f:
        adm_2 = pickle.load(f)

    COUNTRY = argv[1]

    print(COUNTRY, len(adm_1_to_grid[COUNTRY]))



    adm_2_to_grid = create_grid_to_gid_2_dict(adm_1_to_grid, adm_2, COUNTRY)

    # dump dict to pickle file
    with open('out/level_2/adm_2_to_grid_{}.pkl'.format(COUNTRY), 'wb') as handle:
        pickle.dump(adm_2_to_grid, handle)
