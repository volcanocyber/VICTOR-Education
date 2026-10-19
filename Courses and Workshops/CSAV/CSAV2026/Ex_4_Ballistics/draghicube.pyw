"""
Drag coefficient calculation function - Python conversion of draghicube.m
"""
import numpy as np
from spline import spline
from splint import splint


def draghicube(mach):
    """
    Calculate drag coefficient for a cube as a function of Mach number.
    Uses empirical data and cubic spline interpolation.
    
    Args:
        mach: Mach number
    
    Returns:
        cd: drag coefficient
    """
    x = np.array([
        -0.9624766, -0.8649155, -0.6435272, -0.5159475, -0.3921201,
        -0.2645403, -0.1932458, -0.1181989, -0.07317073, -0.03564728,
        0.001876173, 0.0619137, 0.1332083, 0.2345216, 0.3245779,
        0.4333959, 0.4934334, 0.5234522, 0.9362102
    ])
    
    y = np.array([
        1.064151, 1.056604, 1.064151, 1.086792, 1.116981,
        1.184906, 1.237736, 1.320755, 1.396226, 1.486792,
        1.607547, 1.728302, 1.788679, 1.811321, 1.811321,
        1.773585, 1.743396, 1.728302, 1.720755
    ])
    
    # Convert x from log10 to actual values
    x = 10**x
    
    n = len(x)
    
    # Set values of Cd for unusually low or high Mach numbers
    if mach < x[0]:
        cd = y[0]
    elif mach > x[-1]:
        cd = y[-1]
    else:
        # Use spline interpolation to get cd from x and y
        y2 = spline(x, y, n, 0, 0)
        cd = splint(x, y, y2, n, mach)
    
    return cd
