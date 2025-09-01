import os

from dotenv import load_dotenv

from grace_query.config import getenv_list

required_envnames = ["TABLE_NAME", "DATABASE_URL"]

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