import os
import matplotlib.pyplot as plt
import torch
import geopandas as gpd
import contextily as ctx
from pyproj import Proj, transform


files = os.listdir(os.path.join(os.getcwd(),"logs"))
dims = []
boxes = []
P3857 = Proj(init="epsg:3857")
P4326 = Proj(init="epsg:4326")
for file in files:
    #latitude -> north/south
    #longitude -> west/east
    logpath = os.path.join(os.getcwd(),"logs",file,"logfile.pt")
    log = torch.load(logpath)
    log_gdf = gpd.GeoDataFrame(log,geometry=gpd.points_from_xy(log.Lng,log.Lat),crs="EPSG:4326")
    print(log_gdf.crs)
    log_gdf.to_crs(crs="EPSG:3857")
    ax = log_gdf.plot(marker = ".")
    print(log_gdf.total_bounds)
    minx, miny, maxx, maxy = log_gdf.total_bounds

    ctx.add_basemap(ax,zoom = "auto",crs="EPSG:3857", source = ctx.providers.OpenStreetMap.HOT)
    plt.savefig(("pictures/"+str(file)+".png"))

# -1, 12, 55, 38