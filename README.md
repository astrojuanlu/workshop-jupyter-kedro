# Workshop "Refactor your Jupyter notebooks into maintainable data science code with Kedro"

> You're a Machine Learning Engineer that has just arrived to an existing project.
> The Data Scientist has given you a seemingly working notebook,
> and now it's your task to refactor it appropriately
> so that the analysis is more reproducible and the process is easier to deploy to production.
> For that, you will first verify that everything is working,
> and then convert the notebook to a Kedro project.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/astrojuanlu/workshop-jupyter-kedro/tree/workshop-kth)

What's the starting point?

- Some data
- A notebook analyzing it
- The needed requirements to get it working

## Steps

### Get started and assess the baseline

1. **Open the repository on Gitpod** by following [this link](https://gitpod.io/#https://github.com/astrojuanlu/workshop-jupyter-kedro/tree/workshop-kth).
2. **Wait for the workspace to set up** (it will need some time to build the Docker image, install the dependencies, and launch JupyterLab).
3. **Confirm that Kedro is installed** by running `kedro info` in the terminal.
4. **Confirm that the catalog is properly configured** by opening the `OpenRepair quick EDA.ipynb` notebook in JupyterLab and running it top to bottom.

Success! 🎉 You can now start working on the project for real. The fun starts now.
### Create a data processing pipeline

1. Create a new data processing pipeline by running `kedro pipeline create data_processing`.
2. Turn the code that joins the two `DataFrames` and cleans the result into Python functions by adding this to `src/openrepair/pipelines/data_processing/nodes.py`:

```python
# src/openrepair/pipelines/data_processing/nodes.py

import polars as pl


def join_events_categories(events: pl.DataFrame, categories: pl.DataFrame):
    df_clean = events.select(pl.all().exclude("product_category")).join(
        categories, on="product_category_id"
    )
    return df_clean


def consolidate_barriers(df_clean: pl.DataFrame):
    return df_clean.with_columns(
        pl.col("repair_barrier_if_end_of_life").map_dict(
            {"Item too worn out": "Product too worn out"},
            default=pl.col("repair_barrier_if_end_of_life"),
        )
    )
```

3. Craft the pipeline by modifying `src/openrepair/pipelines/data_processing/pipeline.py` as follows:

```python
# src/openrepair/pipelines/data_processing/pipeline.py

from .nodes import join_events_categories, consolidate_barriers


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=join_events_categories,
                inputs=["openrepair-0_3-events-raw", "openrepair-0_3-categories"],
                outputs="openrepair-0_3-combined",
                name="join_events_categories_node",
            ),
            node(
                func=consolidate_barriers,
                inputs="openrepair-0_3-combined",
                outputs="openrepair-0_3",
                name="consolidate_barriers",
            ),
        ]
    )
```

4. Register the pipeline by creating a `src/openrepair/pipeline_registry.py` module with these contents:

```python
# src/openrepair/pipeline_registry.py

"""Project pipelines."""
from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()
    pipelines["__default__"] = sum(pipelines.values())
    return pipelines
```

Verify that `kedro registry list` shows a `__default__` pipeline as well as the data processing one.

5. Add `kedro-viz` to `requirements.txt` and install it. After that, run `kedro viz`, and wait for the web interface to open.

Success! 🎉 You just created your first Kedro pipeline and now you can see it as a beautiful directed acyclic graph (DAG).
Now it's time to actually save those intermediate results to disk.

![Data processing pipeline in Kedro Viz](data-processing-kedro-viz.png)

### Open ended: Refine your pipeline and visualize artifacts

1. Register the intermediate datasets used in the data processing nodes by adding these contents to `conf/base/catalog.yml`:

```yaml
# conf/base/catalog.yml

openrepair-0_3-combined:
  type: polars.CSVDataSet
  filepath: data/02_intermediate/openrepairdata_v0.3_combined.csv
  load_args:
    dtypes:
      product_age: ${pl:Float64}
      group_identifier: ${pl:Utf8}
    try_parse_dates: true

openrepair-0_3:
  type: polars.CSVDataSet
  filepath: data/03_primary/openrepairdata_v0.3_clean.csv
  load_args:
    dtypes:
      product_age: ${pl:Float64}
      group_identifier: ${pl:Utf8}
    try_parse_dates: true
```

2. Run the pipeline by running `kedro run`. Verify that a `data/03_primary/openrepairdata_v0.3_clean.csv` file appeared on the filesystem.
3. Create a `notebooks` directory, and move the EDA notebook there.
4. Add a new `notebooks/data-science.ipynb` notebook and, using the `kedro.ipython` extension and the `catalog`, load the `openrepair-0_3` and extract insights from it. For example, here is a plot of the repair statuses by year:

![Repair statuses by year](repair-status.png)

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
