"""
Example usage of the ballistic trajectory simulation
Demonstrates how to use the converted Python functions
"""
import numpy as np
import matplotlib.pyplot as plt
from eject import eject
from distances import distances


def main():
    """
    Example demonstrating the use of the ballistic trajectory simulation.
    """
    # Example 1: Calculate a single trajectory
    print("Example 1: Single trajectory calculation")
    print("-" * 50)
    
    thetadeg = 45.0  # ejection angle in degrees
    vi = 100.0       # initial velocity in m/s
    diam = 0.5       # diameter in meters
    
    print(f"Input parameters:")
    print(f"  Ejection angle: {thetadeg}°")
    print(f"  Initial velocity: {vi} m/s")
    print(f"  Diameter: {diam} m")
    print()
    
    # Calculate trajectory
    traj = eject(thetadeg, vi, diam)
    
    x_coords = traj[:, 0]
    z_coords = traj[:, 1]
    
    print(f"Results:")
    print(f"  Maximum horizontal distance: {x_coords[-1]:.2f} m")
    print(f"  Maximum height: {np.max(z_coords):.2f} m")
    print(f"  Number of trajectory points: {len(x_coords)}")
    print()
    
    # Plot the trajectory
    plt.figure(figsize=(10, 6))
    plt.plot(x_coords, z_coords, 'b-', linewidth=2)
    plt.xlabel('Horizontal Distance (m)', fontsize=12)
    plt.ylabel('Height (m)', fontsize=12)
    plt.title('Ballistic Trajectory', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3, label='Ground level')
    plt.axhline(y=-1000, color='r', linestyle='--', alpha=0.3, label='Landing plane')
    plt.legend()
    plt.tight_layout()
    plt.savefig('trajectory_example.png', dpi=150)
    print("Trajectory plot saved as 'trajectory_example.png'")
    print()
    
    # Example 2: Multiple trajectories with different angles
    print("\nExample 2: Multiple trajectories with different angles")
    print("-" * 50)
    
    angles = [30, 45, 60]
    plt.figure(figsize=(12, 7))
    
    for angle in angles:
        traj = eject(angle, vi, diam)
        x_coords = traj[:, 0]
        z_coords = traj[:, 1]
        plt.plot(x_coords, z_coords, linewidth=2, label=f'{angle}°')
        print(f"Angle {angle}°: max distance = {x_coords[-1]:.2f} m")
    
    plt.xlabel('Horizontal Distance (m)', fontsize=12)
    plt.ylabel('Height (m)', fontsize=12)
    plt.title('Ballistic Trajectories at Different Angles', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.axhline(y=-1000, color='r', linestyle='--', alpha=0.3, label='Landing plane')
    plt.legend()
    plt.tight_layout()
    plt.savefig('trajectories_comparison.png', dpi=150)
    print("\nComparison plot saved as 'trajectories_comparison.png'")
    print()
    
    # Example 3: Sensitivity to initial velocity
    print("\nExample 3: Sensitivity to initial velocity")
    print("-" * 50)
    
    velocities = [50, 75, 100, 125]
    plt.figure(figsize=(12, 7))
    
    for vel in velocities:
        traj = eject(45, vel, diam)
        x_coords = traj[:, 0]
        z_coords = traj[:, 1]
        plt.plot(x_coords, z_coords, linewidth=2, label=f'{vel} m/s')
        print(f"Velocity {vel} m/s: max distance = {x_coords[-1]:.2f} m")
    
    plt.xlabel('Horizontal Distance (m)', fontsize=12)
    plt.ylabel('Height (m)', fontsize=12)
    plt.title('Ballistic Trajectories at Different Initial Velocities (45°)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.axhline(y=-1000, color='r', linestyle='--', alpha=0.3, label='Landing plane')
    plt.legend()
    plt.tight_layout()
    plt.savefig('velocities_comparison.png', dpi=150)
    print("\nVelocity comparison plot saved as 'velocities_comparison.png'")
    print()
    
    print("\nAll examples completed successfully!")


if __name__ == "__main__":
    main()
