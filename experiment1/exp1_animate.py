import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate(i, x, y, scatter, circle, ax):
    sample_size = i + 1
    x_new, y_new = x[i], y[i]
    distance = np.sqrt(x_new**2 + y_new**2)
    color = 'blue' if distance <= 1 else 'red'
    scatter.set_offsets(np.c_[x[:sample_size], y[:sample_size]])
    colors = np.where(np.sqrt(x[:sample_size]**2 + y[:sample_size]**2) <= 1, 'blue', 'red')
    scatter.set_color(colors)
    pi_estimate = 4 * np.sum(np.sqrt(x[:sample_size]**2 + y[:sample_size]**2) <= 1) / sample_size
    ax.set_title(f'Pi Estimation with Monte Carlo Sampling\nEstimate: {pi_estimate:.5f} with {sample_size} samples')

def main():
    # Number of samples
    num_samples = 10_000
    x = np.random.uniform(-1, 1, num_samples)
    y = np.random.uniform(-1, 1, num_samples)

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title('Pi Estimation with Monte Carlo Sampling')

    # Draw the circle boundary
    circle = plt.Circle((0, 0), 1, edgecolor='black', facecolor='none')
    ax.add_patch(circle)

    # Initial scatter plot
    scatter = ax.scatter([], [], s=1)

    # Create animation
    ani = animation.FuncAnimation(fig, animate, frames=num_samples, fargs=(x, y, scatter, circle, ax), interval=10)

    # Show plot
    plt.show()

if __name__ == "__main__":
    main()
