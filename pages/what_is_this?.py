import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="What is RepeatRadar?",
    page_icon="📡",
    layout="wide"
)

st.title("📡 What is RepeatRadar?")

# Introduction section
st.markdown("""
**RepeatRadar** is a Python package designed to simplify cohort analysis for businesses and data analysts. 
It provides an intuitive way to track user behavior, retention, and value generation over time.
""")

# Main content in columns
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 What is Cohort Analysis?")
    st.markdown("""
    Cohort analysis is a powerful analytical technique that groups users based on shared characteristics 
    or experiences within a defined time period. It helps answer critical business questions like:
    
    - **🔄 User Retention:** How many users come back after their first purchase?
    - **💰 Revenue Trends:** Which user groups generate the most value over time?
    - **📈 Growth Patterns:** How does user behavior change as your business evolves?
    - **🎯 Segmentation:** Which marketing campaigns bring the most loyal customers?
    """)
    
    st.header("🚀 Why Use RepeatRadar?")
    st.markdown("""
    **RepeatRadar** makes cohort analysis accessible and efficient:
    
    ✅ **Simple API:** Just a few lines of code to generate complex analyses  
    ✅ **Flexible Timeframes:** Daily, weekly, monthly, quarterly, or yearly cohorts  
    ✅ **Multiple Metrics:** Track user counts, revenue, or any custom metric  
    ✅ **Beautiful Visualizations:** Interactive heatmaps powered by Plotly  
    ✅ **Pandas Integration:** Works seamlessly with your existing data workflow  
    ✅ **Easy Installation:** Available on PyPI - just `pip install repeatradar`
    """)

with col2:
    st.header("📊 Key Features")
    
    # Feature highlights
    features = [
        {"icon": "🔢", "title": "Multiple Aggregations", "desc": "Sum, mean, count, median, nunique"},
        {"icon": "📅", "title": "Flexible Periods", "desc": "From daily to yearly analysis"},
        {"icon": "🎨", "title": "Interactive Plots", "desc": "Customizable heatmaps"},
        {"icon": "⚡", "title": "Fast Processing", "desc": "Optimized for large datasets"},
        {"icon": "📖", "title": "Well Documented", "desc": "Comprehensive guides & examples"},
        {"icon": "🔧", "title": "PyPI Available", "desc": "pip install repeatradar"}
    ]
    
    for feature in features:
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 10px; margin: 5px 0; border-radius: 5px;'>
            <strong>{feature['icon']} {feature['title']}</strong><br>
            <small>{feature['desc']}</small>
        </div>
        """, unsafe_allow_html=True)

# Example section
st.header("💡 See It In Action")

# Create sample data for demonstration
@st.cache_data
def create_sample_cohort_data():
    """Create sample cohort data for visualization"""
    periods = ['Period 0', 'Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5']
    cohorts = ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06']
    
    # Create realistic retention data
    np.random.seed(42)
    data = []
    for i, cohort in enumerate(cohorts):
        row = [cohort]
        base_retention = 100  # Start at 100%
        for j, period in enumerate(periods):
            if j == 0:
                retention = 100  # Always 100% in period 0
            else:
                # Simulate realistic retention drop-off
                decay_factor = 0.6 + (j * 0.05)  # Gets worse over time
                retention = base_retention * (decay_factor ** j)
                retention += np.random.normal(0, 5)  # Add some noise
                retention = max(0, min(100, retention))  # Keep between 0-100
            row.append(round(retention, 1))
        data.append(row)
    
    df = pd.DataFrame(data, columns=['Cohort'] + periods)
    return df

st.subheader("📊 Sample Cohort Retention Analysis")

# Create and display sample data
sample_data = create_sample_cohort_data()

# Create heatmap using plotly
fig = go.Figure(data=go.Heatmap(
    z=sample_data.iloc[:, 1:].values,
    x=sample_data.columns[1:],
    y=sample_data['Cohort'],
    colorscale='Blues',
    text=sample_data.iloc[:, 1:].values,
    texttemplate="%{text}%",
    textfont={"size": 10},
    colorbar=dict(title="Retention %")
))

fig.update_layout(
    title="User Retention by Cohort (%)",
    xaxis_title="Periods Since First Purchase",
    yaxis_title="Cohort (Month Acquired)",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**👆 This heatmap shows:** How different cohorts of users (grouped by acquisition month) 
retain over subsequent periods. Darker blue indicates higher retention rates.
""")

st.subheader("💻 Quick Start Code")
st.code("""
# Install RepeatRadar from PyPI
pip install repeatradar

# Basic usage
import pandas as pd
from repeatradar import generate_cohort_data, plot_cohort_heatmap

# Load your transaction data
df = pd.read_csv('your_data.csv')

# Generate cohort analysis
cohort_data = generate_cohort_data(
    data=df,
    date_column='purchase_date',
    user_column='customer_id',
    cohort_period='M',  # Monthly cohorts
    period_duration=30  # 30-day periods
)

# Create visualization
fig = plot_cohort_heatmap(
    cohort_data=cohort_data,
    title="Monthly User Retention",
    color_scale="Blues"
)

fig.show()
""", language="python")

# Links section
st.header("🔗 Learn More")

link_col1, link_col2, link_col3 = st.columns(3)

with link_col1:
    st.markdown("""
    **📦 Package**
    - [GitHub Repository](https://github.com/krinya/repeatradar)
    - [PyPI Package](https://pypi.org/project/repeatradar/)
    """)

with link_col2:
    st.markdown("""
    **📚 Documentation**
    - [Complete Documentation](https://krinya.github.io/repeatradar/)
    - [API Reference](https://krinya.github.io/repeatradar/)
    """)

with link_col3:
    st.markdown("""
    **👨‍💻 Author**
    - [Kristof Menyhert](https://www.linkedin.com/in/kristof-menyhert/)
    - [Dashboard Demo](https://github.com/krinya/repeatradar_demo)
    """)

# Call to action
st.success("🚀 **Ready to try RepeatRadar?** Head back to the main dashboard to explore interactive cohort analysis!")

if st.button("🏠 Back to Main Dashboard", type="primary", use_container_width=True):
    st.switch_page("Home.py")