"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.13
"""

import warnings

import matplotlib as mpl
import polars as pl
from wordcloud import WordCloud, STOPWORDS


def create_wordcloud_plot(events: pl.DataFrame):
    eol = events.filter(pl.col("repair_status") == "End of life")

    problems_gbr = list(eol.filter((pl.col("country") == "GBR"))["problem"].drop_nulls())

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        wordcloud = WordCloud(
            background_color="white",
            stopwords=set(STOPWORDS),
            collocation_threshold=1,
            colormap=mpl.pyplot.cm.Dark2,
            scale=3,
            random_state=42,
        ).generate(" ".join(problems_gbr))

    fig, ax = mpl.pyplot.subplots(figsize=(10, 8))
    ax.imshow(wordcloud)
    ax.axis("off")

    return fig
