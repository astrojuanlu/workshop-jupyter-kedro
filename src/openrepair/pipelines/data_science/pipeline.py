"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.10
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_wordcloud_plot


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=create_wordcloud_plot,
            inputs=["openrepair-0_3"],
            outputs="wordcloud-plot",
            name="create_wordcloud_plot_node"
        )
    ])
