from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("degen-cli")
except PackageNotFoundError:
    __version__ = "dev"
