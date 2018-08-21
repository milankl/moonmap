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

## plot data

# levels for contourf
# use percentiles to ignore outliers
lev_moon = np.linspace(np.percentile(z_moon,0.5),np.percentile(z_moon,99.9),64)
lev_mars = np.linspace(np.percentile(z_mars,0.5),np.percentile(z_mars,99.99),64)

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
cax_moon = fig.add_axes([0.06,0.11,0.38,0.03])
cax_mars = fig.add_axes([0.56,0.11,0.38,0.03])

ax_moon.set_global()
ax_mars.set_global()

# plotting the height
qmo = ax_moon.contourf(lon_moon,lat_moon,z_moon,lev_moon,transform=contourfproj,cmap=cm.cividis,extend="both")
qma = ax_mars.contourf(lon_mars,lat_mars,z_mars,lev_mars,transform=contourfproj,cmap=cm.cividis,extend="both")

cb_moon = plt.colorbar(qmo,cax=cax_moon,orientation="horizontal")
cb_moon.set_ticks(np.arange(-4,8,1))
cb_moon.ax.tick_params(labelsize=8,color="w",labelcolor="w")
cb_moon.outline.set_edgecolor("w")
cb_moon.set_label("Topography [km]",color="w",size=8)

cb_mars = plt.colorbar(qma,cax=cax_mars,orientation="horizontal")
cb_mars.set_ticks(np.arange(-10,30,2))
cb_mars.ax.tick_params(labelsize=8,color="w",labelcolor="w")
cb_mars.outline.set_edgecolor("w")
cb_mars.set_label("Topography [km]",color="w",size=8)

ax_moon.set_title("Moon",loc="left",color="w")
ax_mars.set_title("Mars",loc="left",color="w")

plt.savefig("figs/moon_mars_z.png",dpi=300,facecolor="k")
plt.close(fig)
