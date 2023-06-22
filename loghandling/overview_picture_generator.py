import os
import matplotlib.pyplot as plt
import torch
import geopandas as gpd
import contextily as ctx
import pandas as pd
from pyproj import Proj, transform


files = os.listdir(os.path.join(os.getcwd(),"logs"))
dims = []
boxes = []
P3857 = Proj(init="epsg:3857")
P4326 = Proj(init="epsg:4326")

log = None

for file in files:
    #latitude -> north/south
    #longitude -> west/east
    logpath = os.path.join(os.getcwd(),"logs",file,"logfile.pt")
    if log is None:
        log = torch.load(logpath)
        
    else:
        log = pd.concat([log,torch.load(logpath)])
log_gdf = gpd.GeoDataFrame(log,geometry=gpd.points_from_xy(log.Lng,log.Lat),crs="EPSG:4326")
log_gdf = log_gdf.to_crs(crs = "EPSG:3857")

print(log_gdf.crs)
ax = log_gdf.plot(figsize= (100,100),marker = ".")

ctx.add_basemap(ax,zoom = "auto", crs="EPSG:3857",  source = ctx.providers.OpenStreetMap.HOT)
plt.savefig(("pictures/overview.png"))
