import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Particle:
    def __init__(self, box_size, circular=False):
        self.circular = circular
        self.box_size = box_size
        if circular:
            r = box_size / 2
            angle = np.random.rand() * 2 * np.pi
            radius = np.random.rand() * r
            self.position = np.array([r + radius * np.cos(angle), r + radius * np.sin(angle)])
        else:
            self.position = np.random.rand(2) * box_size
        self.velocity = (np.random.rand(2) - 0.5) * 2

    def move(self):
        self.position += self.velocity
        if self.circular:
            self.check_collision_with_circle()
        else:
            self.check_collision_with_walls()

    def check_collision_with_walls(self):
        for i in range(2):
            if self.position[i] <= 0 or self.position[i] >= self.box_size:
                self.velocity[i] = -self.velocity[i]
                self.position[i] = np.clip(self.position[i], 0, self.box_size)

    def check_collision_with_circle(self):
        center = np.array([self.box_size / 2, self.box_size / 2])
        distance_from_center = np.linalg.norm(self.position - center)
        if distance_from_center >= self.box_size / 2:
            normal = (self.position - center) / distance_from_center
            self.velocity -= 2 * np.dot(self.velocity, normal) * normal
            self.position = center + normal * (self.box_size / 2)

def update_particles(particles):
    for particle in particles:
        particle.move()

def animate(i, particles, scat):
    update_particles(particles)
    scat.set_offsets([particle.position for particle in particles])
    return scat,

def run_simulation(fig, num_particles, box_size, interval, ax, circular=False):
    particles = [Particle(box_size, circular) for _ in range(num_particles)]
    scat = ax.scatter([particle.position[0] for particle in particles],
                      [particle.position[1] for particle in particles], s=1)
    ax.set_xlim(0, box_size)
    ax.set_ylim(0, box_size)
    if circular:
        circle = plt.Circle((box_size / 2, box_size / 2), box_size / 2, color='r', fill=False)
        ax.add_patch(circle)
    return FuncAnimation(fig, animate, fargs=(particles, scat), interval=interval, blit=True, cache_frame_data=False)

def main():
    sample_counts = [10, 100, 1000, 10000]

    fig, axs = plt.subplots(2, 4, figsize=(16, 8), constrained_layout=True)
    axs = axs.flatten()

    animations = []
    for i, num_particles in enumerate(sample_counts):
        ax = axs[i]
        ax.set_aspect('equal')
        ax.set_title(f'Square Region: {num_particles} particles')
        anim = run_simulation(fig, num_particles, box_size=10, interval=20, ax=ax)
        animations.append(anim)

    for i, num_particles in enumerate(sample_counts):
        ax = axs[i + len(sample_counts)]
        ax.set_aspect('equal')
        ax.set_title(f'Circular Region: {num_particles} particles')
        anim = run_simulation(fig, num_particles, box_size=10, interval=20, ax=ax, circular=True)
        animations.append(anim)

    plt.show()

if __name__ == "__main__":
    main()
