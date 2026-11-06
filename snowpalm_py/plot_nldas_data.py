import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

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
