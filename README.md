# snowPALM-py
Python implementation of snowPALM

## EarthAccess
Edit EarthAccess credentials in `config.ini`. This file is part of `.gitignore` so changes made will not be committed
```
[earthaccess]
username=REPLACE_WITH_USERNAME
password=REPLACE_WITH_PASSWORD
```
This file will be created by default from the `config.example.ini` file, but not tracked in this repo

## Data
- `data/US_DEM.tf`: Digital Elevation Model (DEM) raster file for the United States as a TIFF file (copied from snowPALM)
