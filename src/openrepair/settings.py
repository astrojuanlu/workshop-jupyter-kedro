import polars as pl
from kedro.config import OmegaConfigLoader

CONFIG_LOADER_CLASS = OmegaConfigLoader
CONFIG_LOADER_ARGS = {
    "custom_resolvers": {"pl": lambda obj: getattr(pl, obj)},
}
