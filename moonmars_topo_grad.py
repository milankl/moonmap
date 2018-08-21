import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from netCDF4 import Dataset
from cmaputil import cm

path1 = "/local/kloewer/marsmoon/Moon/LOLA2600p_geoid.grd"
path2 = "/local/kloewer/marsmoon/Mars/MarsTopo_geoid_jgmro_110c.grd"

# read data Moon
nc = Dataset(path1)

x0,x1 = (2000,-1)
y0,y1 = (200,2700)

lon_moon = nc["x"][x0:x1]
lat_moon = nc["y"][y0:y1]
z_moon = nc["z"][y0:y1,x0:x1]

# read data Mars
nc = Dataset(path2)

lon_mars = nc["x"][x0:x1]
lat_mars = nc["y"][y0:y1]
z_mars = nc["z"][y0:y1,x0:x1]

## compute gradient of z in y direction
# ignore dy as it is constant

dz_moon = np.gradient(z_moon,axis=0)
dz_mars = np.gradient(z_mars,axis=0)

## plot data

# vmin vmax for pcolormesh
# use percentiles to ignore outliers
lev_moon = (np.percentile(dz_moon,2),np.percentile(dz_moon,98))
lev_mars = (np.percentile(dz_mars,1),np.percentile(dz_mars,99))

# figure
fig = plt.figure(figsize=(8,4))

# map projection
moonproj = ccrs.NearsidePerspective(central_latitude=0.,central_longitude=250,satellite_height=40000000.0)
marsproj = ccrs.NearsidePerspective(central_latitude=0.,central_longitude=270,satellite_height=40000000.0)
contourfproj = ccrs.RotatedPole(pole_longitude=180.)

ax_moon = fig.add_subplot(1,2,1,projection=moonproj)
ax_mars = fig.add_subplot(1,2,2,projection=marsproj)

plt.tight_layout(rect=[-.2,.12,1.2,0.95])
fig.subplots_adjust(wspace=-0.4,hspace=0.)

ax_moon.set_global()
ax_mars.set_global()

# plotting the gradient
ax_moon.pcolormesh(lon_moon,lat_moon,dz_moon,vmin=lev_moon[0],vmax=lev_moon[1],transform=contourfproj,cmap="Greys")
ax_mars.pcolormesh(lon_mars,lat_mars,dz_mars,vmin=lev_mars[0],vmax=lev_mars[1],transform=contourfproj,cmap="Greys")

ax_moon.set_title("Moon",loc="left",color="w")
ax_mars.set_title("Mars",loc="left",color="w")

plt.savefig("figs/moon_mars_grad.png",dpi=300,facecolor="k")
plt.close(fig)
