import sqlite3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap


def plot_world_map():
    conn = sqlite3.connect('santa_routes.db')
    query = 'SELECT * FROM santa_visits'
    df = pd.read_sql_query(query, conn)
    conn.close()

    plt.figure(figsize=(12, 8))
    m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180, resolution='c')

    m.drawcoastlines()
    m.drawcountries()

    for _, row in df.iterrows():
        x, y = m(row['longitude'], row['latitude'])
        size = row['estimated_number_of_households'] / 1000000
        m.plot(x, y, 'o', markersize=size, alpha=0.5, color='red')

    unique_longitudes = np.unique(df['longitude'])
    for lon in unique_longitudes:
        m.drawmeridians([lon], color='blue', linestyle='dotted', linewidth=0.5)
    
    plt.title('Santa Visits World Map')
    plt.savefig('worldmap.png')
    plt.show()    
    return df

if __name__ == "__main__":
    df = plot_world_map()
