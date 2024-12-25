#!/usr/bin/env python3

import os
import json
import sqlite3
import re
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
            latitude REAL,
            longitude REAL,
            estimated_number_of_households INTEGER
        )
    ''')
    
    # Clear existing data
    cursor.execute('DELETE FROM santa_visits')
    
    # Process each file
    for filename in os.listdir(directory_path):
        if filename.startswith('population-estimate') and filename.endswith('.json'):
            try:
                # Parse coordinates from filename
                timezone_offset, longitude, latitude = parse_filename(filename)
                
                # Read and parse JSON file
                with open(os.path.join(directory_path, filename), 'r') as f:
                    data = json.load(f)
                
                # Extract households estimate
                households = data['estimated_number_of_households']
                
                # Insert into database
                cursor.execute(
                    'INSERT INTO santa_visits (latitude, longitude, estimated_number_of_households) VALUES (?, ?, ?)',
                    (latitude, longitude, households)
                )
                
            except (ValueError, json.JSONDecodeError, KeyError) as e:
                print(f"Error processing file {filename}: {str(e)}")
                continue
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    process_directory(directory_path)
    print("Database created successfully!")
