## What this is
A collection of hands‑on educational materials for volcanology and remote sensing aimed at students and instructors (workshops, labs, and course modules). The repo is notebook-first: interactive Jupyter notebooks plus supporting Python utilities and images that together teach petrology, physical volcanology, and remote sensing workflows.

### Stack
- **Language(s):** Jupyter Notebook (primary), Python for supporting scripts
- **Framework / runtime:** Jupyter / IPython notebooks (run with JupyterLab or Jupyter Notebook)
- **Notable libraries:** common scientific / geospatial Python stack (numpy, matplotlib, xarray/rasterio, pandas, scipy) used across notebooks and scripts

## How it's organized
```
.gitignore                         repo ignores
Courses and Workshops/             workshop and course folders (2023 VICTOR Workshop, 2025 Idaho Workshop, CSAV, Goldschmidt 2026, IAVCEI 2025, USF Comp Volc Courses)
Petrology/                         petrology notebooks and exercises
  MELTS_Crystallization_Examples.ipynb
  MantleMelting_ex.ipynb
  MantleMelting_lab_VICTOR.ipynb
  Viscosity_ex.ipynb

Physical Volcanology Modules/      notebooks, assignments, and images for physical volcanology
  Melt_Density.ipynb
  Melt_Density_Assignment.ipynb
  Answerkey_Melt_Density_Assignment.ipynb
  suface_deformation.ipynb
  images/                          diagrams and photos (mogi_equation_diagram.jpeg, mogi_source_usgs.jpg)

Remote Sensing/                    remote sensing lab materials
  Remote Sensing Lab/
    remote_sensing_lab.ipynb
    src/                           Python utilities used by the notebooks (cslc_utils.py, dist_utils.py, dswx_utils.py, ...)
```

How it fits together: The notebooks are the primary teaching artifacts (lecture/lab content and assignments). Notebooks in Remote Sensing call into the Python utilities under Remote Sensing/Remote Sensing Lab/src (for processing SAR, distribution utilities, etc.), and Physical Volcanology/ Petrology folders contain topic-specific exercises and answer keys. Images and data embedded in notebooks are used for figures and worked examples.

## How to run it
The simplest way to use these materials is to open the notebooks in Jupyter and run cells. If you want to run the Remote Sensing lab (which includes Python utilities), install the typical scientific/geospatial packages and point any cloud credentials the notebooks expect at a secure location.

Example commands (replace or extend package list as needed):
```
# create and activate a venv (optional)
python -m venv .venv
source .venv/bin/activate

# install minimal typical stack used by the notebooks
pip install jupyterlab numpy matplotlib pandas scipy xarray rasterio

# start the notebook UI
jupyter lab
```

Note:
- Several notebooks and the remote_sensing_lab.ipynb are large — open them in JupyterLab or nbviewer for best results.
