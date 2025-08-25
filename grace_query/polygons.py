# grace_client/polygons.py
from typing import Optional, Dict
from shapely.geometry import Polygon, shape
from shapely import wkt as shapely_wkt
from shapely.validation import explain_validity
import json

def _close_ring(coords):
    return coords if coords[0] == coords[-1] else coords + [coords[0]]

def parse_space(bbox=None, polygon_str=None, polygon_file=None, polygon_crs="EPSG:4326", target_srid=4326) -> Optional[Dict]:
    if not any([bbox, polygon_str, polygon_file]):
        return None

    if bbox:
        xmin, ymin, xmax, ymax = map(float, bbox)
        poly = Polygon([(xmin,ymin),(xmax,ymin),(xmax,ymax),(xmin,ymax),(xmin,ymin)])

    elif polygon_str:
        pairs = [p.strip() for p in polygon_str.split(",")]
        coords = [(float(x), float(y)) for x, y in pairs.split()]
        poly = Polygon(_close_ring(coords))

    else:  # polygon_file (GeoJSON or WKT in a .wkt)
        if polygon_file.lower().endswith(".geojson") or polygon_file.lower().endswith(".json"):
            with open(polygon_file) as f:
                gj = json.load(f)
            geom = shape(gj["features"][0]["geometry"] if "features" in gj else gj["geometry"])
            poly = Polygon(geom.exterior.coords)
        elif polygon_file.lower().endswith(".wkt"):
            with open(polygon_file) as f: 
                poly = shapely_wkt.loads(f.read().strip())
        else:
            raise ValueError("Unsupported polygon file (use GeoJSON or WKT for lightweight deps).")

    if not poly.is_valid:
        raise ValueError(f"Invalid polygon: {explain_validity(poly)}")

    # Assume polygon_crs == target_srid (to avoid heavy deps). If not, require reprojection done upstream.
    if polygon_crs not in ("EPSG:4326",) or target_srid != 4326:
        raise ValueError("For simplicity, supply EPSG:4326 geometries. (Or add pyproj/geopandas to reproject.)")

    wkt = poly.wkt
    return {"wkt": wkt, "srid": target_srid}