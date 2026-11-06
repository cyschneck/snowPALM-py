import snowpalm_py as snowpalm

from pathlib import Path


if __name__ == "__main__":
	# Inputs: TO BE MOVED TO CONF FILE (TODO)
	output_directory = "testing_outputs/" # local directory where forcing data will be stored
	domain = "Valles"

	# make output directory
	Path(output_directory).mkdir(parents=True, exist_ok=True) # make if does not exist

	# define forcing data domains
	snowpalm.domains(Domain=domain)
