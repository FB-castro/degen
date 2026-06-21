from degen.tools.base import Tool
from degen.core.phases import Phase


class PythonExtractTool(Tool):

    name = "Python"
    phase = Phase.EXTRACT

    def get_python_dependencies(self):
        return [
            "pandas>=2.1.0",
            "python-dotenv>=1.0.0",
            "requests>=2.31.0",
        ]

    def get_env_variables(self):
        return {
            "RAW_DATA_PATH": "data/raw",
        }

    def get_project_structure(self):
        return {
            "src": {
                "extract.py": '''\
import os
import logging
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

RAW_DATA_PATH = Path(os.getenv("RAW_DATA_PATH", "data/raw"))


def extract() -> pd.DataFrame:
    logger.info(f"Reading source data from {RAW_DATA_PATH}")
    df = pd.read_csv(RAW_DATA_PATH / "sample.csv")
    logger.info(f"Extracted {len(df)} rows")
    return df


if __name__ == "__main__":
    df = extract()
    print(df.head())
''',
            },
            "data/raw": {
                "sample.csv": "id,name,value\n1,Alice,100\n2,Bob,200\n3,Carol,300\n",
            },
        }

    def get_makefile_targets(self):
        return {
            "run": ["$(VENV)/bin/python src/extract.py"],
        }
