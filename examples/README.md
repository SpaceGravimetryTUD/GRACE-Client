# GRACE Query Examples

This folder contains example files and configurations for testing the GRACE CLI Query Tool.

## Polygon Files

### `sample_area.geojson`
A simple rectangular polygon covering parts of Europe and North Africa:
- Longitude: -10° to 40°
- Latitude: 30° to 60°

### `mediterranean_region.geojson`
A more complex polygon roughly covering the Mediterranean Sea region with irregular boundaries.

## Usage Examples

### Test with polygon file
```bash
# Query data using the sample area polygon
poetry run grace query \
  --start-time "2012-03-01T00:00:00" \
  --end-time "2012-03-01T01:00:00" \
  --polygon-file examples/sample_area.geojson \
  --out-format netcdf \
  --out-path "./polygon_test_output.nc"

# Query data using the Mediterranean region polygon
poetry run grace query \
  --start-time "2012-03-01T00:00:00" \
  --end-time "2012-03-01T01:00:00" \
  --polygon-file examples/mediterranean_region.geojson \
  --out-format csv \
  --out-path "./mediterranean_test_output.csv"
```

### Test with polygon string
```bash
# Simple rectangular polygon using string format
poetry run grace query \
  --start-time "2012-03-01T00:00:00" \
  --end-time "2012-03-01T01:00:00" \
  --polygon-str "10 35, 30 35, 30 45, 10 45, 10 35" \
  --out-format parquet \
  --out-path "./polygon_string_test.parquet"
```

### Test with bounding box
```bash
# Simple bounding box query
poetry run grace query \
  --start-time "2012-03-01T00:00:00" \
  --end-time "2012-03-01T01:00:00" \
  --bbox 0 40 20 50 \
  --out-format csv \
  --out-path "./bbox_test_output.csv"
```

## Coordinate System

All polygon coordinates are in EPSG:4326 (WGS84) format:
- x = longitude (degrees East)
- y = latitude (degrees North)
