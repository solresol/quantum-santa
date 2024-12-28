import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_probability_histogram():
    conn = sqlite3.connect('santa_routes.db')
    query = 'SELECT longitude, latitude, estimated_number_of_households / total_households AS probability_density FROM probability_density_in_timezone ORDER BY longitude'
    df = pd.read_sql_query(query, conn)
    conn.close()

    unique_longitudes = df['longitude'].unique()
    num_longitudes = len(unique_longitudes)

    fig, axes = plt.subplots(nrows=num_longitudes, ncols=1, figsize=(10, 5 * num_longitudes), sharex=True, sharey=True)

    for ax, longitude in zip(axes, unique_longitudes):
        subset = df[df['longitude'] == longitude]
        sns.kdeplot(data=subset, x='latitude', y='probability_density', ax=ax, fill=True)
        ax.set_title(f'Longitude: {longitude}')
        ax.set_xlabel('Latitude')
        ax.set_ylabel('Probability Density')

    plt.tight_layout()
    plt.savefig('probability_histogram.png')

if __name__ == "__main__":
    plot_probability_histogram()
