import numpy as np
import matplotlib.pyplot as plt

def estimate_pi(num_samples):
    # Generate random points
    x = np.random.uniform(-1, 1, num_samples)
    y = np.random.uniform(-1, 1, num_samples)
    
    # Calculate distance from the origin
    distance = np.sqrt(x**2 + y**2)
    
    # Points inside the unit circle
    inside_circle = distance <= 1
    
    # Estimate pi
    pi_estimate = 4 * np.sum(inside_circle) / num_samples
    
    return pi_estimate, x, y, inside_circle

def visualize_pi_estimation(num_samples):
    pi_estimate, x, y, inside_circle = estimate_pi(num_samples)
    
    plt.figure(figsize=(8, 8))
    plt.scatter(x[inside_circle], y[inside_circle], color='blue', s=1, label='Inside Circle')
    plt.scatter(x[~inside_circle], y[~inside_circle], color='red', s=1, label='Outside Circle')
    
    # Draw the circle boundary
    circle = plt.Circle((0, 0), 1, edgecolor='black', facecolor='none')
    plt.gca().add_patch(circle)
    
    plt.title(f'Pi Estimation with Monte Carlo Sampling\nEstimate: {pi_estimate:.5f} with {num_samples} samples')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    num_samples = 10_000
    visualize_pi_estimation(num_samples)
