import streamlit as st
import pandas as pd

# Create here a sample DataFrame
data = {
    "Column 1": [1, 2, 3, 4, 5],
    "Column 2": ["A", "B", "C", "D", "E"],
    "Column 3": [10.5, 20.5, 30.5, 40.5, 50.5]
}
df = pd.DataFrame(data)

# Streamlit app code
st.title("🎈 Sample Page")
st.write("This is a sample Streamlit app.")
st.dataframe(df)