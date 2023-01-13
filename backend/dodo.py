import os
from pathlib import Path
from shutil import rmtree
from loguru import logger


def task_install():
    """Install project dependencies."""
    return {"actions": ["pipenv install"]}


def task_launch():
    """Runs the API server locally."""
    return {
        "actions": ["python src/main.py"],
        "task_dep": ["clean_pycache", "lint"],
    }


def init_build_dirs():
    build_path = Path(Path.cwd(), "build")
    build_path.mkdir(exist_ok=True)


def task_init_build_dir():
    """Create build directories."""
    return {
            "actions": [init_build_dirs],
            "clean": True,
            "targets": ["build"],
        }

def task_lint():
    """Lint python code."""
    relative_lint_path = "build/lint.json"
    return {
        "targets": [relative_lint_path],
        "actions": [
            "python -m black src",
            "python -m pylint src --rcfile .pylintrc --load-plugins pylint_pydantic --extension-pkg-whitelist='pydantic' --output-format=json:{},colorized".format(
                relative_lint_path
            ),
        ],
        "task_dep": ["init_build_dir"],
        "clean": True
    }

def task_test():
    """Run tests."""
    return {
        "task_dep": ["lint"],
        "targets": ["build/cov.xml", ".coverage"],
        "actions": [
            "pytest --cov-report xml:build/cov.xml src"
        ],
        "clean": True
    }

def task_clean_pycache():
    """Clean pycache."""
    def rm_pycache():
        for path in Path.cwd().glob("__pycache__"):
            rmtree(path)

    return {
        "actions": [rm_pycache],
    }


def task_check_env():
    """Checks environment variables and sets them accordingly."""
    python_path = os.getenv("PYTHONPATH")
    if python_path is None:
        python_path = ""
    src_path = Path(Path.cwd(), "src").absolute()
    split_python_path = python_path.split(":")
    if str(src_path) not in split_python_path:
        logger.info("Adding ./src to PYTHONPATH env var.")
        new_python_path = python_path + ":" + str(src_path)
        os.putenv("PYTHONPATH", new_python_path)
