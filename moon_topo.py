import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from netCDF4 import Dataset
import cmocean.cm as cm
import cmaputil

# read data
path = "/local/kloewer/marsmoon/Moon/GRGM900B_SHA_geoid.grd"
nc = Dataset(path)

x0,x1 = (3000,5000)
y0,y1 = (500,2000)

lon = nc["x"][x0:x1]
lat = nc["y"][y0:y1]
z = nc["z"][y0:y1,x0:x1]

## compute gradient of z in y direction

dzdy = np.gradient(z,axis=0)

# rescale to be within -1,1
dzdy = dzdy - dzdy.min()
dzdy = dzdy/(dzdy.max()/2) - 1


# highlights / lowlights
# highlights = np.ma.MaskedArray(dzdy,mask=dzdy > 0.4)
# lowlights = np.ma.MaskedArray(dzdy,mask=dzdy < 0.7)
# 
# zm = np.ma.MaskedArray(z,mask=np.logical_or(dzdy > 0.7,dzdy < 0.3))
# 

## plot data

# levels for contourf
lev = np.linspace(-500,500,128)
lights = np.linspace(np.percentile(dzdy,0.5),np.percentile(dzdy,99.5),128)

phase2 = cm.thermal.from_list('phase2',np.vstack((cm.phase(np.arange(128,256)),cm.phase(np.arange(0,64)))))

# figure
fig = plt.figure(figsize=(6,5))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

plt.tight_layout(rect=[0,.1,1,0.98])
cax = fig.add_axes([0.06,0.09,0.88,0.03])

ax.set_extent([lon[0], lon[-1], lat[0], lat[-1]], crs=ccrs.PlateCarree())



#ax.contourf(lon, lat, np.ones_like(z),lev,transform=ccrs.PlateCarree(0.0),cmap="magma",extend="both")

#ax.contourf(lon, lat, dzdy,lights,transform=ccrs.PlateCarree(0.0),cmap="Greys",extend="both")
#ax.contourf(lon, lat, lowlights,lights,transform=ccrs.PlateCarree(0.0),cmap="Greys",alpha=0.3)
q = ax.contourf(lon, lat, z,lev,transform=ccrs.PlateCarree(0.0),cmap=phase2,extend="both")
# 
# dr = 0.1
# for i in np.arange(-1,0.5,dr):
#     dzdym = np.ma.MaskedArray(dzdy,mask=~np.logical_and(dzdy >= i,dzdy < i+dr))
#     ax.contourf(lon,lat,dzdym,lights,transform=ccrs.PlateCarree(0.0),alpha=(i+dr/2)**2,cmap="Greys")
# 
# for i in np.arange(0.5,1.0,dr):
#     dzdym = np.ma.MaskedArray(dzdy,mask=~np.logical_and(dzdy >= i,dzdy < i+dr))
#     ax.contourf(lon,lat,dzdym,lights,transform=ccrs.PlateCarree(0.0),alpha=(i+dr/2),cmap="Greys",extend="max")

cb = plt.colorbar(q,cax=cax,orientation="horizontal")
cb.set_ticks([-500,-400,-300,-200,-100,0,100,200,300,400,500])

ax.set_title("Moon geoid",loc="left")
cb.set_label("[m]")

plt.savefig("figs/map_z_phase3.png",dpi=300)
plt.close(fig)
