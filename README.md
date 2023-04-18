# Workshop "Analyze your data at the speed of light with Polars and Kedro"

> You're a Machine Learning Engineer that has just arrived to an existing project.
> The Data Scientist has given you a seemingly working notebook,
> and now it's your task to refactor it appropriately
> so that the analysis is more reproducible and the process is easier to deploy to production.
> For that, you will first verify that everything is working,
> and then convert the notebook to a Kedro project.

What's the starting point?

- Some data
- A notebook analyzing it
- The needed requirements to get it working

## Steps

### Get started and assess the baseline

1. **Download the data**. Fill the form at https://openrepair.org/open-data/downloads/ or use [the direct URL](https://openrepair.org/wp-content/uploads/2023/02/OpenRepairData_v0.3_aggregate_202210.zip). Extract all the files and place them under the `data/` directory.
2. **Setup your development environment**. Create a conda/mamba environment called `repair310` with Python 3.10, activate it, and install the dependencies from `requirements.txt` using pip.
3. **Verify that everything works**. Run the notebook top to bottom. How many rows does the repair events dataset have?

Success! 🎉 You can now start working on the project for real. The fun starts now.
### Refactor data loading using the catalog

1. Add `kedro~=0.18.7` to `requirements.txt` and install it. Verify that `kedro info` works.
2. You will need a "bleeding edge" version of `kedro-datasets` to proceed. Add `kedro-datasets[pandas.CSVDataSet,polars.CSVDataSet] @ git+https://github.com/kedro-org/kedro-plugins@3b42fae#subdirectory=kedro-datasets` to `requirements.txt`, and install it.
3. Create a `data/01_raw` directory, and move all the data files there.
4. Create `conf/base` and `conf/local` directories, as well as a `conf/base/catalog.yml` file, and register the events dataset as follows:

```yaml
# conf/base/catalog.yml

openrepair-0_3-events-raw:
  type: polars.CSVDataSet
  filepath: data/01_raw/OpenRepairData_v0.3_aggregate_202210.csv
  load_args:
    dtypes:
      product_age: ${pl_Float64}
      group_identifier: ${pl_Utf8}
    try_parse_dates: true
```

4. Add the following code snippet at the beginning of the notebook to use the Kedro catalog for data loading:

```python
from kedro.config import TemplatedConfigLoader
from kedro.io import DataCatalog

catalog_variables = {
    "pl_Float64": pl.Float64,
    "pl_Utf8": pl.Utf8,
}

conf_loader = TemplatedConfigLoader("conf", globals_dict=catalog_variables)
conf_catalog = conf_loader.get("catalog.yml")
catalog = DataCatalog.from_config(conf_catalog)
```

5. Finally, replace the `df = pl.read_csv(...)` call with `df = catalog.load("openrepair-0_3-events-raw")`. Verify that everything works.
6. Do the same with the categories `DataFrame`: register it in the `conf/base/catalog.yml` and replace the `categories = pl.read_csv(...)` with the appropriate `categories = catalog.load("...")` call.

Success! 🎉 After adding some Kedro boilerplate, you decoupled the Jupyter notebook from the actual file locations and loading options.
In addition, you prepared the project structure to accommodate intermediate datasets.
There is still some work to do, but you are getting there.

## Resources

- Kedro documentation: https://docs.kedro.org/

## Cheatsheet

```bash
# Create a mamba environment using micromamba (you can replace micromamba with mamba or conda)
# Replace $VARIABLES with actual parameters or give them a value
$ micromamba create -n $ENV_NAME python=$PY_VERSION -c conda-forge

# Activate a mamba environment using micromamba (you can replace micromamba with mamba or conda)
$ micromamba activate $NEV_NAME

# Install dependencies from `requirements.txt` file using pip
$ pip install -r requirements.txt
```
