"""
Calculate flight distances considering topography - Python conversion of distances.m
"""
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def distances(x, z_ballistic, direction, topography_file='Topography.xlsx'):
    """
    Calculate the flight distance of ballistic clasts by comparing their flight 
    trajectory with the topography of the volcano.
    
    Args:
        x: matrix where every row represents the trajectory x-coordinates of one clast
        z_ballistic: matrix where every row represents the trajectory z-coordinates of one clast
        direction: vector with one entry for every clast (1=north, 2=south, 3=east, 4=west)
        topography_file: path to the Excel file containing topography data
    
    Returns:
        distances: array of flight distances [north, south, east, west] for each clast
    """
    # Storage vectors
    n_clasts = len(direction)
    distances_north = np.zeros(n_clasts)
    distances_south = np.zeros(n_clasts)
    distances_east = np.zeros(n_clasts)
    distances_west = np.zeros(n_clasts)
    
    # Import topography data
    df = pd.read_excel(topography_file, sheet_name='Licancabur')
    
    # Extract topography profiles for each direction
    x_east = df['x_east'].dropna().values
    topography_east = df['topography_east'].dropna().values
    
    x_north = df['x_north'].dropna().values
    topography_north = df['topography_north'].dropna().values
    
    x_west = df['x_west'].dropna().values
    topography_west = df['topography_west'].dropna().values
    
    x_south = df['x_south'].dropna().values
    topography_south = df['topography_south'].dropna().values
    
    # Convert topography such that the vent elevation is at 0
    vent_elevation = 5923
    topography_east = topography_east - vent_elevation
    topography_west = topography_west - vent_elevation
    topography_north = topography_north - vent_elevation
    topography_south = topography_south - vent_elevation
    
    # Create interpolation functions for each direction
    Topography_east = interp1d(x_east, topography_east, kind='linear', 
                               bounds_error=False, fill_value='extrapolate')
    Topography_west = interp1d(x_west, topography_west, kind='linear',
                               bounds_error=False, fill_value='extrapolate')
    Topography_north = interp1d(x_north, topography_north, kind='linear',
                                bounds_error=False, fill_value='extrapolate')
    Topography_south = interp1d(x_south, topography_south, kind='linear',
                                bounds_error=False, fill_value='extrapolate')
    
    # Calculate the flight distance by comparing the flight trajectory against topography
    for k in range(n_clasts):
        if direction[k] == 1:  # North
            for i in range(len(z_ballistic[k])):
                if z_ballistic[k, i] < Topography_north(x[k, i]):
                    x_impact_north = x[k, i-1] + ((x[k, i] - x[k, i-1]) / 2)
                    distances_north[k] = x_impact_north
                    break
        
        elif direction[k] == 2:  # South
            for i in range(len(z_ballistic[k])):
                if z_ballistic[k, i] < Topography_south(x[k, i]):
                    x_impact_south = x[k, i-1] + ((x[k, i] - x[k, i-1]) / 2)
                    distances_south[k] = x_impact_south
                    break
        
        elif direction[k] == 3:  # East
            for i in range(len(z_ballistic[k])):
                if z_ballistic[k, i] < Topography_east(x[k, i]):
                    x_impact_east = x[k, i-1] + ((x[k, i] - x[k, i-1]) / 2)
                    distances_east[k] = x_impact_east
                    break
        
        elif direction[k] == 4:  # West
            for i in range(len(z_ballistic[k])):
                if z_ballistic[k, i] < Topography_west(x[k, i]):
                    x_impact_west = x[k, i-1] + ((x[k, i] - x[k, i-1]) / 2)
                    distances_west[k] = x_impact_west
                    break
    
    # Output: flight distances that take the topography into account
    distances_array = np.column_stack([distances_north, distances_south, 
                                       distances_east, distances_west])
    
    return distances_array
