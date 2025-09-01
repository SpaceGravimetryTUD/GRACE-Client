# grace_query/config.py
from dataclasses import dataclass
from datetime import datetime
import yaml
from dotenv import load_dotenv
import os               # Library for system operations, like reading environment variables


required_columns = ["id","datetime","latitude_A","longitude_A","postfit","up_combined"]

# Load environment variables
load_dotenv()

def getenv_list() -> list:
    f = open('.env','r')
    env_list=list(filter(None,[ s.split('=')[0].split('#')[0] for s in f.read().split('\n')]))
    f.close()
    return env_list

def showenv(env_list: list = getenv_list()):
  print('Loaded the following env vars from .env:')
  for f in env_list:
      print(f'{f} = {os.getenv(f)}')

def getenv(envname: str) -> str:
  envvar = os.getenv(envname)
  if not envvar:
      raise EnvironmentError("{name} not found in environment variables.")
  return envvar

@dataclass
class TimeCfg:  start:str|None=None; end:str|None=None
@dataclass
class SpaceCfg: bbox:list|None=None; polygon_str:str|None=None; polygon_file:str|None=None; polygon_crs:str="EPSG:4326"
@dataclass
class ExportCfg: format:str="netcdf"; out:str="./query_output.nc"; strict_cf:bool=False; options:dict=None
@dataclass
class ProbleCfg: cadence_seconds:int=5; missing_threshold_pct:float=2.0; report_path:str|None=None
@dataclass
class Backend:   url:str|None=None; table:str|None=None; srid:int=4326
@dataclass
class Cfg:
    time:TimeCfg; space:SpaceCfg; columns:list; export:ExportCfg; problematic:ProbleCfg|None; backend:Backend

def load_config(path:str|None)->dict:
    if not path: return {}
    try:
        with open(path) as f: return yaml.safe_load(f)
    except:
        return {}

def merge_cli_over_config(cfg:dict, args)->Cfg:
    # very light merging; you can expand validations
    time = TimeCfg(args.start_time or cfg.get("time",{}).get("start"),
                   args.end_time   or cfg.get("time",{}).get("end"))
    
    space_dict = cfg.get("space",{})
    space = SpaceCfg(
        bbox=[float(x) for x in args.bbox] if args.bbox else space_dict.get("bbox"),
        polygon_str=args.polygon_str or space_dict.get("polygon_str"),
        polygon_file=args.polygon_file or space_dict.get("polygon_file"),
        polygon_crs=args.polygon_crs or space_dict.get("polygon_crs","EPSG:4326")
    )

    export_dict = cfg.get("export",{})
    export = ExportCfg(
        format=(args.out_format or export_dict.get("format","netcdf")),
        out=(args.out_path or export_dict.get("path","./query_output.nc")),
        strict_cf=bool(args.strict_cf or export_dict.get("strict_cf",False)),
        options=export_dict.get("netcdf",{}) if (args.out_format or export_dict.get("format","netcdf"))=="netcdf" else {}
    )
    
    
    prob_dict = cfg.get("problematic_months")
    problematic = None

    
    if prob_dict or args.problematic_report:
        problematic = ProbleCfg(
            cadence_seconds=int((prob_dict or {}).get("cadence_seconds",5)),
            missing_threshold_pct=float((prob_dict or {}).get("missing_threshold_pct",2.0)),
            report_path=args.problematic_report or (prob_dict or {}).get("report_path")
        )
        
    
    backend_dict = cfg.get("backend",{})
    backend = Backend(
        url=args.db_url or backend_dict.get("url"),
        table=args.table or backend_dict.get("table"),
        srid=int(backend_dict.get("srid",4326))
    )

    columns = (args.columns.split(",") if args.columns else cfg.get("columns")) or required_columns
    
    return Cfg(time=time, space=space, columns=columns, export=export, problematic=problematic, backend=backend)