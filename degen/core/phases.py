from enum import Enum


class Phase(str, Enum):
    EXTRACT = "extract"
    TRANSFORM = "transform"
    STORE = "store"
    ORCHESTRATE = "orchestrate"
    SERVE = "serve"