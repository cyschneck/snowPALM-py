import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import plotting_extent
import zipfile

def plot_nldas_data(ds=None):
		variable_list = list(ds.data_vars)[1:] # skip time_bnds
		variable_dict = {
			"Tair":"2-meter above ground temperature",
			"Qair":"2-meter above ground specific humidity",
			"PSurf":"surface pressure",
			"Wind_E":"10-meter above ground zonal wind speed",
			"Wind_N":"10-meter above ground meridional wind speed",
			"LWdown": "longwave radiationflux downwards",
			"CRainf_frac": "Convective precipitation",
			"CAPE": "Convective Available Potential Energy",
			"PotEvap": "Potential evaporation",
			"Rainf": "Total precipitation",
			"SWdown": "Shortwave radiation flux downwards",
		}

		n_plots = len(variable_list)
		ncols = 4
		nrows = 3

		# Setup figure with Cartopy projection on each subplot
		fig, axes = plt.subplots(
			nrows=nrows,
			ncols=ncols,
			figsize=(16, 4 * nrows),
			subplot_kw={'projection': ccrs.PlateCarree()},
			constrained_layout=True,
		)

		# Flatten axes
		axes = axes.flatten()

		for i, var_name in enumerate(variable_list):
			var_data = ds[var_name]
			ax = axes[i]

		# Plot your map data
			if "time" in var_data.dims:
				data_slice = var_data.isel(time=0)
			else:
				data_slice = var_data

			data_slice.plot(
				ax=ax,
				transform=ccrs.PlateCarree(),
				cmap="viridis",
				cbar_kwargs={"label": f"{var_data.name} ({var_data.attrs.get('units', '')})"},
			)

			# Add map features and coastlines
			ax.coastlines()
			ax.add_feature(cfeature.BORDERS, linestyle=':')
			ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

			ax.set_title(f"{variable_dict[var_name]}")

		# Hide any unused axes
		for j in range(n_plots, len(axes)):
			fig.delaxes(axes[j])

		plt.savefig("testing_outputs/NLDAS_testing.png")
		#plt.show()

def plot_prism_data(prism_data_file=None):
	print(f"plot data: {prism_data_file}")
	
	# files within zip file
	internal_rasterio_file = None
	with zipfile.ZipFile(f"testing_outputs/PRISM_data/{prism_data_file}", "r") as z:
		for zip_file in z.infolist():
			if str(zip_file.filename).split(".")[-1] in ["bil", "tif", "asc"]:
				print(zip_file.filename)
				internal_rasterio_file = zip_file.filename
	print(internal_rasterio_file)
	
	zip_path = f"zip://testing_outputs/PRISM_data/{prism_data_file}!{internal_rasterio_file}"
	with rasterio.open(zip_path) as prism_src:
		print(f"Dimensions: {prism_src.width} by {prism_src}")
		print(f"Bands: {prism_src.count}")
		print(f"Coordinate Reference System: {prism_src.crs}")
		print(f"Transform by Bounds/Resolution: {prism_src.transform}")
		ppt_array = prism_src.read(1, masked=True)

	print(f"Max Precipitation: {ppt_array.max():.2f} mm")
	print(f"Mean Precipitation: {ppt_array.mean():.2f} mm")

	# 4. Plot the extracted raster map
	plt.figure(figsize=(8, 8))
	plt.imshow(ppt_array, cmap="Blues", extent=plotting_extent(prism_src))
	plt.colorbar(label="Precipitation (mm)")
	plt.title(f"PRISM Total Precipitation: {prism_data_file}")
	plt.xlabel("Longitude (Degree)")
	plt.ylabel("Latitude (Degree)")
	plt.grid(True, linestyle="--", alpha=0.5)
	plt.savefig("testing_outputs/prism_data_testing.png")
	plt.show()
	
