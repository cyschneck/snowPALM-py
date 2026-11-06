import snowpalm_py as snowpalm

import configparser # reads config.ini
from pathlib import Path


if __name__ == "__main__":
	# CONFIGURATIONS
	config = configparser.ConfigParser()
	config.read("config.ini")
	earthaccess_username = config["earthaccess"]["username"]
	earthaccess_password = config["earthaccess"]["password"]
	print(f"EarthAccess:\n\tUsername: {earthaccess_username}\n\tPassword: {earthaccess_password}")
	
	# Inputs: TO BE MOVED TO CONFIG FILE (TODO)
	output_directory = "testing_outputs/" # local directory where forcing data will be stored
	domain = "Valles"

	# make output directory
	Path(output_directory).mkdir(parents=True, exist_ok=True) # make if does not exist

	# define forcing data domains
	domains_result = snowpalm.domains(Domain=domain)
	print(domains_result)
