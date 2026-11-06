# Define forcing data domains

from pathlib import Path

def domains(Domain: str) -> tuple[ulx: float,
								uly:float,
								lrx: float,
								lry: float,
								outdir: str,
								demfile: str]:
	# Input:
	# Output: tuple
		# ulx: upper left X coordinate (longitude)
		# uyl: upper right Y coordinate (latitude)
		# lrx: lower right X coordinate (longitude)
		# lry: lower right y coordinate (latitude)
		# outdir: directory for outputs
		# dem: path to DEM data file
	print(f"Domain = {Domain}")
	demfile = "data/US_DEM.tif" # TODO: move into CONF file
	outdir = "testing_outputs/" # TODO: move into CONF file
	
	# DEM file: to be used along with the forcing data (will be reprojected)
	if not Path(demfile).is_file():
		print(f"DEM file does not exist = {demfile}")
	print(f"DEM file: {demfile}")
	
	# Forcing domains (download areas that are larger than, or encompass multiple indivudal snowPALM domains
	# TODO: currently only uses one forcing domain (?) (from default in snowPALM) for Valles
	
	# Bounding box lat/lon coordinates (Northwest to Southeast corner) for the Valles Caldera region
	all_domains = [
		{
			"name": "Valles",
			"ulx": -107,
			"uly": 36.5,
			"lrx": -106,
			"lry": 35.5
		}
	]

	# Search for domain
	forcing_domain_found = False
	for domain in all_domains:
		if domain["name"] is Domain:
			forcing_domain_found = True
			ulx = domain["ulx"]
			uly = domain["uly"]
			lrx = domain["lrx"]
			lry = domain["lry"]
	if not forcing_domain_found:
		print(f"No forcing domain called on {Domain}")

	return ulx, uly, lrx, lry, outdir, demfile
