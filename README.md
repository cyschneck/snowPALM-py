# snowPALM-py
Python implementation of snowPALM

## Data

### EarthAccess
Edit EarthAccess credentials in `config.ini`. This file is part of `.gitignore` so changes made will not be committed
```
[earthaccess]
username=REPLACE_WITH_USERNAME
password=REPLACE_WITH_PASSWORD
```
This file will be created by default from the `config.example.ini` file, but not tracked in this repo

[Register for free Earthdata login (EDL) account](https://urs.earthdata.nasa.gov/)

Returns hourly data
- Missing value: -9999.0

Data returned (Hourly):
1. Tair: 2-meter above ground temperature (units: K (Kelvin), standard_name: "Near surface air temperature", long_name: "2-meter above ground Temperature", vmin: precomuted minimum value, vmax: precommuted maximum value)
2. Qair: 2-meter above ground specific humidity (units: kg kg-1, standard_name: "Near surface specific humidity", long_name: "2-meter above ground Specific humidity", vmin: precomuted minimum value, vmax: precommuted maximum value)
3. PSurf: surface pressure (units: Pa, standard_name: "Surface pressure, long_name: "Surface pressure", vmin: precomuted minimum value, vmax: precommuted maximum value)
4. Wind_E: 10-meter aboveground zonal wind speed (units: m s-1, standard_name: "Near surface eastward wind component", long_name: "10-meter above ground Zonal wind speed", vmin: precomuted minimum value, vmax: precommuted maximum value)
5. Wind_N: 10-meter aboveground meridional wind speed (units: m s-1, standard_name: "Near surface northward wind component", long_name: "10-meter above ground Meridional wind speed", vmin: precomuted minimum value, vmax: precommuted maximum value)
6. LWdown: longwave radiationflux downwards (units: W m-2, standard_name: "Surface incident longwave radiation", long_name: "Longwave radiation flux downwards (surface)", vmin: precomuted minimum value, vmax: precommuted maximum value)
7. CRainf_frac: Convective precipitation (units: fraction, standard_name: "Convective precipitation fraction", long_name: "Fraction of total precipitation that is convective", vmin: precomuted minimum value, vmax: precommuted maximum value)
8. CAPE: Convective Available Potential Energy (units: J kg-1, standard_name: "Convective Available Potential Energy", long_name: "Convective Available Potential Energy", vmin: precomuted minimum value, vmax: precommuted maximum value)
9. PotEvap: Potential evaporation (units: kg m-2, standard_name: "Potential evaporation", long_name: "Potential evaporation", vmin: precomuted minimum value, vmax: precommuted maximum value)
10. Rainf: Total precipitation (units: kg m-2, standard_name: "Total precipitation", long_name: "Total precipitation", vmin: precomuted minimum value, vmax: precommuted maximum value)
11. SWdown: Shortwave radiation flux downwards (units: W m-2, standard_name: "Surface incident shortwave radiation", long_name: "Shortwave radiation flux downwards (surface)", vmin: precomuted minimum value, vmax: precommuted maximum value)
		

### PRISM
PRISM Gridded data is collected from the [PRISM web service site](https://prism.oregonstate.edu/downloads/) from Oregon State

### snowPALM Data
- `data/US_DEM.tf`: Digital Elevation Model (DEM) raster file for the United States as a TIFF file (copied from snowPALM)

Data downloaded from EarthAccess will be saved to the `testing_outputs`, but ignored in `.gitignore`
