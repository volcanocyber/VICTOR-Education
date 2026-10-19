"""
Derivatives calculation function - Python conversion of derivs.m
"""
import numpy as np


def derivs(vwind, vvxwd, vvz, w, dt, rhoa, cdnow, area, mass, g, rhor):
    """
    Calculate the derivatives for the Runge-Kutta integration.
    
    Args:
        vwind: wind velocity magnitude
        vvxwd: x-component of velocity relative to wind
        vvz: z-component of velocity
        w: wind velocity
        dt: time step
        rhoa: air density
        cdnow: drag coefficient
        area: cross-sectional area
        mass: mass of projectile
        g: gravitational acceleration
        rhor: density of projectile
    
    Returns:
        derivs: array of derivatives [dx, dz, dvx, dvz]
    """
    derivs = np.zeros(4)
    
    derivs[0] = (vvxwd + w) * dt
    derivs[1] = vvz * dt
    derivs[2] = -rhoa * cdnow * area * vwind**2 * vvxwd / (2 * mass * vwind) * dt
    derivs[3] = (-g * (rhor - rhoa) / rhor - 
                 rhoa * cdnow * area * vwind**2 * vvz / (2 * mass * vwind)) * dt
    
    return derivs
