import streamlit as st
from utils.load_and_clean_sample_data import load_ecommerc_data
from repeatradar import generate_cohort_data

st.title("🎈 RepeatRadar - A package for creating cohort analysis")
st.subheader(
    "This dashboard is demonstrating the use of RepeatRadar that I developed and currently in an early state."
)

st.selectbox(
    "Select a Dataset",
    placeholder="Choose a dataset to analyze",
    options=["E-commerce Data 1", "E-commerce Data 2"],
    index=None,
    key="main_dataset_selector"
)

st.button(
    "Load Data",
    key="load_data_button",
    help="Click to load the selected dataset",
    on_click=load_ecommerc_data,
    kwargs={"selected_dataset": st.session_state.get("main_dataset_selector", "E-commerce Data 1")}
)

st.checkbox(
    "Show Raw Data",
    value=True,
    key="show_raw_data_checkbox",
    help="Check to display the raw data of the selected dataset"
)

if st.session_state.get("ecommerce_data_raw") is not None:
    st.dataframe(st.session_state.ecommerce_data_raw, use_container_width=True, hide_index=True)
    st.markdown("Shape of the DataFrame: " + str(st.session_state.ecommerce_data_raw.shape))
    st.markdown("From this raw data we actually need only the columns that are relevant for the cohort analysis example.")
    st.markdown("These columns are: `CustomerID`, `InvoiceDate`, `TotalPrice`.")