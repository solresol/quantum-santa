import sqlite3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap


def plot_world_map() -> pd.DataFrame:
    conn = sqlite3.connect('santa_routes.db')
    query = 'SELECT * FROM santa_visits'
    try:
        df = pd.read_sql_query(query, conn)
        if df.empty:
            raise ValueError("The query returned no results. The DataFrame is empty.")
    except Exception as e:
        conn.close()
        raise RuntimeError(f"Failed to retrieve data from the database: {e}")
    conn.close()

    plt.figure(figsize=(12, 8))
    m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180, resolution='c')

    m.drawcoastlines()
    m.drawcountries()

    for _, row in df.iterrows():
        x, y = m(row['longitude'], row['latitude'])
        size = row['estimated_number_of_households'] / 1000000
        m.plot(x, y, 'o', markersize=size, alpha=0.5, color='red')

    plt.title('Santa Visits World Map')
    plt.show()

if __name__ == "__main__":
    try:
        df = plot_world_map()
        if df is None or df.empty:
            raise RuntimeError("No data available to plot. Please check the database content.")
        plt.savefig('worldmap.png')
        unique_longitudes = np.unique(df['longitude'])
        for lon in unique_longitudes:
            m.drawmeridians([lon], color='blue', linestyle='dotted', linewidth=0.5)
    except RuntimeError as e:
        print(e)
        exit(1)
