import pandas as pd
from sodapy import Socrata
import geopandas as gpd
from shapely.geometry import Point

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
# client = Socrata("data.cityofnewyork.us", None)

app_token = ""

# Example authenticated client (needed for non-public datasets):

client = Socrata("data.cityofnewyork.us", app_token)

# Define the date range　5/8は水曜日
start_date = "2013-05-08T04:00:00.000"
end_date = "2013-05-09T03:59:59.000"

# Load the shapefile of Manhattan or any GeoJSON file containing Manhattan's geometry
manhattan_gdf = gpd.read_file("../data/Boundaries_manha.geojson")
# マンハッタン島の一つのジオメトリしか含まれていないため
manhattan_geometry = manhattan_gdf.geometry.iloc[0]

# First 2000 results filtered by date range, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("t7ny-aygi", limit=200,
                     where=f"tpep_pickup_datetime >= '{start_date}' AND tpep_pickup_datetime <= '{end_date}'")

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

results_df = results_df[
    results_df.apply(
        lambda row: (
            Point(float(row["pickup_longitude"]), float(row["pickup_latitude"])).within(manhattan_geometry) and
            Point(float(row["dropoff_longitude"]), float(row["dropoff_latitude"])).within(manhattan_geometry)
        ),
        axis=1
    )
]

results_df.to_csv("../data/NYCTaxi0.csv", encoding='utf-8', index=None)
