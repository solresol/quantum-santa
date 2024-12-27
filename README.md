# Quantum Santa: Analyzing Santa's Visits as a Quantum Phenomenon

This project explores the concept of Santa Claus as a quantum phenomenon, analyzing his potential visits across the globe on Christmas Eve. The analysis involves generating data on estimated household visits, storing this data in a SQLite database, and visualizing it on a world map.

## Project Overview

The project consists of several scripts that work together to estimate and visualize Santa's visits:

- **methodology.sh**: Generates JSON files containing time zone and latitude data, which are used to estimate household visits.
- **make_sqlite_database.py**: Processes JSON files to populate a SQLite database (`santa_routes.db`) with estimated household visit data.
- **worldmap.py**: Visualizes the data from the database on a world map, highlighting the estimated number of households Santa visits in various regions.

## Visualization

The world map below illustrates the estimated number of households Santa visits across different time zones and latitudes. Each red dot represents a location, with the size of the dot proportional to the number of households.
## Checking the Database

Before running the visualization script, it is important to verify that the SQLite database has been populated correctly. You can use a SQLite viewer or a command-line tool to inspect the `santa_routes.db` database. Ensure that the tables contain data and that the data appears as expected.
Note that the longitudes are a little off, since we're mostly working with timezone data (Santa comes around
midnight), and then we have approximated the longitude based on the timezone.

![Santa Visits World Map](worldmap.png)

## Instructions

1. Run `methodology.sh` to generate the necessary JSON data files.
2. Execute `make_sqlite_database.py` to populate the SQLite database with the generated data.
3. Verify the database population by checking `santa_routes.db` using a SQLite viewer or command-line tool. Ensure that the data is present and correct.
4. Run `worldmap.py` to create and display the world map visualization. The map will be saved as `worldmap.png`.

### Troubleshooting

- If `worldmap.py` fails with a "No data available to plot" error, ensure that the database is populated with data.
- Check for any errors in the previous steps and ensure all dependencies are installed.

Ensure all dependencies, such as Python libraries for database handling and plotting, are installed before executing the scripts.
