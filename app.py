import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(page_title="yyc-compensation-disclosure", page_icon="random")
st.title("YYC Compensation Disclosure")


@st.cache
def load_df():
    yyc_data_url = "https://data.calgary.ca/resource/9bze-mzx6.json?$limit=50000"
    response = requests.get(yyc_data_url)
    df = pd.DataFrame(response.json())
    return df


st.subheader("Data Sample")
df = load_df()
st.table(df.sample(10).sort_values(["year", "position_title"]))

st.subheader("Search...")
position_title = st.text_input("Position title")
years = st.multiselect("Year", df["year"].unique())
if position_title:
    results = df[
        df["position_title"].apply(lambda t: position_title.lower() in t.lower())
    ]
    if years:
        results = results[results["year"].astype(str).isin(years)]

    if results.empty:
        st.warning("No matching entry.")
    else:
        st.dataframe(results)
        n_entry = results.shape[0]
        if n_entry > 1:
            item = "entries"
        else:
            item = "entry"
        st.success(f"{n_entry} {item} found.")

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
