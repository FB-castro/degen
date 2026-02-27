import pkgutil
import importlib
from types import ModuleType
from typing import Type
from degen.core.logger import logger


def load_modules(package: ModuleType) -> None:
    """
    Importa dinamicamente todos os módulos dentro de um pacote.

    Isso garante que classes que usam registry sejam registradas automaticamente.
    """

    logger.debug(f"Autoloading package: {package.__name__}")

    for module_info in pkgutil.walk_packages(
        package.__path__,
        package.__name__ + ".",
    ):
        try:
            logger.debug(f"Importing module: {module_info.name}")
            importlib.import_module(module_info.name)
        except Exception as e:
            logger.error(
                f"Erro ao importar módulo '{module_info.name}': {e}"
            )
            raise