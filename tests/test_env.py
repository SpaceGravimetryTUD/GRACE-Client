# tests/test_env.py

# standard libraries
import os

# third party imports
from dotenv import load_dotenv

# local imports
from grace_query import constants
from grace_query.config import getenv_list

required_envnames = [constants.TABLE_ENVNAME, constants.DB_ENVNAME]

def test_env():

  # Load environment variables
  load_dotenv()

  env_list = getenv_list()
  assert len(env_list) > 0, "No environment variables found."
  
  for envname in required_envnames:
    assert envname in env_list, "Required environment variable " + envname + " not found."

  for envname in env_list:
    envvar = os.getenv(envname)
    assert bool(envvar) is True, "Value of the environment variable " + envname + " could not be return."