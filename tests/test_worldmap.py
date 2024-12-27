import sqlite3

import pandas as pd
import pytest
from worldmap import plot_world_map

TEST_DB_PATH = 'test_santa_routes.db'

def setup_module(module):
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS santa_visits (
            timezone_offset REAL,
            latitude REAL,
            longitude REAL,
            estimated_number_of_households INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def teardown_module(module):
    import os
    os.remove(TEST_DB_PATH)

def test_data_retrieval():
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM santa_visits')
    cursor.execute('''
        INSERT INTO santa_visits (timezone_offset, latitude, longitude, estimated_number_of_households)
        VALUES (1.0, 45.0, 90.0, 1000)
    ''')
    conn.commit()
    conn.close()
    
    df = plot_world_map()
    assert not df.empty
    assert len(df) == 1
    assert df.iloc[0]['latitude'] == 45.0
    assert df.iloc[0]['longitude'] == 90.0
    assert df.iloc[0]['estimated_number_of_households'] == 1000

def test_empty_database():
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM santa_visits')
    conn.commit()
    conn.close()
    
    with pytest.raises(ValueError, match="The query returned no results. The DataFrame is empty."):
        plot_world_map()

def test_missing_columns():
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM santa_visits')
    cursor.execute('''
        INSERT INTO santa_visits (timezone_offset, latitude, longitude)
        VALUES (1.0, 45.0, 90.0)
    ''')
    conn.commit()
    conn.close()
    
    with pytest.raises(ValueError, match="DataFrame does not contain the required columns."):
        plot_world_map()

def test_incorrect_data_format():
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM santa_visits')
    cursor.execute('''
        INSERT INTO santa_visits (timezone_offset, latitude, longitude, estimated_number_of_households)
        VALUES ('invalid', 'invalid', 'invalid', 'invalid')
    ''')
    conn.commit()
    conn.close()
    
    with pytest.raises(RuntimeError, match="Failed to retrieve data from the database:"):
        plot_world_map()
