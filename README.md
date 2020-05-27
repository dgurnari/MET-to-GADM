# MET-to-GADM
The code in this repository allows to create a mapping between the MET 12x12 grid points and the GADM regions. We create this mapping in a iterative way, by first assign each point of the grid to a Country (GADM level 0) and then refine it by considering GADM level 1 and level 2. 

At the end of the process we will have a nested dictionary where the keys are the GID (GADM identifiers) at various levels
{ ...
  GID_0 : { ...,
            GID_0_1 : { ...,
                        GID_0_1_2 : [list of grid points],
                        ...
                       }
          }
}

Once we have this dictionary we can aggregate MET weather data up to GADM level 2.
# PIPELINE


download the Jan-April pickle file from this folder
https://drive.google.com/open?id=1czvUXI3pmhLlIcqBUtEsMaOzOW1r4l5o

and use the upload_weather_data.ipynb notebook to upload it to the play DB
