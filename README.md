# MET-to-GADM
The code in this repository allows to create a mapping between the MET 12x12 grid points and the GADM regions. We create this mapping in a iterative way, by first assign each point of the grid to a Country (GADM level 0) and then refine it by considering GADM level 1 and level 2. 

At the end of the process we will have a nested dictionary where the keys are the GID (GADM identifiers) at various levels

```
{ ...
  GID_0 : { ...,
            GID_0_1 : { ...,
                        GID_0_1_2 : [list of grid points],
                        ...
                       }
          }
}
```

Once we have this dictionary we can aggregate MET weather data up to GADM level 2.
# PIPELINE
Since checking all points in the grid can be very time consuming we provide a python code that can be run in a parallel fashion on a computer cluster. 

To create the dictionary use the `merge_grid_dicts.ipynb` notebook. For each GADM level i use the notebook to prepare the input files, run the script `run_parallel_area_i.sh` and go back to the notebook to merge the dictionaries. 

We provide all the intermediate files in the `out/` so there is no need to run parallel code again. 

Dictionaries for levels 0,1,2 can be found in the folder `input/dicts` .

To aggregate the MET weather data using a specifific dictionary use the notebook `aggregate_weather_data.ipynb`. 

The Jan-April data aggregated at level 2 can be dowloaded from
https://drive.google.com/open?id=1czvUXI3pmhLlIcqBUtEsMaOzOW1r4l5o 

The `upload_weather_data.ipynb` notebook can be used to upload it to the covid19 DB.
