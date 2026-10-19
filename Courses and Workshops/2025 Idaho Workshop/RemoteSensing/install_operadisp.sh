#!/usr/bin/env sh

# conda create -n opera_disp-s1 --yes
# conda activate opera_disp-s1
git clone https://github.com/insarlab/MintPy.git
pip install -e ./MintPy
git clone https://github.com/opera-adt/disp-xr.git
pip install -e ./disp-xr
pip install matplotlib ipykernel pandas rasterio rioxarray asf_search opera_utils zarr s3fs dem_stitcher tile_mate contextily h5netcdf h5py ipyleaflet ipywidgets jupyter-leaflet

