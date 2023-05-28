import h3
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon

# Manhattanの中心部の緯度と経度
lat = 40.7831
lng = -73.9712

# H3 resolution level (0-15), 数字が大きいほどグリッドのサイズが小さくなります、レベル8の時エッジの長さは約531m
resolution = 8

# マンハッタンの中心部を含むヘキサゴンを取得
hex_center = h3.geo_to_h3(lat, lng, resolution)

# マンハッタンの中心部を中心としたヘキサゴンのグリッドを取得
hexagons = h3.k_ring(hex_center, 20)

# ヘキサゴンをシェイプファイルに変換
def hex_to_geom(h):
    geo_json = h3.h3_to_geo_boundary(h, geo_json=True)
    return Polygon(geo_json)

# ヘキサゴンの中心座標を取得
def hex_to_center_lat(h):
    lat, lng = h3.h3_to_geo(h)
    return lat

def hex_to_center_lng(h):
    lat, lng = h3.h3_to_geo(h)
    return lng

# Load the shapefile of Manhattan or any GeoJSON file containing Manhattan's geometry
manhattan_gdf = gpd.read_file("data/Boundaries_manha.geojson")
manhattan_geometry = manhattan_gdf.geometry.iloc[0]

df = pd.DataFrame(hexagons, columns=['hex_id'])
df['geometry'] = df['hex_id'].apply(hex_to_geom)
df['center_lat'] = df['hex_id'].apply(hex_to_center_lat)
df['center_lng'] = df['hex_id'].apply(hex_to_center_lng)

# Create a new geometry for center points
df['center_point'] = df.apply(lambda row: Point(row['center_lng'], row['center_lat']), axis=1)

# Keep only those center points that are within the Manhattan geometry
df = df[df['center_point'].apply(lambda point: point.within(manhattan_geometry))]

# Drop the center_point column as we don't need it anymore
df.drop(columns=['center_point'], inplace=True)

gdf = gpd.GeoDataFrame(df, geometry='geometry')

# ファイルに書き出す
gdf.to_file("data/NYCHex0.shp")

# ファイルに書き出す（CSV）
df.to_csv("data/NYCHex0.csv", index=False)