import sqlite3
import logging

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap


def plot_world_map() -> pd.DataFrame:
    try:
        conn = sqlite3.connect('santa_routes.db')
        query = 'SELECT * FROM santa_visits'
        df = pd.read_sql_query(query, conn)
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return pd.DataFrame()
    finally:
        conn.close()
    
    if df.empty:
        logging.error("No data found in the database.")
        return df

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
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    df = plot_world_map()
    if df.empty:
        logging.info("Exiting script due to empty DataFrame.")
        exit(1)
    plt.savefig('worldmap.png')
    unique_longitudes = np.unique(df['longitude'])
    for lon in unique_longitudes:
        m.drawmeridians([lon], color='blue', linestyle='dotted', linewidth=0.5)
