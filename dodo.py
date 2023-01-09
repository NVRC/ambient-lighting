import os
from pathlib import Path
from shutil import rmtree
from loguru import logger



def task_install():
  """Install project dependencies."""
  return {
    "actions": [
      "pipenv install"
    ]
  }

def task_launch():
  """Runs the API server locally."""
  return {
    "actions": [
      "python3 src/main.py --serial-device /dev/ttyUSB0"
    ],
    "task_dep": [
      "clean_pycache"
    ]
  }

def task_clean_pycache():
  """Clean pycache."""
  def rm_pycache():
    for path in Path.cwd().glob("__pycache___"):
      rmtree(path)
  return {
    "actions": [
      rm_pycache
    ]
  }

def task_check_env():
  """Checks environment variables and sets them accordingly."""
  python_path = os.getenv("PYTHONPATH")
  if python_path is None:
    python_path = ""
  src_path = Path(Path.cwd(), "src").absolute()
  split_python_path = python_path.split(":")
  if (str(src_path) not in split_python_path):
    logger.info("Adding ./src to PYTHONPATH env var.")
    new_python_path = python_path + ":" + str(src_path)
    os.putenv("PYTHONPATH", new_python_path)