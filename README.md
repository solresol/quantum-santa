# Quantum Santa: Analyzing Santa's Visits as a Quantum Phenomenon

This project explores the concept of Santa Claus as a quantum phenomenon, analyzing his potential visits across the globe on Christmas Eve. The analysis involves generating data on estimated household visits, storing this data in a SQLite database, and visualizing it on a world map.

## Project Overview

The project consists of several scripts that work together to estimate and visualize Santa's visits:

- **methodology.sh**: Generates JSON files containing time zone and latitude data, which are used to estimate household visits.
- **make_sqlite_database.py**: Processes JSON files to populate a SQLite database (`santa_routes.db`) with estimated household visit data.
- **worldmap.py**: Visualizes the data from the database on a world map, highlighting the estimated number of households Santa visits in various regions.

## Visualization

The world map below illustrates the estimated number of households Santa visits across different time zones and latitudes. Each red dot represents a location, with the size of the dot proportional to the number of households.
## Note on Data Availability

If the database is empty, the `worldmap.py` script will not generate a world map. Instead, it will print a message indicating the absence of data. Ensure that the database is populated with data before running the visualization script.
Note that the longitudes are a little off, since we're mostly working with timezone data (Santa comes around
midnight), and then we have approximated the longitude based on the timezone.

![Santa Visits World Map](worldmap.png)

## Instructions

1. Run `methodology.sh` to generate the necessary JSON data files.
2. Execute `make_sqlite_database.py` to populate the SQLite database with the generated data.
3. Run `worldmap.py` to create and display the world map visualization. If the database contains data, the map will be saved as `worldmap.png`. If no data is found, a message will be printed indicating the absence of data.

Ensure all dependencies, such as Python libraries for database handling and plotting, are installed before executing the scripts.
