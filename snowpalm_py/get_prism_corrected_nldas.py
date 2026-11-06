import snowpalm_py as snowpalm

import earthaccess
from earthaccess.exceptions import LoginAttemptFailure
import xarray as xr


def get_prism_corrected_nldas(domain=None,
							start_year=None,
							start_month=None,
							start_day=1,
							end_year=None,
							end_month=None,
							end_day=1):
	# Download and process PRISM-corrected NLDS forcing data
	# Input:
		# Domain: A region defined in "domains.py" for which to download forcing data for
		# start_month: month of starting date
		# start_year:  year of starting date
		# start_day:  date of starting date (default to start of the month)
		# end_month:   month of ending date
		# end_year:    year of ending date
		# end_day:    date of ending date (default to the start of the month)
	
	# Example: get_prism_corrected_nldas('CO_NM',1,2013,12,2013)
	print("\nget_prism_corrected_nldas()")
	print(f"Domain: {domain}")
	print(f"DATES: From {start_year}-{start_month}-{start_day} to {end_year}-{end_month}-{end_day}")
	
	# Login to Earthdata
	try:
		auth = earthaccess.login(strategy="environment") # via password/username in config.ini
	except LoginAttemptFailure:
		print(f"Invalid EarthAccess Creds")
	except Exception as e:
		print(f"Unexpected error occured during EarthAccess Login authentication: {e}")
	else:
		print("EarthAccess Login Successful")
		
		data_file = "NLDAS_FORA0125_H"
		print(f"Download data: {data_file}\n")
		
		# NLDAS Data collection
		# NLDAS provides for spatial and temporal land-surface model (LSM) datasets
	
		# Example dataset: NLDAS_FORA0125_H.A20131201.0100.020.nc
		# NLDAS:     North American Land Data Assimiliation System
		# FORA:      Primary forcing dataset "File A" (default) forcing dataset with eleven fields
		# 0125:      1/8thdegree grid spacing
		# H:         hourly
		# A20131201: A<YYYYMMDD> for the date as year, month, day
		# 0100:      <HH>00 for GMT Hour of the day
		# 020:       data version 2 for NLDAS Phase 2
		# .nc:       netCDF file format
		
		# Forcing hourly data:
		# Tair: 2-meter above ground temperature
		# Qair: 2-meter above ground specific humidity
		# PSurf: surface pressure
		# Wind_E: 10-meter aboveground zonal wind speed
		# Wind_N: 10-meter aboveground meridional wind speed
		# LWdown: longwave radiationflux downwards
		# CRainf##: Convective precipitation
		# CAPE: Convective Available Potential Energy
		# PotEvap: Potential evaporation
		# Rainf: Total precipitation
		# SWdown: Shortwave radiation flux downwards
		
	
		# Description: This data set contains the primary forcing hourly data "File A" for Phase 2 of the North American Land Data Assimilation System (NLDAS-2). The data are in 1/8th degree grid spacing and range from Jan 1979 to the present. The temporal resolution is hourly
		# DOI location: https://doi.org/10.5067/THUF4J1RLSYG
		# Current location: https://www.earthdata.nasa.gov/data/catalog/ges-disc-nldas-fora0125-h-2.0
		# Data details: https://docserver.gesdisc.eosdis.nasa.gov/public/project/hydrology/NLDAS2_README.pdf
		valles_domain = snowpalm.domains(Domain="Valles")
		print(valles_domain)

		# Access data via EarthAccess
		NLDAS_results = earthaccess.search_data(short_name="NLDAS_FORA0125_H",
												version="2.0",
												temporal=(f"{start_year}-{start_month}-{start_day}", f"{end_year}-{end_month}-{end_day}"),
												bounding_box=(valles_domain[2], valles_domain[3], valles_domain[0], valles_domain[1]))
												#,count=1) # TODO: count only collects one file
	
		total_download_size = sum([nldas_file.size for nldas_file in NLDAS_results]) / 1024
		print(f"Total size for {len(NLDAS_results)} files found: {total_download_size:.2f} GB")
				
		NLDAS_files = earthaccess.open(NLDAS_results)
		ds_files = xr.open_mfdataset(NLDAS_files, chunks={"time": 12})
		print(f"\nData represents {len(NLDAS_results)} hours of hourly NLDAS data")
		print(f"Data files variables: {list(ds_files.data_vars)}")
		print(f"Data Dimensions: {ds_files.sizes}")
		#snowpalm.plot_nldas_data(ds_files) # plot to view data
		
