import streamlit as st


df = st.session_state["df"]

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
