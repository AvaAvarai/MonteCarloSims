import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Particle:
    def __init__(self, box_size):
        self.box_size = box_size
        self.radius = 0.1  # Particle radius
        self.position = np.random.rand(2) * box_size
        self.velocity = (np.random.rand(2) - 0.5) * 0.1
        self.energy = 0.5  # Initial energy level (midway between blue and red)

    def move(self):
        self.position += self.velocity
        self.check_collision_with_walls()

    def check_collision_with_walls(self):
        for i in range(2):
            if self.position[i] - self.radius <= 0 or self.position[i] + self.radius >= self.box_size:
                self.velocity[i] = -self.velocity[i]
                self.position[i] = np.clip(self.position[i], self.radius, self.box_size - self.radius)

    def trade_energy(self, other_particle):
        # Randomly decide the direction of energy transfer
        direction = np.sign(np.random.randn())
        # Transfer energy based on direction
        self.energy -= direction * 0.1
        other_particle.energy += direction * 0.1

    def get_color(self):
        # Interpolate color based on energy level
        return (self.energy, 0, 1 - self.energy)

def update_particles(particles):
    for i, particle in enumerate(particles):
        particle.move()
        # Check collision with other particles
        for other_particle in particles[i+1:]:
            if np.linalg.norm(particle.position - other_particle.position) < particle.radius + other_particle.radius:
                particle.trade_energy(other_particle)
                # Change color based on energy level after collision
                particle.energy = np.clip(particle.energy, 0, 1)
                other_particle.energy = np.clip(other_particle.energy, 0, 1)

def animate(i, particles, scat):
    update_particles(particles)
    colors = [particle.get_color() for particle in particles]
    scat.set_offsets([particle.position for particle in particles])
    scat.set_facecolors(colors)
    return scat,

def run_simulation(fig, num_particles, box_size, interval, ax):
    particles = [Particle(box_size) for _ in range(num_particles)]
    scat = ax.scatter([particle.position[0] for particle in particles],
                      [particle.position[1] for particle in particles], s=50)
    ax.set_xlim(0, box_size)
    ax.set_ylim(0, box_size)
    return FuncAnimation(fig, animate, fargs=(particles, scat), interval=interval, blit=True, cache_frame_data=False)

def main():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_title('Square Region: 350 particles')
    # Increase interval for slower animation (in milliseconds)
    anim = run_simulation(fig, num_particles=300, box_size=10, interval=20, ax=ax)
    plt.show()

if __name__ == "__main__":
    main()
