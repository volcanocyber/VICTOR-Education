# Ballistic Trajectory Simulation - Python Conversion

This package contains a Python conversion of the MATLAB ballistic trajectory simulation code for volcanic eruptions.

## Overview

This simulation calculates the trajectory of ballistic projectiles during volcanic eruptions, accounting for:
- Atmospheric conditions (pressure, density, temperature)
- Drag forces and drag coefficient variations with Mach number
- Wind effects
- Topographic constraints

## Files

### Core Functions
- `eject.py` - Main function to calculate ballistic trajectory
- `rk.py` - 4th order Runge-Kutta integration
- `derivs.py` - Derivatives calculation for the equations of motion
- `draghicube.py` - Drag coefficient calculation for cubic projectiles
- `spline.py` - Cubic spline computation
- `splint.py` - Cubic spline interpolation
- `distances.py` - Calculate flight distances considering topography

### Data
- `Topography.xlsx` - Topographic profiles for Licancabur volcano (4 directions)

### Examples
- `example_usage.py` - Demonstrates how to use the simulation

## Requirements

```
numpy
pandas
scipy
matplotlib
openpyxl  # for reading Excel files
```

## Installation

Install the required packages:

```bash
pip install numpy pandas scipy matplotlib openpyxl
```

## Usage

### Basic Example

```python
from eject import eject

# Calculate a single trajectory
thetadeg = 45.0  # ejection angle in degrees
vi = 100.0       # initial velocity in m/s
diam = 0.5       # diameter in meters

traj = eject(thetadeg, vi, diam)

# Extract coordinates
x_coords = traj[:, 0]  # horizontal distance
z_coords = traj[:, 1]  # height
```

### Using Topography

```python
import numpy as np
from distances import distances

# Assuming you have multiple trajectories
# x: array of x-coordinates for each clast (rows = clasts, cols = trajectory points)
# z: array of z-coordinates for each clast
# direction: array indicating direction (1=north, 2=south, 3=east, 4=west)

flight_distances = distances(x, z, direction, 'Topography.xlsx')
```

### Running the Examples

```bash
python example_usage.py
```

This will generate three comparison plots:
- Single trajectory
- Multiple ejection angles
- Multiple initial velocities

## Parameters

### Input Parameters (in `eject` function)

- `thetadeg`: Ejection angle in degrees (0-90)
- `vi`: Initial velocity in m/s
- `diam`: Diameter of projectile in meters

### Internal Parameters (can be modified in `eject.py`)

- `dragred`: Zone of reduced drag in meters (default: 100)
- `elev`: Elevation of ejection point in meters (default: 5916, Licancabur summit)
- `lapse`: Thermal lapse rate in K/km (default: 6.5)
- `rhor`: Density of ballistic projectiles in kg/m³ (default: 2400)
- `w`: Wind velocity in m/s (default: 0)
- `xi`: Vertical distance to landing plane in meters (default: -1000, must be negative)
- `TzeroC`: Temperature at sea level in °C (default: 14)

## Physical Model

The simulation uses:
1. **4th order Runge-Kutta integration** for accurate trajectory calculation
2. **Cubic spline interpolation** for drag coefficient calculation
3. **Standard atmosphere model** with temperature lapse rate
4. **Drag force** that varies with Mach number
5. **Buoyancy effects** based on projectile and air density

## Differences from MATLAB Version

1. **Array indexing**: Python uses 0-based indexing (MATLAB uses 1-based)
2. **Array creation**: Uses NumPy arrays instead of MATLAB matrices
3. **Interpolation**: Uses scipy.interpolate for topography functions
4. **File I/O**: Uses pandas for Excel file reading

## Notes

- The coordinate system has the ejection point at (0, 0)
- The landing plane is at z = xi (typically -1000 m)
- Topography elevations are adjusted so the vent is at z = 0
- The simulation stops when the trajectory crosses the landing plane

## Citation

If you use this code, please cite:

**Original Visual Basic implementation:**
- Mastin, L.G. (2001). A simple calculator of ballistic trajectories for blocks ejected during volcanic eruptions. U.S. Geological Survey Open-File Report 01-45, 16p. https://pubs.usgs.gov/of/2001/0045/

**MATLAB translation:**
- Strehlow, K., Mastin, L.G., Sandri, L., Gottsmann, J.H., Kilgour, G., Rust, A.C., & Tonini, R. (2019). Eject! for Matlab. https://vhub.org/resources/4543

**Related publication:**
- Strehlow, K., Sandri, L., Gottsmann, J.H., Kilgour, G., Rust, A.C., & Tonini, R. (2017). Phreatic eruptions at crater lakes: occurrence statistics and probabilistic hazard forecast. Journal of Applied Volcanology, 6(4). DOI: 10.1186/s13617-016-0053-2

**Python conversion:**
- This Python version (2026) is an independent conversion of the MATLAB code for use with Python scientific computing libraries.

## License

This is a conversion of the original MATLAB code. Please respect any licensing 
terms associated with the original implementation.
