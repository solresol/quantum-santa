#!/usr/bin/env python3

import os
import json
import sqlite3
import re
import logging
from typing import Tuple

def parse_filename(filename: str) -> Tuple[float, float, float]:
    """Extract timezone offset, calculated longitude, and latitude from filename."""
    # Using regex to extract the coordinates
    pattern = r'population-estimate,([^,]+),([^.]+)\.json'
    match = re.match(pattern, filename)
    if not match:
        raise ValueError(f"Invalid filename format: {filename}")
    
    timezone_offset = float(match.group(1))
    calculated_longitude = timezone_offset * 15
    latitude = float(match.group(2))
    return timezone_offset, calculated_longitude, latitude

def process_directory(directory_path: str, db_path: str = "santa_routes.db"):
    """
    Process all population-estimate*.json files in the directory and store data in SQLite.
    
    Args:
        directory_path: Path to directory containing the JSON files
        db_path: Path where the SQLite database should be created
    """
    # Create database and table
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS santa_visits (
            timezone_offset REAL,
            latitude REAL,
            longitude REAL,
            estimated_number_of_households INTEGER
        )
    ''')
    
    # Clear existing data
    cursor.execute('DELETE FROM santa_visits')
    
    # Process each file
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    for filename in os.listdir(directory_path):
        if filename.startswith('population-estimate') and filename.endswith('.json'):
            try:
                # Parse coordinates from filename
                timezone_offset, longitude, latitude = parse_filename(filename)
                
                # Read and parse JSON file
                with open(os.path.join(directory_path, filename), 'r') as f:
                    data = json.load(f)
                
                # Verify JSON keys
                if 'estimated_number_of_households' not in data:
                    raise KeyError("Missing key 'estimated_number_of_households' in JSON data.")
                
                # Extract households estimate
                households = data['estimated_number_of_households']
                
                # Insert into database
                cursor.execute(
                    'INSERT INTO santa_visits (timezone_offset, latitude, longitude, estimated_number_of_households) VALUES (?, ?, ?, ?)',
                    (timezone_offset, latitude, longitude, households)
                )
                logging.info(f"Successfully inserted data from {filename}.")
                
            except (ValueError, json.JSONDecodeError, KeyError) as e:
                logging.error(f"Error processing file {filename}: {str(e)}")
                continue
    
    # Commit changes and close connection
    try:
        conn.commit()
        logging.info("All changes committed to the database.")
    except sqlite3.Error as e:
        logging.error(f"Error committing changes to the database: {e}")
    finally:
        conn.close()
        logging.info("Database connection closed.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    process_directory(directory_path)
    print("Database created successfully!")
    try:
        logging.info("Connecting to the database and preparing the table.")
        # Create database and table
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS santa_visits (
                timezone_offset REAL,
                latitude REAL,
                longitude REAL,
                estimated_number_of_households INTEGER
            )
        ''')
        
        # Clear existing data
        cursor.execute('DELETE FROM santa_visits')
        logging.info("Database connected and table prepared.")
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")
    try:
        logging.info("Connecting to the database and preparing the table.")
        # Create database and table
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS santa_visits (
                timezone_offset REAL,
                latitude REAL,
                longitude REAL,
                estimated_number_of_households INTEGER
            )
        ''')
        
        # Clear existing data
        cursor.execute('DELETE FROM santa_visits')
        logging.info("Database connected and table prepared.")
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return
                logging.info(f"Successfully inserted data from {filename}.")
                
            except (ValueError, json.JSONDecodeError, KeyError) as e:
                logging.error(f"Error processing file {filename}: {str(e)}")
                continue
    
    # Commit changes and close connection
    try:
        conn.commit()
        logging.info("All changes committed to the database.")
    except sqlite3.Error as e:
        logging.error(f"Error committing changes to the database: {e}")
    finally:
        conn.close()
        logging.info("Database connection closed.")
