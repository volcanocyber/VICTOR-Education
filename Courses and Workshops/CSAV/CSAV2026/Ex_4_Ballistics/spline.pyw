"""
Spline computation function - Python conversion of spline.m
"""
import numpy as np


def spline(x, y, n, yp1, ypn):
    """
    Given arrays x[0..n-1] and y[0..n-1] containing a tabulated function,
    i.e., yi = f(xi), with x0 < x1 < ... < xn-1, and given values yp1 and ypn
    for the first derivative of the interpolating function at points 0 and n-1,
    respectively, this routine returns an array y2[0..n-1] that contains the
    second derivatives of the interpolating function at the tabulated points xi.
    If yp1 and/or ypn are equal to 1e30 or larger, the routine is signaled to
    set the corresponding boundary condition for a natural spline, with zero
    second derivative on that boundary.
    
    Args:
        x: x-values of data points
        y: y-values of data points
        n: number of points
        yp1: first derivative at point 0 (use large value like 1e30 for natural spline)
        ypn: first derivative at point n-1 (use large value like 1e30 for natural spline)
    
    Returns:
        y2: array of second derivatives
    """
    y2 = np.zeros(n)
    u = np.zeros(n)
    
    if yp1 > 9.9e29:
        y2[0] = 0
        u[0] = 0
    else:
        y2[0] = -0.5
        u[0] = (3 / (x[1] - x[0])) * ((y[1] - y[0]) / (x[1] - x[0]) - yp1)
    
    for i in range(1, n - 1):
        sig = (x[i] - x[i - 1]) / (x[i + 1] - x[i - 1])
        p = sig * y2[i - 1] + 2
        y2[i] = (sig - 1) / p
        u[i] = (6 * ((y[i + 1] - y[i]) / (x[i + 1] - x[i]) - 
                     (y[i] - y[i - 1]) / (x[i] - x[i - 1])) / 
                (x[i + 1] - x[i - 1]) - sig * u[i - 1]) / p
    
    if ypn > 9.9e29:
        qn = 0
        un = 0
    else:
        qn = 0.5
        un = (3 / (x[n - 1] - x[n - 2])) * (ypn - (y[n - 1] - y[n - 2]) / 
                                             (x[n - 1] - x[n - 2]))
    
    y2[n - 1] = (un - qn * u[n - 2]) / (qn * y2[n - 2] + 1)
    
    for k in range(n - 2, -1, -1):
        y2[k] = y2[k] * y2[k + 1] + u[k]
    
    return y2
