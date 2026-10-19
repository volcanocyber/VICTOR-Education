"""
Spline interpolation function - Python conversion of splint.m
"""
import numpy as np


def splint(xa, ya, y2a, n, x):
    """
    Given arrays xa[0..n-1] and ya[0..n-1] of length n, and given the array
    y2a[0..n-1], which is the output from spline, and given a value of x,
    this routine returns a cubic-spline interpolated value y.
    
    Args:
        xa: x-values of data points
        ya: y-values of data points
        y2a: second derivatives from spline()
        n: number of points
        x: x-value to interpolate at
    
    Returns:
        y: interpolated y-value
    """
    klo = 0  # Python uses 0-based indexing
    khi = n - 1
    
    # Binary search to find the right interval
    while (khi - klo) > 1:
        k = round((khi + klo) / 2)
        if xa[k] > x:
            khi = k
        else:
            klo = k
    
    h = xa[khi] - xa[klo]
    
    if h == 0:
        raise ValueError('bad xa input in splint')
    
    a = (xa[khi] - x) / h
    b = (x - xa[klo]) / h
    y = (a * ya[klo] + b * ya[khi] + 
         ((a**3 - a) * y2a[klo] + (b**3 - b) * y2a[khi]) * (h**2) / 6)
    
    return y
