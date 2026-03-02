from degen.tools.base import Tool
from degen.core.phases import Phase


class PythonExtractTool(Tool):

    name = "Python"
    phase = Phase.EXTRACT

    def get_env_variables(self):
        return {
            "RAW_DATA_PATH": "data/raw"
        }
    
    def get_project_structure(self):
        return {
            "src": {
                "extract.py": """import pandas as pd

                df = pd.read_csv("data/raw/sample.csv")
                print(df.head())
                """
            },
            "data/raw": {
                "sample.csv": "id,name\n1,Alice\n2,Bob\n"
            }
        }