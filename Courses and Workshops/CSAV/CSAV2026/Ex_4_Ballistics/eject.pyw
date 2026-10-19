"""
Main ballistic trajectory calculation - Python conversion of eject.m
"""
import numpy as np
from draghicube import draghicube
from rk import rk


def eject(thetadeg, vi, diam):
    """
    Calculate the trajectory of a ballistic projectile during a volcanic eruption.
    
    Args:
        thetadeg: ejection angle in degrees
        vi: initial velocity (m/s)
        diam: diameter of ballistic (m)
    
    Returns:
        traj: trajectory as [x, z] array where x is horizontal distance and z is height
    """
    # Other input parameters (set within function)
    dragred = 100      # zone of reduced drag (empirical value)
    elev = 5923        # elevation of ejection point (m) - Licancabur summit
    lapse = 6.5        # thermal lapse rate (K/km)
    rad = diam / 2     # radius of ballistic projectiles (m)
    rhor = 2400        # density of ballistic projectiles (kg/m³)
    w = 0              # wind velocity (m/s)
    xi = -1000         # vertical distance between landing point and ejection point (m)
    TzeroC = 14        # Temperature at sea level (°C)
    
    g = 9.80665        # gravity (m/s²)
    erad = 6370800     # earth's radius (meters)
    rair = 286.98      # gas constant for air (J/(kg·K))
    
    # Check whether xi is negative
    if xi >= 0:
        raise ValueError('Please enter a negative value for xi.')
    
    # Initialize variables
    theta = np.radians(thetadeg)  # convert theta to radians
    TzeroK = TzeroC + 273.15      # convert temperature to Kelvin
    
    # Estimate time of travel, assuming no drag
    ttotcd0 = (-vi * np.sin(theta) - 
               np.sqrt(vi**2 * (np.sin(theta)**2) - 2 * g * xi)) / (-g)
    
    dt = ttotcd0 / 500  # length of timesteps
    
    # Initialize storage vectors
    max_steps = 1000  # Allow for more steps if needed
    x = np.zeros(max_steps)
    z = np.zeros(max_steps)
    vx = np.zeros(max_steps)
    vz = np.zeros(max_steps)
    
    vx[0] = vi * np.cos(theta)  # initial vx
    vz[0] = vi * np.sin(theta)  # initial vz
    v = vi                       # initial velocity
    time = 0                     # initial time (seconds)
    zmax = 0                     # maximum point in block's trajectory
    
    # Air pressure at vent
    po = 101300 * ((TzeroK - elev * lapse / 1000) / TzeroK) ** (-g / (rair**2 * lapse / 1000))
    
    # Mass and area of clast (based on "high cube" option)
    mass = 8 * rad**3 * rhor
    area = 4 * rad * rad
    
    # Timesteps
    xnow = x[0]
    znow = z[0]
    vxnow = vx[0]
    vznow = vz[0]
    i = 0
    
    while znow >= xi and i < max_steps - 1:  # run until flightpath crosses landing plane
        # Store current positions and velocities in vectors
        x[i] = xnow
        z[i] = znow
        vx[i] = vxnow
        vz[i] = vznow
        
        # Temperature at znow
        temp = TzeroK - (znow + elev) * lapse / 1000
        
        # Air viscosity at znow
        visc = (0.000172 * (390 / (temp + 117)) * (temp / 273)**1.5) / 10
        
        # Air pressure at znow
        pressure = po * ((TzeroK - (znow + elev) * lapse / 1000) / TzeroK) ** (g / (rair * lapse / 1000))
        
        # Air density at znow
        rhoa = pressure / (rair * temp)
        
        # Sound speed at znow
        c = 20.116 * np.sqrt(temp)
        
        # Velocity relative to wind
        vwind = np.sqrt(vznow**2 + (vxnow - w)**2)
        
        # Mach number
        mach = vwind / c
        
        # Drag coefficient
        cd = draghicube(mach)
        
        # Calculate drag reduction in reduced-drag zone
        if dragred > 0 and np.sqrt(xnow**2 + znow**2) < dragred:
            cdnow = cd * (np.sqrt(xnow**2 + znow**2) / dragred)**2
        else:
            cdnow = cd
        
        # Runge-Kutta to determine new position and velocities
        RK = rk(xnow, znow, vxnow, vznow, w, dt, rhoa, cdnow, area, mass, g, rhor)
        
        # Update position and velocity
        xnow = RK[0]
        znow = RK[1]
        vxnow = RK[2]
        vznow = RK[3]
        
        # Update i for next iteration
        i += 1
        
        # Update time
        time = time + dt
    
    # Interpolate to find the exact value of x when the block hits the earth
    xfinal = x[i-1] + (xnow - x[i-1]) * (xi - z[i-1]) / (znow - z[i-1])
    tfinal = time + dt * (xi - z[i-1]) / (znow - z[i-1])
    zfinal = xi
    vxfinal = vx[i-1] + (vxnow - vx[i-1]) * (xi - z[i-1]) / (znow - z[i-1])
    vzfinal = vz[i-1] + (vznow - vz[i-1]) * (xi - z[i-1]) / (znow - z[i-1])
    vfinal = np.sqrt(vxfinal**2 + vzfinal**2)
    
    # Store the final values
    x[i] = xfinal
    z[i] = zfinal
    
    # Delete unneeded entries in storage vector
    x = x[:i+1]
    z = z[:i+1]
    
    # Output: the trajectory (in 2D) of the ballistic ejectile
    traj = np.column_stack([x, z])
    
    return traj
