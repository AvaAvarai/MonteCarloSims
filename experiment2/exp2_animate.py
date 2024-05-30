import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation

def estimate_pi(num_samples):
    x = np.random.uniform(-1, 1, num_samples)
    y = np.random.uniform(-1, 1, num_samples)
    distance = np.sqrt(x**2 + y**2)
    inside_circle = distance <= 1
    pi_estimate = 4 * np.sum(inside_circle) / num_samples
    return pi_estimate, x, y, inside_circle

def compare_sample_counts(sample_counts, num_runs):
    results = {count: [] for count in sample_counts}

    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(3, 1, height_ratios=[2, 1, 1.5], hspace=0.4)

    scatter_gs = gs[0].subgridspec(1, len(sample_counts), wspace=0.4)
    scatter_axs = [fig.add_subplot(scatter_gs[i]) for i in range(len(sample_counts))]
    error_ax = fig.add_subplot(gs[1])
    convergence_ax = fig.add_subplot(gs[2])

    def animate(frame):
        nonlocal results
        for ax in scatter_axs:
            ax.clear()
        
        current_results = []
        
        for ax, num_samples in zip(scatter_axs, sample_counts):
            pi_estimate, x, y, inside_circle = estimate_pi(num_samples)
            results[num_samples].append(pi_estimate)
            current_results.append((num_samples, pi_estimate))
            
            ax.scatter(x[inside_circle], y[inside_circle], color='blue', s=1, label='Inside Circle')
            ax.scatter(x[~inside_circle], y[~inside_circle], color='red', s=1, label='Outside Circle')
            circle = plt.Circle((0, 0), 1, edgecolor='black', facecolor='none')
            ax.add_patch(circle)
            ax.set_title(f'Samples: {num_samples}\nPi Estimate: {pi_estimate:.5f}', fontsize=10)
            ax.set_xlabel('X', fontsize=8)
            ax.set_ylabel('Y', fontsize=8)
            ax.set_aspect('equal', adjustable='box')
            ax.tick_params(axis='both', which='major', labelsize=8)
        
        handles, labels = scatter_axs[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper center', ncol=2, fontsize=10)
        plt.subplots_adjust(top=0.925)
        
        df = pd.DataFrame(current_results, columns=['Sample Count', 'Pi Estimate'])
        df['Error'] = np.abs(np.pi - df['Pi Estimate'])
        df['Percentage Error'] = (df['Error'] / np.pi) * 100

        error_ax.clear()
        df.plot(x='Sample Count', y='Error', kind='bar', ax=error_ax, legend=False)
        error_ax.set_ylabel('Error', fontsize=10)
        error_ax.set_title('Error in Pi Estimation vs Sample Count', fontsize=12)
        error_ax.set_xticklabels(df['Sample Count'], rotation=0, fontsize=8)
        for i, v in enumerate(df['Error']):
            percentage_error = df['Percentage Error'].iloc[i]
            error_ax.text(i, v + 0.01, f"{percentage_error:.2f}%", ha='center', fontsize=8, verticalalignment='bottom')
        
        convergence_ax.clear()
        for num_samples in sample_counts:
            convergence_ax.plot(results[num_samples], label=f'Samples: {num_samples}')
        convergence_ax.axhline(y=np.pi, color='black', linestyle='--', label='True π')
        convergence_ax.set_title('Convergence of Pi Estimation Over Time', fontsize=12)
        convergence_ax.set_xlabel('Run', fontsize=10)
        convergence_ax.set_ylabel('Pi Estimate', fontsize=10)
        convergence_ax.legend(fontsize=8, loc='upper left')
        convergence_ax.tick_params(axis='both', which='major', labelsize=8)

    anim = FuncAnimation(fig, animate, frames=num_runs, repeat=False)
    plt.show()

    return results

if __name__ == "__main__":
    sample_counts = [10, 100, 1000, 10000, 100000]
    num_runs = 100  # Number of iterations for animation
    results = compare_sample_counts(sample_counts, num_runs)
