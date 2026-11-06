import snowpalm_py as snowpalm

import os
import configparser # reads config.ini
from pathlib import Path
import shutil


if __name__ == "__main__":
	# 1. 
	# Setup configuration file (if does not already exist)
	if not Path("config.ini").is_file():
		# create a copy of the config file to edit if does not already exist
		shutil.copy("config.example.ini", "config.ini")
		print("New configuration file created (config.ini). Edit with username/password to continue")

	# 2. 
	# Edit with data for EarthAccess credetials
	config = configparser.ConfigParser()
	config.read("config.ini")
	os.environ["EARTHDATA_USERNAME"] = config["earthaccess"]["username"]
	os.environ["EARTHDATA_PASSWORD"] = config["earthaccess"]["password"]
	print(f"EarthAccess:\n\tUsername: {os.environ['EARTHDATA_USERNAME']}\n\tPassword: {os.environ['EARTHDATA_PASSWORD']}")
	
	# 3. User inputs
	# Inputs: TO BE MOVED TO A CONFIGURATION (?) FILE (TODO)
	output_directory = "testing_outputs/" # local directory where forcing data will be stored
	Path(output_directory).mkdir(parents=True, exist_ok=True) # make output directory if does not exist

	# 4.
	# define forcing data domains
	domain = "Valles"
	domains_result = snowpalm.domains(Domain=domain)
	print(domains_result)

	# 5.
	# Download Data
	snowpalm.get_prism_corrected_nldas(domain="CO_NM",
									start_month=12,
									start_day=1,
									start_year=2013,
									end_month=12,
									end_day=1,
									end_year=2013
									)
