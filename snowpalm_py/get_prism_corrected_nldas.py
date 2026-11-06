import earthaccess
from earthaccess.exceptions import LoginAttemptFailure

def download_data():
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
		print(f"Download data: {data_file}")
		
		# NLDAS Data collection
		# NLDAS: North American Land Data Assimiliation System
		# NLDAS provides for spatial and temporal land-surface model (LSM) datasets
	
		# NLDAS_FORA0125_H.002 = NLDAS_FORA0125_H version 2
		# Description: This data set contains the primary forcing hourly data "File A" for Phase 2 of the North American Land Data Assimilation System (NLDAS-2). The data are in 1/8th degree grid spacing and range from Jan 1979 to the present. The temporal resolution is hourly
		# File format: netCDF
		# DOI location: https://doi.org/10.5067/THUF4J1RLSYG
		# Current location: https://www.earthdata.nasa.gov/data/catalog/ges-disc-nldas-fora0125-h-2.0
		
		#NLDAS_data - earthaccess.search_data(short_name="NLDAS_FORA0125_H", version="2.0")

def get_prism_corrected_nldas(domain="",
							start_month="",
							start_year="",
							end_month="",
							end_year=""):
	# Download and process PRISM-corrected NLDS forcing data
	# Input:
		# Domain: A region defined in "domains.py" for which to download forcing data for
		# start_month: month of starting date
		# start_year:  year of starting date
		# end_month:   month of ending date
		# end_year:    year of ending date
	
	# Example: get_prism_corrected_nldas('CO_NM',1,2013,12,2013)
	print("\nget_prism_corrected_nldas()")
	print(f"Domain: {domain}")
	print(f"start_month: {start_month}")
	print(f"start_year: {start_year}")
	print(f"end_month: {end_month}")
	print(f"end_year: {end_year}")
	
	download_data()
	
