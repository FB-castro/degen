import pkgutil
import importlib


def load_modules(package):
    for module_info in pkgutil.walk_packages(
        package.__path__, package.__name__ + "."
    ):
        importlib.import_module(module_info.name)