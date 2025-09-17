# grace_query/polygons.py

"""This module handles space filtering configurations for data querying."""

# standard libraries
from typing import Optional, Dict
from collections import Counter

# third party imports
import json
from shapely import wkt as shapely_wkt
from shapely.geometry import Polygon, shape
from shapely.validation import explain_validity
import warnings

# local imports
from grace_query import constants

def _close_ring(coords):

    coord_counts = [counter[1] for counter in Counter(coords).most_common()]

    if max(coord_counts)==constants.MAX_REPCOORDS:
        counter_counts = [counts[1] for counts in Counter(coord_counts).most_common() if counts[0]==constants.MAX_REPCOORDS][0]
    elif max(coord_counts)>constants.MAX_REPCOORDS:
        raise ValueError("--polygon_str does contain more than the two (expected) occurrences of the same set of x/y coordinates.")

    if len(coords)<(constants.MAX_COORDS-1) or len(coords)>constants.MAX_COORDS or (len(coords)==constants.MAX_COORDS and max(coord_counts) < constants.MAX_REPCOORDS) or (len(coords)==(constants.MAX_COORDS-1) and max(coord_counts)>(constants.MAX_REPCOORDS-1)):
        raise ValueError("--polygon_str does not contain 5 sets of x/y coordinates locations, of which the first and the last are the same.")
    elif len(coords)==constants.MAX_COORDS and coords[0] != coords[-1]: 
        raise ValueError("--polygon_str first and last coordinates expected to be the same.")
    elif len(coords)==(constants.MAX_COORDS-1):
        warnings.warn("--polygon_str contains for 4 unique sets x/y coordinates instead of 5 sets of x/y coordinates locations, of which the first and the last are the same. The code will automatically fill the 5th missing coordinate set with the first coordinate set given in the command line.", UserWarning)
        coords = coords + [coords[0]]
    
    return coords

def parse_space(bbox=None, polygon_str=None, polygon_file=None, polygon_crs=constants.POLYGON_CRS, target_srid=constants.SRID) -> Optional[Dict]:
    if not any([bbox, polygon_str, polygon_file]):
        return None

    if bbox:
        xmin, ymin, xmax, ymax = map(float, bbox)
        poly = Polygon([(xmin,ymin),(xmax,ymin),(xmax,ymax),(xmin,ymax),(xmin,ymin)])

    elif polygon_str:
        pairs = [p.strip() for p in polygon_str.split(",")]
        coords = [(float(x), float(y)) for x, y in (pair.split() for pair in pairs)]
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
    if polygon_crs not in (constants.POLYGON_CRS,) or target_srid != constants.SRID:
        raise ValueError("For simplicity, supply EPSG:4326 geometries. (Or add pyproj/geopandas to reproject.)")

    wkt = poly.wkt
    return {"wkt": wkt, "srid": target_srid}