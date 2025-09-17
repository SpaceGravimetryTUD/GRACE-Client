# tests/test_config.py

"""This test checks that (if) existing ./config.yml follows expected format."""

# standard libraries
import warnings

# local imports
from grace_query import constants
from grace_query.config import load_config

def test_config_yml():
  cfg = load_config(constants.CONFIG_PATH)

  if cfg == {}:
    warnings.warn("No configuration file found. If that should not be the case, please make sure to name and place the file in \"" + constants.CONFIG_PATH + "\".", UserWarning)
  else:
    for fld1 in list(constants.CONFIG_TMPLT.keys()):
       if fld1 not in list(cfg.keys()):
         warnings.warn("First level field \"" + fld1 + "\" not found in configuration file. Query will be carried out with field value flagged in the command line or assumed to be missing. If needed, add it to \"" + constants.CONFIG_PATH + "\" with the following second level fields: \"" + "\", \"".join(list(constants.CONFIG_TMPLT[fld1].keys())) + "\".", UserWarning)
       else:
         for fld2 in list(constants.CONFIG_TMPLT[fld1].keys()):
           if fld1 == "space" and fld2 == "polygon_crs" and fld2 not in list(cfg[fld1].keys()):
             warnings.warn("Second level field \"" + ".".join([fld1,fld2]) + "\" not found in configuration file. Query will be carried out with field value flagged in the command line or assumed to be \"" + constants.POLYGON_CRS + "\".", UserWarning)
           elif fld1 == "backend" and fld2 == "srid" and fld2 not in list(cfg[fld1].keys()):
             warnings.warn("Second level field \"" + ".".join([fld1,fld2]) + "\" not found in configuration file. Query will be carried out with field value flagged in the command line or assumed to be \"" + str(constants.SRID) + "\".", UserWarning)
           elif fld2 not in list(cfg[fld1].keys()):
             warnings.warn("Second level field \"" + ".".join([fld1,fld2]) + "\" not found in configuration file. Query will be carried out with field value flagged in the command line or assumed to be missing.", UserWarning)
           
    if "space" in list(cfg.keys()) and "backend" in list(cfg.keys()):
      skip_related_tests = False
      if "polygon_crs" in list(cfg["space"].keys()) and "srid" in list(cfg["backend"].keys()):
        skip_related_tests = True
        assert cfg["space"]["polygon_crs"] == f"EPSG:{cfg['backend']['srid']}", "SRID values in \"space.polygon_crs\" and \"backend.srid\". Please make sure \"space.polygon_crs\" = \"" + constants.POLYGON_CRS +  "\" and \"backend.srid\" = \"" + str(constants.SRID) + "\"."
    else:
      skip_related_tests = False

    if skip_related_tests is False:
      if "space" in list(cfg.keys()) and "polygon_crs" in list(cfg["space"].keys()):
        assert cfg["space"]["polygon_crs"] == constants.POLYGON_CRS, "For simplicity, supply EPSG:4326 geometries."
      if "backend" in list(cfg.keys()) and "srid" in list(cfg["backend"].keys()):
        assert cfg["backend"]["srid"] == constants.SRID, "For simplicity, supply EPSG:4326 geometries."