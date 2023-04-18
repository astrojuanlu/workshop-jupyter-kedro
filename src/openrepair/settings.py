import polars as pl
from omegaconf import OmegaConf
from kedro.config import OmegaConfigLoader

if not OmegaConf.has_resolver("pl"):
    OmegaConf.register_new_resolver("pl", lambda attr: getattr(pl, attr))


CONFIG_LOADER_CLASS = OmegaConfigLoader

# See https://github.com/kedro-org/kedro/issues/2583
CONFIG_LOADER_ARGS = {
    "config_patterns": {
        "catalog": ["catalog.yml", "**/catalog.yml"],
    }
}
