# ファイルをダウンロード
wget -P data/ http://download.geofabrik.de/north-america/us/new-york-latest.osm.pbf

osmosis --read-pbf data/new-york-latest.osm.pbf --bounding-polygon file=data/Boundaries_manha.poly --tf accept-ways highway=primary,secondary,tertiary,residential,unclassified,road,living_street,trunk --used-node --write-pbf data/manhattan.osm.pbf

