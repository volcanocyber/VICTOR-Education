"""
Runge-Kutta integration function - Python conversion of rk.m
"""
import numpy as np
from derivs import derivs


def rk(x, z, vx, vz, w, dt, rhoa, cdnow, area, mass, g, rhor):
    """
    Fourth-order Runge-Kutta method for integrating the equations of motion.
    
    Args:
        x: horizontal position
        z: vertical position
        vx: x-component of velocity
        vz: z-component of velocity
        w: wind velocity
        dt: time step
        rhoa: air density
        cdnow: drag coefficient
        area: cross-sectional area
        mass: mass of projectile
        g: gravitational acceleration
        rhor: density of projectile
    
    Returns:
        rk: array containing [new_x, new_z, new_vx, new_vz]
    """
    # First evaluation
    vwind = np.sqrt((vx - w)**2 + vz * vz)
    vvxwd = vx - w
    vxwind = vx - w
    vvz = vz
    
    derivs1 = derivs(vwind, vvxwd, vvz, w, dt, rhoa, cdnow, area, mass, g, rhor)
    
    # Second evaluation
    vwind = np.sqrt((vx + 0.5 * derivs1[2])**2 + (vz + 0.5 * derivs1[3])**2)
    vvxwd = vx + 0.5 * derivs1[2]
    vvz = vz + 0.5 * derivs1[3]
    
    derivs2 = derivs(vwind, vvxwd, vvz, w, dt, rhoa, cdnow, area, mass, g, rhor)
    
    # Third evaluation
    vwind = np.sqrt((vx + 0.5 * derivs2[2])**2 + (vz + 0.5 * derivs2[3])**2)
    vvxwd = vx + 0.5 * derivs2[2]
    vvz = vz + 0.5 * derivs2[3]
    
    derivs3 = derivs(vwind, vvxwd, vvz, w, dt, rhoa, cdnow, area, mass, g, rhor)
    
    # Fourth evaluation
    vwind = np.sqrt((vx + derivs3[2])**2 + (vz + derivs3[3])**2)
    vvxwd = vx + derivs3[2]
    vvz = vz + derivs3[3]
    
    derivs4 = derivs(vwind, vvxwd, vvz, w, dt, rhoa, cdnow, area, mass, g, rhor)
    
    # Combine the derivatives
    r = np.column_stack([derivs1, derivs2, derivs3, derivs4])
    
    d = np.zeros(4)
    for i in range(4):
        d[i] = r[i, 0] / 6 + r[i, 1] / 3 + r[i, 2] / 3 + r[i, 3] / 6
    
    rk_result = np.zeros(4)
    rk_result[0] = x + d[0]      # new x
    rk_result[1] = z + d[1]      # new z
    rk_result[2] = vxwind + d[2] + w  # new vx
    rk_result[3] = vz + d[3]     # new vz
    
    return rk_result
