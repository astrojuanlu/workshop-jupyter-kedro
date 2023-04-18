"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.10
"""

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
