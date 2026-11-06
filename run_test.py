import snowpalm_py as snowpalm

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
	earthaccess_username = config["earthaccess"]["username"]
	earthaccess_password = config["earthaccess"]["password"]
	print(f"EarthAccess:\n\tUsername: {earthaccess_username}\n\tPassword: {earthaccess_password}")
	
	# 3. User inputs
	# Inputs: TO BE MOVED TO CONFIG FILE (TODO)
	output_directory = "testing_outputs/" # local directory where forcing data will be stored
	domain = "Valles"
	# make output directory
	Path(output_directory).mkdir(parents=True, exist_ok=True) # make if does not exist

	# 4.
	# define forcing data domains
	domains_result = snowpalm.domains(Domain=domain)
	print(domains_result)
