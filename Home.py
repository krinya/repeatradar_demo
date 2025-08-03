"""
RepeatRadar Streamlit Demo Application

This Streamlit app demonstrates cohort analysis using the RepeatRadar package.

"""

import streamlit as st
import pandas as pd
from repeatradar import generate_cohort_data, plot_cohort_heatmap
from utils.load_and_clean_sample_data import load_ecommerce_data, load_ecommerce_data_sample1, load_ecommerce_data_sample2, get_dataset_columns
from utils.helper_functions import handle_generate_cohort_data
from utils.loading_screen import show_simple_loading

# --- Page Configuration ---
st.set_page_config(
    page_title="RepeatRadar | Cohort Analysis Demo",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Header and Introduction ---
st.title("📡 RepeatRadar: Interactive Cohort Analysis")

# Create a nice introduction section with links
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    Welcome to RepeatRadar – an interactive demo of my Python package for cohort analysis.
    
    I built RepeatRadar to solve a common problem: cohort analysis is incredibly valuable for understanding customer behavior, but it can be time-consuming to implement and difficult to adjust its settings. With RepeatRadar, you can generate comprehensive cohort insights with just a few lines of code.

    This dashboard showcases the package in action and demonstrates how I approach building complete data solutions – from developing a well-documented Python package to creating an intuitive web interface.

    **What you can explore:**

    - 🔍 **Cohort Analysis:** Track user retention and analyze customer lifetime value patterns
    - 📊 **Interactive Visualizations:** Generate publication-ready heatmaps that update in real time  
    - ⚙️ **Flexible Configuration:** Experiment with different time periods, metrics, and aggregation methods
    - 🔄 **Multiple Datasets:** Compare results across various business scenarios

    **Jump right in by picking a dataset from the sidebar and tweaking the analysis settings.**

    Everything you see here – the charts, tables, and insights – can be reproduced in your own Python environment using RepeatRadar. No complex setup required.
    """)

with col2:
    st.info("**Quick Links**")
    st.markdown("🔗 [RepeatRadar Package](https://github.com/krinya/repeatradar)")
    st.markdown("📚 [Documentation](https://krinya.github.io/repeatradar/)")
    st.markdown("👤 [My LinkedIn](https://www.linkedin.com/in/kristof-menyhert/)")
    st.markdown("💻 [Dashboard Code](https://github.com/krinya/repeatradar_demo)")

# --- Quickstart Guide ---
with st.expander("🚀 Getting Started with RepeatRadar in Python", expanded=False):
    st.markdown("""
    You can easily install the package using pip:
    ```bash
    pip install repeatradar
    ```
    
    RepeatRadar is available on PyPI and can be installed in any Python environment.

    **Example Usage:**
    ```python
    import pandas as pd
    from repeatradar import generate_cohort_data, plot_cohort_heatmap

    # 1. Load your transactional data
    # This example uses a sample dataset from the repository
    url = "https://github.com/krinya/repeatradar/raw/main/examples/data/ecommerce_data_1.pkl"
    ecommerce_data = pd.read_pickle(url)

    # 2. Generate cohort data
    # Specify your data, date column, user ID, and desired cohort period
    cohort_data = generate_cohort_data(
        data=ecommerce_data,
        date_column='InvoiceDateTime',
        user_column='CustomerID',
        cohort_period='M',  # 'D', 'W', 'M', 'Q', or 'Y'
        period_duration=30
    )

    # 3. Visualize the results with an interactive heatmap
    fig = plot_cohort_heatmap(
        cohort_data=cohort_data,
        title="Monthly User Retention",
        color_scale="viridis"
    )
    fig.show()
    ```
    """)

# --- Initial Data Loading with Caching ---
@st.cache_data(ttl=86400)  # Cache both datasets for 24 hours
def initialize_datasets():
    """
    Pre-load both datasets using caching for efficient access across sessions.
    This runs once every 24 hours and is shared across all users.
    """
    data1 = load_ecommerce_data_sample1()
    data2 = load_ecommerce_data_sample2()
    cols1 = get_dataset_columns("E-commerce Data 1")
    cols2 = get_dataset_columns("E-commerce Data 2")
    
    return {
        "E-commerce Data 1": {"data": data1, "columns": cols1},
        "E-commerce Data 2": {"data": data2, "columns": cols2}
    }

# Initialize cached datasets
@st.cache_data(ttl=86400)
def get_cached_datasets():
    """Get all datasets with 24-hour caching."""
    return initialize_datasets()

# Check if datasets are already cached to show loading screen if needed
if "datasets_loaded" not in st.session_state:
    # Show loading screen while datasets are being cached for the first time
    show_simple_loading()
    st.info("🔄 Loading datasets into cache... This happens once every 24 hours and is shared across all users.")
    
    # Load datasets into cache (this only happens once every 24 hours)
    cached_datasets = get_cached_datasets()
    
    # Mark as loaded to avoid showing loading screen again
    st.session_state.datasets_loaded = True
    st.rerun()
else:
    # Datasets are already cached, load them quickly
    cached_datasets = get_cached_datasets()

# --- Auto-detect columns for cohort analysis (moved here to be available for sidebar) ---
def get_auto_columns(dataset_name, columns):
    """Automatically get the date, customer, and value columns for the selected dataset."""
    if not columns:
        return None, None, None
    if dataset_name == "E-commerce Data 1":
        date_col = "InvoiceDateTime" if "InvoiceDateTime" in columns else columns[0]
        cust_col = "CustomerID" if "CustomerID" in columns else columns[0]
        value_col = "TotalPrice" if "TotalPrice" in columns else None
    elif dataset_name == "E-commerce Data 2":
        date_col = "OrderedDateTime" if "OrderedDateTime" in columns else columns[0]
        cust_col = "Customer_Id" if "Customer_Id" in columns else columns[0]
        value_col = None  # No default value column for Data 2
    else:
        date_col, cust_col, value_col = None, None, None
    return date_col, cust_col, value_col

# Get columns list for current dataset - now from cached data
def get_current_dataset_info(selected_dataset):
    """Get current dataset info from cache"""
    if selected_dataset in cached_datasets:
        return cached_datasets[selected_dataset]["columns"]
    return []

# Initialize default dataset in session state if not present
if "current_dataset" not in st.session_state:
    st.session_state.current_dataset = "E-commerce Data 1"

# Set current dataset data from cache
current_dataset_info = cached_datasets.get(st.session_state.current_dataset, {})
if current_dataset_info:
    st.session_state.ecommerce_data_raw = current_dataset_info.get("data")
    st.session_state.ecommerce_data_raw_columns = current_dataset_info.get("columns", [])

columns_list = st.session_state.get("ecommerce_data_raw_columns", [])

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Dashboard Controls")
    
    # Dataset Selection
    st.subheader("📊 Dataset Selection")
    selected_dataset = st.selectbox(
        "Choose a sample dataset:",
        options=["E-commerce Data 1", "E-commerce Data 2", "Upload Your Own (Coming Soon)"],
        index=0 if st.session_state.current_dataset == "E-commerce Data 1" else 1,
        key="main_dataset_selector",
        help="Select which dataset to analyze"
    )
    
    if st.button("📥 Load Dataset", type="primary", use_container_width=True):
        with st.spinner(f"Loading {selected_dataset}..."):
            # Update session state with cached data
            if selected_dataset in cached_datasets:
                st.session_state.current_dataset = selected_dataset
                st.session_state.ecommerce_data_raw = cached_datasets[selected_dataset]["data"]
                st.session_state.ecommerce_data_raw_columns = cached_datasets[selected_dataset]["columns"]
                
                # Clear existing analysis when switching datasets
                if "cohort_data" in st.session_state:
                    del st.session_state.cohort_data
                if "cohort_data_percent" in st.session_state:
                    del st.session_state.cohort_data_percent
                
                # Update columns list after loading new dataset
                columns_list = st.session_state.get("ecommerce_data_raw_columns", [])
                st.success(f"✅ {selected_dataset} loaded!")
            else:
                st.error("Dataset not available in cache.")
        st.rerun()  # Refresh to update the sidebar options
    
    st.caption("Once you switch datasets, press the button above to load it, and wait a bit.")
    
    
    # Display Options
    st.subheader("👁️ Display Options")
    show_dataset_overview = st.checkbox("Show Dataset Overview & Raw Data", value=False)
    
    # Advanced Options
    st.subheader("⚡ Advanced Analysis")
    st.caption("Configure value-based cohort analysis")
    
    # Restrict value column options based on dataset
    if selected_dataset == "E-commerce Data 1":
        allowed_value_cols = [col for col in ['InvoiceNo', 'Quantity', 'StockCode', 'TotalPrice'] if col in columns_list]
    elif selected_dataset == "E-commerce Data 2":
        allowed_value_cols = [col for col in ['Sales', 'Profit', 'Product'] if col in columns_list]
    else:
        allowed_value_cols = []
    
    value_column_options = [None] + allowed_value_cols
    
    value_column = st.selectbox(
        "💰 Value Column (Optional)",
        options=value_column_options,
        index=0,  # Always default to None
        help="Select a numeric column for value-based analysis (e.g., revenue)",
        key=f"value_column_selector_{selected_dataset}"
    )
    
    # Only show aggregation function if a value column is selected
    if value_column:
        st.info("💡 **Tip:** Use 'sum' for price columns or 'nunique' for count-based columns")
        aggregation_function = st.selectbox(
            "Aggregation Function",
            options=[None, "sum", "mean", "count", "median", "nunique"],
            index=0,  # Always default to None
            help="How to aggregate the value column (e.g., sum for total revenue)",
            key="aggregation_function_selector"
        )
        is_value_analysis = aggregation_function is not None
    else:
        aggregation_function = None
        is_value_analysis = False


# --- Main Content Area ---
# Data is now always available from cache, so we don't need the loading check
if st.session_state.get("ecommerce_data_raw") is not None:
    
    # --- Dataset Overview ---
    if show_dataset_overview:
        st.header("📊 Dataset Overview")
        
        # Create metrics in a nice layout
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📋 Dataset", selected_dataset)
        with col2:
            st.metric("📝 Transactions", f"{st.session_state.ecommerce_data_raw.shape[0]:,}")
        with col3:
            st.metric("📊 Columns", st.session_state.ecommerce_data_raw.shape[1])
        with col4:
            unique_customers = st.session_state.ecommerce_data_raw.iloc[:, 1].nunique() if st.session_state.ecommerce_data_raw.shape[1] > 1 else "N/A"
            st.metric("👥 Customers", f"{unique_customers:,}" if unique_customers != "N/A" else "N/A")
        
        with st.expander("📋 Raw Data Preview", expanded=True):
            rows_to_show = st.slider("Number of rows to display:", min_value=5, max_value=500, value=100, step=5)
            st.dataframe(
                st.session_state.ecommerce_data_raw.head(rows_to_show),
                use_container_width=True,
                hide_index=True
            )

    # --- Auto-detect columns for cohort analysis ---
    date_column, customer_id_column, default_value_col = get_auto_columns(selected_dataset, columns_list)

    # --- Analysis Configuration ---
    st.header("🔧 Analysis Configuration")
    
    # Create time parameters in one row
    time_col1, time_col2 = st.columns(2)
    
    with time_col1:
        period_options = {"Daily": "D", "Weekly": "W", "Monthly": "M", "Quarterly": "Q", "Yearly": "Y"}
        selected_period_display = st.selectbox(
            "Cohort Grouping Period",
            options=list(period_options.keys()),
            index=2,  # Default to Monthly
            help="How to group users into cohorts (e.g., all users who joined in the same month)"
        )
        cohort_period = period_options[selected_period_display]

    with time_col2:
        period_duration = st.selectbox(
            "Period Duration (days)",
            options=[1, 7, 30, 90, 180, 365],
            index=2,  # Default to 30 days
            help="Length of each period for tracking cohort activity"
        )

  


    # --- Generate Analysis ---
    can_generate = date_column is not None and customer_id_column is not None

    # Auto-run analysis on first load or when user clicks button
    if can_generate and "cohort_data" not in st.session_state:
        with st.spinner("🔬 Generating initial cohort analysis..."):
            handle_generate_cohort_data(
                data=st.session_state.get("ecommerce_data_raw"),
                date_column=date_column,
                customer_id_column=customer_id_column,
                cohort_period=cohort_period,
                period_duration=period_duration,
                value_column=value_column,
                aggregation_function=aggregation_function,
                output_format="pivot"
            )

    # Create action buttons - two full width columns
    button_col1, button_col2 = st.columns(2)
    
    with button_col1:
        if st.button("🔄 Generate Analysis", type="primary", disabled=not can_generate, use_container_width=True):
            with st.spinner("🔬 Calculating cohorts..."):
                handle_generate_cohort_data(
                    data=st.session_state.get("ecommerce_data_raw"),
                    date_column=date_column,
                    customer_id_column=customer_id_column,
                    cohort_period=cohort_period,
                    period_duration=period_duration,
                    value_column=value_column,
                    aggregation_function=aggregation_function,
                    output_format="pivot"
                )
            st.success("✅ Analysis updated, see the heatmap and the data bellow!")
    
    with button_col2:
        if st.button("🔄 Reset to Defaults", type="secondary", use_container_width=True):
            # Clear session state for fresh start
            if "cohort_data" in st.session_state:
                del st.session_state.cohort_data
            if "cohort_data_percent" in st.session_state:
                del st.session_state.cohort_data_percent
            st.rerun()
    
    if not can_generate:
        st.error("⚠️ Could not auto-detect required columns for cohort analysis. Please check your dataset, maybe you switched dataset and did not click the 'Load Dataset' button.")

    # --- Results Display ---
    if st.session_state.get("cohort_data") is not None:
        st.header("📈 Analysis Results")

        if is_value_analysis:
            heatmap_title = f"Cohort Analysis: {aggregation_function.title()} of {value_column}"
            main_metric_label = f"{aggregation_function.title()} of {value_column}"
        else:
            heatmap_title = "Cohort Analysis: Active Users"
            main_metric_label = "User Count"

        st.subheader(heatmap_title)
        
        # Heatmap customization in a compact form
        with st.container():
            st.markdown("**🎨 Customize Visualization**")
            viz_col1, viz_col2, viz_col3 = st.columns(3)
            with viz_col1:
                color_scale = st.selectbox("Color Scale", [
                    "Turbo", "Viridis", "Plasma", "Blues", "Reds", "Greens", 
                    "Oranges", "Purples", "Greys", "YlOrRd", "YlGnBu", "RdYlBu", 
                    "Spectral", "Coolwarm", "RdBu", "Cividis"
                ], key="color_scale")
            with viz_col2:
                reverse_colors = st.checkbox("Reverse Colors", key="reverse_colors")
            with viz_col3:
                show_colorscale = st.checkbox("Show Legend", value=False, key="show_colorscale")

        final_color_scale = f"{color_scale}{'_r' if reverse_colors else ''}"
        cohort_heatmap = plot_cohort_heatmap(
            cohort_data=st.session_state.cohort_data,
            title=heatmap_title,
            color_scale=final_color_scale,
            show_colorscale=show_colorscale
        )
        st.plotly_chart(cohort_heatmap, use_container_width=True)

        # Interpretation guide
        with st.expander("💡 How to Interpret This Heatmap"):
            st.markdown(f"""
            This heatmap visualizes how groups of users (cohorts) behave over time and provides valuable business insights:

            **📊 Understanding the Layout:**
            - **📅 Rows (Cohort Period):** Each row represents users who made their first transaction in that time period
            - **⏰ Columns (Periods Since Acquisition):** Tracks activity in subsequent periods after joining (Period 0 = acquisition period)
            - **🟦 Cell Values ({main_metric_label}):** The metric value for each cohort in each period
            - **🎨 Color Intensity:** Darker shades typically indicate higher values, making trends easy to spot
            
            **🎯 Business Value & Insights:**
            - **📈 Retention Trends:** Identify which cohorts have the best long-term retention
            - **💰 Revenue Impact:** See which user groups generate the most value over time
            - **📉 Churn Patterns:** Spot when users typically drop off (common after Period 1-2)
            - **🎯 Campaign Effectiveness:** Compare cohorts from different marketing campaigns
            - **🌱 Seasonal Effects:** Identify if certain acquisition periods perform better
            - **🔮 Forecasting:** Use historical patterns to predict future cohort behavior
            
            **📋 Actionable Insights:**
            - Focus retention efforts on periods where drop-off is highest
            - Invest more in channels that bring cohorts with better long-term value
            - Adjust pricing or product offerings based on cohort performance patterns
            """)

        # Show the main cohort data right after the heatmap
        st.subheader(f"📋 Raw Data: {main_metric_label}")
        df_display = st.session_state.cohort_data.copy().reset_index()
        df_display['cohort_period'] = df_display['cohort_period'].dt.date
        st.dataframe(df_display, use_container_width=True, hide_index=True)



        # Always show retention rate analysis
        if st.session_state.get("cohort_data_percent") is not None:
            st.subheader("📊 User Retention Rate Analysis")
            
            with st.container():
                st.markdown("**🎨 Customize Retention Visualization**")
                ret_col1, ret_col2, ret_col3 = st.columns(3)
                with ret_col1:
                    retention_color_scale = st.selectbox(
                        "Color Scale",
                        ["Turbo", "Viridis", "Plasma", "Blues", "Reds", "Greens", 
                         "Oranges", "Purples", "Greys", "YlOrRd", "YlGnBu", "RdYlBu", 
                         "Spectral", "Coolwarm", "RdBu", "Cividis"],
                        index=3,
                        key="retention_color_scale"
                    )
                with ret_col2:
                    retention_reverse_colors = st.checkbox("Reverse Colors", key="retention_reverse_colors")
                with ret_col3:
                    retention_show_colorscale = st.checkbox("Show Legend", value=False, key="retention_show_colorscale")

            retention_final_color_scale = f"{retention_color_scale}{'_r' if retention_reverse_colors else ''}"
            retention_heatmap = plot_cohort_heatmap(
                cohort_data=st.session_state.cohort_data_percent,
                title="User Retention Rate (%)",
                color_scale=retention_final_color_scale,
                show_colorscale=retention_show_colorscale
            )
            st.plotly_chart(retention_heatmap, use_container_width=True)
            
            # Show retention data right after the retention heatmap
            st.subheader("📋 Raw Data: Retention Percentages")
            df_percent_display = st.session_state.cohort_data_percent.copy().reset_index()
            df_percent_display['cohort_period'] = df_percent_display['cohort_period'].dt.date
            st.dataframe(df_percent_display, use_container_width=True, hide_index=True)

# Since data is now cached and always available, we don't need the fallback loading screen

# Update sidebar footer
with st.sidebar:
    st.markdown("---")
    st.markdown("**📌 Quick Links**")
    st.markdown("🔗 [RepeatRadar Package](https://github.com/krinya/repeatradar)")
    st.markdown("📚 [Documentation](https://krinya.github.io/repeatradar/)")
    st.markdown("👤 [My LinkedIn](https://www.linkedin.com/in/kristof-menyhert/)")
    st.markdown("💻 [Dashboard Code](https://github.com/krinya/repeatradar_demo)")
