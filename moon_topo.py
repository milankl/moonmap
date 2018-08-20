import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from netCDF4 import Dataset
import cmocean.cm as cm

# read data
path = "/local/kloewer/marsmoon/Moon/GRGM900B_SHA_geoid.grd"
nc = Dataset(path)
lon = nc["x"][:]
lat = nc["y"][:]
z = nc["z"][:,:]

## plot data
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())

ax.set_global()

ax.contourf(lon, lat, z, 256,transform=ccrs.PlateCarree(central_longitude=90.))

plt.tight_layout()
plt.savefig("figs/map1.png",dpi=300)
plt.close(fig)
