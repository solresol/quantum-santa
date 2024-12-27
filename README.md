# Quantum Santa: Analyzing Santa's Visits as a Quantum Phenomenon

This project explores the concept of Santa Claus as a quantum phenomenon, analyzing his potential visits across the globe on Christmas Eve. The analysis involves generating data on estimated household visits, storing this data in a SQLite database, and visualizing it on a world map.

## Project Overview

The project consists of several scripts that work together to estimate and visualize Santa's visits:

- **methodology.sh**: Generates JSON files containing time zone and latitude data, which are used to estimate household visits.
- **make_sqlite_database.py**: Processes JSON files to populate a SQLite database (`santa_routes.db`) with estimated household visit data.
- **worldmap.py**: Visualizes the data from the database on a world map, highlighting the estimated number of households Santa visits in various regions.

## Visualization

The world map below illustrates the estimated number of households Santa visits across different time zones and latitudes. Each red dot represents a location, with the size of the dot proportional to the number of households.
**Important:** Ensure that the SQLite database (`santa_routes.db`) is populated with data before running `worldmap.py`. Without data, the visualization script will not function correctly.
Note that the longitudes are a little off, since we're mostly working with timezone data (Santa comes around
midnight), and then we have approximated the longitude based on the timezone.

![Santa Visits World Map](worldmap.png)

## Instructions

1. Run `methodology.sh` to generate the necessary JSON data files.
2. Execute `make_sqlite_database.py` to populate the SQLite database with the generated data.
3. Run `worldmap.py` to create and display the world map visualization. The map will be saved as `worldmap.png`.

Ensure all dependencies, such as Python libraries for database handling and plotting, are installed before executing the scripts.
## Troubleshooting

- If `worldmap.py` fails to retrieve data or the database is empty, ensure that `make_sqlite_database.py` has been executed successfully and that the database contains data.
- Check the console output for any error messages that might indicate issues with database connectivity or data retrieval.
- Verify that all required Python libraries are installed. You may need to install additional dependencies using `pip install -r requirements.txt` if a `requirements.txt` file is provided.
