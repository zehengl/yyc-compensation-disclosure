import math

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(page_title="yyc-compensation-disclosure", page_icon="random")
_, center, _ = st.columns([2, 1, 2])
with center:
    st.image(
        "https://cdn0.iconfinder.com/data/icons/business-startup-10/50/44-512.png",
        use_column_width=True,
    )
st.title("YYC Compensation Disclosure")
st.caption("A Streamlit app to visualize City of Calgary's compensation disclosure")


@st.cache
def load_df():
    yyc_data_url = "https://data.calgary.ca/resource/9bze-mzx6.json?$limit=50000"
    response = requests.get(yyc_data_url)
    df = pd.DataFrame(response.json())
    df["minimum_annual_base_rate"] = df["minimum_annual_base_rate"].astype(int)
    df["maximum_annual_base_rate"] = df["maximum_annual_base_rate"].astype(int)
    return df


st.subheader("Data Sample")
df = load_df()
st.session_state["df"] = df
st.table(df.sample(10).sort_values(["year", "position_title"]))

st.subheader("# of Positions over time")
fig = px.bar(
    df.groupby("year").count().reset_index(),
    x="year",
    y="position_title",
    color="year",
)
fig

st.subheader("History of Positions")
fig = px.histogram(
    df.groupby("position_title").count().reset_index(),
    x="year",
    color="year",
)
fig


def rate_hist(df, col):
    n_cols = 2
    n_rows = math.ceil(df["year"].nunique() / n_cols)
    years = df["year"].unique()
    fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=years)
    for index, year in enumerate(years):
        fig.add_trace(
            go.Histogram(
                x=df[df["year"] == year][col],
                name=year,
            ),
            row=index // n_cols + 1,
            col=index % n_cols + 1,
        )
    title = " ".join([w.capitalize() for w in col.split("_")])
    fig.update_layout(height=800, title=title, showlegend=False)
    return fig


st.subheader("Base Rates")
fig = rate_hist(df, "minimum_annual_base_rate")
fig

fig = rate_hist(df, "maximum_annual_base_rate")
fig
