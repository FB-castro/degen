import tomllib
from pathlib import Path

def get_version():
    # Encontra o pyproject.toml na raiz do projeto
    path = Path(__file__).resolve().parent.parent / "pyproject.toml"
    
    with open(path, "rb") as f:
        data = tomllib.load(f)
        # Lê o campo [project] version
        return data["project"]["version"]

__version__ = get_version()