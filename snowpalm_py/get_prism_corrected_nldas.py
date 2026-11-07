import snowpalm_py as snowpalm

import earthaccess
from earthaccess.exceptions import LoginAttemptFailure
import xarray as xr
import numpy as np
import rasterio

from pathlib import Path
import os
from datetime import datetime, timezone
import urllib.request

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
	print("\nCollect EarthData")
	try:
		auth = earthaccess.login(strategy="environment") # via password/username in config.ini
	except LoginAttemptFailure:
		print(f"Invalid EarthAccess Creds")
	except Exception as e:
		print(f"Unexpected error occured during EarthAccess Login authentication: {e}")
	else:
		print("EarthAccess Login Successful")
		
		data_file = "NLDAS_FORA0125_H"
		print(f"Download data: {data_file}")
		
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
		Domain="Valles"
		valles_domain = snowpalm.domains(Domain=Domain)
		ulx = valles_domain[0]
		uly = valles_domain[1]
		lrx = valles_domain[2]
		lry = valles_domain[3]
		output_dir = valles_domain[4]
		demfile = valles_domain[5]
		print(valles_domain)
		
		nc_filename = f"testing_outputs/NLDAS_FORA0125_H_{start_year}{start_month}{start_day}_{end_year}{end_month}{end_day}.nc"

		if not Path(nc_filename).is_file():
			# Access data via EarthAccess
			NLDAS_results = earthaccess.search_data(short_name="NLDAS_FORA0125_H",
													version="2.0",
													temporal=(f"{start_year}-{start_month}-{start_day}", f"{end_year}-{end_month}-{end_day}"),
													bounding_box=(lrx, lry, ulx, uly))
													#,count=1) # TODO: count only collects one file
		
			total_download_size = sum([nldas_file.size for nldas_file in NLDAS_results]) / 1024
			print(f"Total size for {len(NLDAS_results)} files found: {total_download_size:.2f} GB")
			print(f"\nData represents {len(NLDAS_results)} hours of hourly NLDAS data")
					
			NLDAS_files = earthaccess.open(NLDAS_results)
			nldas_ds = xr.open_mfdataset(NLDAS_files, chunks={"time": 12})
			
			# save output to local disk (to save runtime during testing)
			nldas_ds.to_netcdf(nc_filename)
		else:
			print(f"Retrieving data from stored file: {nc_filename}")
			nldas_ds = xr.open_mfdataset(nc_filename)
			nldas_ds = nldas_ds.chunk({"time": 12}) # rechunk in memory after opening
		
		print(f"Data files variables: {list(nldas_ds.data_vars)}")
		print(f"Data Dimensions: {nldas_ds.sizes}")

		#snowpalm.plot_nldas_data(nldas_ds) # plot to view data
		
		# Cut out and resize the DEM to the correct dimensions
		print(f"\nDEM file: {demfile}")
		
		lat = nldas_ds["lat"].values
		lon = nldas_ds["lon"].values
		print((len(lat), len(lon)))
		
		# boolean mask
		locx = (lon > ulx) & (lon < lrx)
		locy = (lat > lry) & (lat < uly)
		
		# grid size
		sz = (np.sum(locy).item(), np.sum(locx).item())

		with rasterio.open(demfile) as dem_src:
			# bounding window based on coordinates from domain
			bounding_window = rasterio.windows.from_bounds(left=ulx,
														bottom=lry,
														right=lrx,
														top=uly,
														transform=dem_src.transform)
			# crop and resize
			dem_sub = dem_src.read(1,
								window=bounding_window,
								out_shape=(sz[1], sz[0]),
								resampling=rasterio.enums.Resampling.bilinear)

			# update metadata
			kwargs = dem_src.meta.copy()
			kwargs.update({
							"height": sz[1],
							"width": sz[0],
							"transform": rasterio.windows.transform(bounding_window, dem_src.transform)
							})

			# save updated DEM
			with rasterio.open("testing_outputs/dem_sub.tif", "w", **kwargs) as dem_out:
				dem_out.write(dem_sub, 1)
				print("Writing: testing_outputs/dem_sub.tif")
		
		# transpose and flip DEM file
		Z = np.fliplr(dem_sub.T)
		
		## write DEM, latitude, longitude data to new netCDF
		domain_name = f"prism_correct_nldas_{Domain}"
		
		# collect lat/lon data, sliced based on domain
		lat_data = lat[locy].astype("float32")
		lon_data = lon[locx].astype("float32")
		
		# transpose elevation data to match latitude as rows and longitude as columns
		elev_data = Z.T.astype("float32")
		
		nc_ds = xr.Dataset(
							data_vars={"Elev": (["lat", "lon"], elev_data, {"units": "meters"})},
							coords={
								"lat": (["lat"], lat_data, {"units": "degrees_north"}),
								"lon": (["lon"], lon_data, {"units": "degrees_east"}),
								}
							)
		
		ncfile = Path(output_dir) / domain_name / "dem.nc"
		ncfile.parent.mkdir(parents=True, exist_ok=True) # ensure parent directory exists for .nc file
		nc_ds.to_netcdf(ncfile)
		print(f"netCDF file 'dem.nc' saved to {output_dir}")

		# Download PRISM data
		# URL: https://prism.oregonstate.edu/downloads/
		# Web service details: https://prism.oregonstate.edu/documents/PRISM_downloads_web_service.
		# https://data.prism.oregonstate.edu/time_series/us/an/4km/ppt/monthly/
		
		# collect PRISM data for each unique month/year combination in data
		prism_data_directory = "testing_outputs/PRISM_data"
		Path(prism_data_directory).mkdir(parents=True, exist_ok=True) # make output directory if does not exist
		print(f"\nCollect PRISM data to save in {prism_data_directory}")
		base_url = "https://data.prism.oregonstate.edu/time_series/us/an/4km/ppt/monthly"
		nc_monthyear_list = np.unique(nldas_ds["time"].dt.strftime("%m-%Y"))
		for month_year in nc_monthyear_list:
			month, year = month_year.split("-")
			month = f"{int(month):02d}"
			prism_data_file = f"prism_ppt_us_25m_{year}{month}.zip"
			prism_data_file_url = f"{base_url}/{year}/{prism_data_file}"
			print(prism_data_file)
			print(prism_data_file_url)
			
			# Define:
			## PRISM takes spare, in-situ point data (i.e. rain gauges or SNOTEL) and transforms it into continuous high-resolution digital grid maps of climate variables (i.e. precipitation, max/min temperature, dew point, and vapor pressure)
			## PRISM uses DEMs (digital elevation models) to account for complex terrain features (i.e. rain shadow, coastal proximity, temperature inversion, vertical atmospheric layers)
			## PRISM applies locally varying, pixel-specific regression equations between climate parameters and elevation rather than a single uniform gradient across a region
			
			# PRISM: Parameter-elevation regression on independent slopes model (spatial interpolation model to calculate how climate variables change across landscapes, explicitly adjusting for terrian variables like elevation, coastal proximity, rain shadows, and atmospheric inversions)
			# tmean: Mean temperature
			# stable: data stability is finalized (at least 6 months old) and will not change (stable vs. provisional)
			# 4kmM: spatial grid resolution of 4 km with monthly (M) temporal frequency == 25m (2.5 archmin = 4km resolution)
			# ppt: precipitation
		
			# Adhere to Oregon State service's data limit
			# PRISM will potentially block an IP address which attempts to download the exact same file more than twice within 24 hours
			prism_file = f"{prism_data_directory}/{prism_data_file}"
			if Path(prism_file).is_file():
				file_last_modified = datetime.fromtimestamp(Path(prism_file).stat().st_mtime, tz=timezone.utc)
				file_age = datetime.now(timezone.utc) - file_last_modified
				if file_age.days < 1:
					print(f"IMPORTANT NOTE:\n\t{prism_data_file} has recently been downloaded, to prevent rate-limiting, wait at least 24 before attempting to download this file via this script.")
					print(f"\tURL for direct download: \n\t{prism_data_file_url}")
			else:
				print(f"Downloading: {prism_data_file}")
				try:
					urllib.request.urlretrieve(prism_data_file_url, f"{prism_data_directory}/{prism_data_file}")
					print("Download complete")
				except Exception as e:
					print(f"Error in download: {e}")
			
			# plot PRISM data
			#snowpalm.plot_prism_data(prism_data_file)
