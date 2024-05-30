import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

def compare_sample_counts(sample_counts):
    results = []

    # Create a figure with 2 gridspecs: one for scatter plots, one for the bar plot
    fig = plt.figure(figsize=(15, 8))
    gs = fig.add_gridspec(2, 1, height_ratios=[2.5, 1.5], hspace=0.3)

    scatter_gs = gs[0].subgridspec(1, len(sample_counts), wspace=0.35)
    bar_ax = fig.add_subplot(gs[1])

    scatter_axs = []
    for i in range(len(sample_counts)):
        scatter_axs.append(fig.add_subplot(scatter_gs[i]))

    for ax, num_samples in zip(scatter_axs, sample_counts):
        pi_estimate, x, y, inside_circle = estimate_pi(num_samples)
        results.append((num_samples, pi_estimate))
        
        ax.scatter(x[inside_circle], y[inside_circle], color='blue', s=1, label='Inside Circle')
        ax.scatter(x[~inside_circle], y[~inside_circle], color='red', s=1, label='Outside Circle')
        
        # Draw the circle boundary
        circle = plt.Circle((0, 0), 1, edgecolor='black', facecolor='none')
        ax.add_patch(circle)
        
        ax.set_title(f'Samples: {num_samples}\nPi Estimate: {pi_estimate:.5f}', fontsize=10)
        ax.set_xlabel('X', fontsize=8)
        ax.set_ylabel('Y', fontsize=8)
        ax.set_aspect('equal', adjustable='box')
        ax.tick_params(axis='both', which='major', labelsize=8)

    # Create a single legend for the scatter plots
    handles, labels = scatter_axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=2, fontsize=10)
    
    # Adjust layout to make room for the legend
    plt.subplots_adjust(top=0.925)

    # Tabulate results
    df = pd.DataFrame(results, columns=['Sample Count', 'Pi Estimate'])
    df['Error'] = np.abs(np.pi - df['Pi Estimate'])
    df['Percentage Error'] = (df['Error'] / np.pi) * 100
    
    print(df)
    
    # Show the error plot
    ax = df.plot(x='Sample Count', y='Error', kind='bar', ax=bar_ax, legend=False)
    bar_ax.set_ylabel('Error', fontsize=10)
    bar_ax.set_title('Error in Pi Estimation vs Sample Count', fontsize=12)
    bar_ax.set_xticklabels(df['Sample Count'], rotation=0, fontsize=8)  # Set x-axis labels to horizontal
    
    # Adding percentage error labels on the bar chart
    for i, v in enumerate(df['Error']):
        percentage_error = df['Percentage Error'].iloc[i]
        bar_ax.text(i, v + 0.01, f"{percentage_error:.2f}%", ha='center', fontsize=8, verticalalignment='bottom')

    plt.show()

    return df

if __name__ == "__main__":
    sample_counts = [10, 100, 1000, 10000, 100000]
    df = compare_sample_counts(sample_counts)
    print(df)
