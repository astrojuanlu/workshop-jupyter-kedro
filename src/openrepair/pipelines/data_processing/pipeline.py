"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, node, pipeline

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
                name="consolidate_barriers_node",
            ),
        ]
    )
