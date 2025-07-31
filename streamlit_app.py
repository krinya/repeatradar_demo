import streamlit as st
import pandas as pd
from repeatradar import generate_cohort_data, plot_cohort_heatmap
from utils.load_and_clean_sample_data import load_ecommerc_data
from utils.helper_functions import handle_generate_cohort_data

# Page configuration
st.set_page_config(
    page_title="RepeatRadar Demo Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📡 RepeatRadar - Cohort Analysis Package Demo")
st.markdown("""
Welcome to the **RepeatRadar Demo Dashboard**! 👋

This dashboard is part of my portfolio and CV, showing what you get when you work with me: a robust Python package and a professional Streamlit dashboard, both built from scratch. My aim with RepeatRadar is twofold:

1. **Help others create cohort analysis with just simple commands.**
2. **Demonstrate that I can design, build, and document both a Python package and a Streamlit dashboard like this.**

If you're curious about cohort analysis, user retention, or want to see how easy it is to analyze your own transaction data, you're in the right place!

**What does this dashboard do?**
- Lets you explore cohort analysis using sample e-commerce datasets, or you can adapt the code for your own data.
- Demonstrates the main features of the RepeatRadar package: calculating cohorts and visualizing them with beautiful, interactive heatmaps.

**What is RepeatRadar?**  
RepeatRadar is a Python package I built to make cohort analysis simple and accessible. You can install it via pip and use it in your own projects. You only need transaction data with a date and user ID column to get started. For more details and advanced usage, check out the [documentation](https://krinya.github.io/repeatradar/)."""
)

st.expander("📦 Coding part for technical people, this is how you can use the RepeatRadar package", expanded=False).markdown("""

You can easily install the package via pip:
                                                                                                                             
```python
pip install repeatradar
```

**Quick Start Example:**
```python
from repeatradar import generate_cohort_data
import pandas as pd

# Load your data (example dataset available in the repo)
ecommerce_data = pd.read_pickle("https://github.com/krinya/repeatradar/raw/refs/heads/main/examples/data/ecommerce_data_1.pkl")

# Calculate cohorts
basic_cohorts = generate_cohort_data(
    data=ecommerce_data, # Your transaction data as a pandas DataFrame
    date_column='InvoiceDateTime', # Your date column name in your data (should be datetime)
    user_column='CustomerID', # Your user ID column name in your data
    cohort_period='M', # You can set this to 'D', 'W', 'M', 'Q', or 'Y' for daily, weekly, monthly, quarterly, or yearly cohorts
    period_duration=30 # You can set this to the number of days you want to track cohorts
)
basic_vohorts
                                                                                                                             
# Visualize cohorts with a heatmap
from repeatradar import plot_cohort_heatmap
                                                                                                                             
heatmap_fig = plot_cohort_heatmap(
    cohort_data=basic_cohorts,
    title="📊 User Retention",
    color_scale="viridis",
    show_values=True,
    show_colorscale=False
)
heatmap_fig.show()
```
""")

# Load default dataset automatically
if "ecommerce_data_raw" not in st.session_state:
    with st.spinner("Loading E-commerce Data 1... Please wait, this csan take 1-2 minutes so be patient, the data is big!"):
        load_ecommerc_data("E-commerce Data 1")
    st.success("✅ E-commerce Data 1 loaded successfully!")

# Dataset Selection in main area

st.sidebar.header("🗂️ Dataset Selection")
selected_dataset = st.sidebar.selectbox(
    "Select a Dataset",
    options=["E-commerce Data 1", "E-commerce Data 2", "Upload Your Own Dataset (Coming Soon)"],
    index=0,
    help="Choose one of the sample datasets to analyze",
    key="main_dataset_selector")

if st.sidebar.button("📥 Load Selected Dataset", type="primary"):
    with st.spinner(f"Loading {selected_dataset}... Please wait, this can take 1-2 minutes so be patient, the data is big!"):
        load_ecommerc_data(selected_dataset)
    # Clear existing analysis when switching datasets
    if "cohort_data" in st.session_state:
        del st.session_state.cohort_data
    if "cohort_data_percent" in st.session_state:
        del st.session_state.cohort_data_percent
    st.success(f"✅ {selected_dataset} loaded successfully!")


# Main content area
if st.session_state.get("ecommerce_data_raw") is not None:

    st.sidebar.checkbox("Show Dataset Overview", value=False, key="dataset_overview_checkbox")
    st.sidebar.caption("This checkbox toggles the dataset overview section for the main page that provides insights into the loaded dataset.")

    if st.session_state.get("dataset_overview_checkbox"):
        # Dataset overview
        st.header("📊 Dataset Overview")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.info(f"**Current Dataset:** {selected_dataset}")
        with col2:
            st.metric("Transaction Count", f"{st.session_state.ecommerce_data_raw.shape[0]:,}")
        with col3:
            st.metric("Total Columns", f"{st.session_state.ecommerce_data_raw.shape[1]:,}")
        
        # Show raw data option
        st.checkbox(
            "👁️ Show Raw Data Preview",
            value=False,
            help="Check to display a preview of the raw dataset",
            key="show_raw_data_checkbox"
        )
        
        if st.session_state.get("show_raw_data_checkbox", False):

            with st.expander("📋 Raw Data Preview", expanded=True):
                
                col1, col2, col3 = st.columns([1, 1, 1])

                with col1:
                    st.number_input("Number of Rows to Display", 
                                    min_value=1, 
                                    max_value=st.session_state.ecommerce_data_raw.shape[0], 
                                    value=100, 
                                    step=1, 
                                    key="raw_data_row_limit")

                st.dataframe(
                    st.session_state.ecommerce_data_raw.head(st.session_state.get("raw_data_row_limit", 100)), 
                    use_container_width=True, 
                    hide_index=True
                )
                
                st.markdown(f"""
                **Dataset Information:**
                - Shape: {st.session_state.ecommerce_data_raw.shape[0]:,} rows × {st.session_state.ecommerce_data_raw.shape[1]:,} columns
                - Key columns for cohort analysis: Date, Customer ID, and optionally Value columns
                """)
        
    # Column Configuration
    st.sidebar.header("⚙️ Settings and Configuration")
    st.sidebar.caption("For cohort analysis, the minimum required columns are a **Date** column and a **Customer ID** column. Optionally, you can include a **Value** column for revenue-based analysis. " \
    "Why? Because we are analyzing returning customers and their behavior over time. The Date column tracks when transactions occur, the Customer ID identifies unique users, and the Value column (if included) allows for revenue-based cohort analysis.")
    
    # Get default column indices based on dataset - update when dataset changes
    def get_column_defaults(dataset_name, columns):
        """Get default column indices for the selected dataset"""
        if not columns:
            return 0, 0, 0
            
        if dataset_name == "E-commerce Data 1":
            date_default = columns.index("InvoiceDateTime") if "InvoiceDateTime" in columns else 0
            customer_default = columns.index("CustomerID") if "CustomerID" in columns else 0
            value_default = 0  # Default to None (first option)
        elif dataset_name == "E-commerce Data 2":
            date_default = columns.index("OrderedDateTime") if "OrderedDateTime" in columns else 0
            customer_default = columns.index("Customer_Id") if "Customer_Id" in columns else 0
            value_default = 0  # Default to None (first option)
        else:
            date_default = customer_default = value_default = 0
        return date_default, customer_default, value_default
    
    # Get defaults for current dataset
    date_default, customer_default, value_default = get_column_defaults(
        selected_dataset, 
        st.session_state.get("ecommerce_data_raw_columns", [])
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.sidebar.subheader("📅 Map Required Columns")
        date_column = st.sidebar.selectbox(
            "Date Column *",
            options=st.session_state.get("ecommerce_data_raw_columns", []),
            index=date_default,
            help="Select the column containing transaction dates",
            key=f"date_column_selector_{selected_dataset}"  # Make key unique per dataset
        )

        st.sidebar.caption("**Note:** For 'E-commerce Data 1', use 'InvoiceDateTime'. For 'E-commerce Data 2', use 'OrderedDateTime'.")
        
        customer_id_column = st.sidebar.selectbox(
            "Customer ID Column *",
            options=st.session_state.get("ecommerce_data_raw_columns", []),
            index=customer_default,
            help="Select the column containing customer identifiers",
            key=f"customer_id_column_selector_{selected_dataset}"  # Make key unique per dataset
        )

        st.sidebar.caption("**Note:** For 'E-commerce Data 1', use 'CustomerID'. For 'E-commerce Data 2', use 'Customer_Id'.")
    
    with col2:
        st.sidebar.subheader("💰 Optional Value Column")
        value_column = st.sidebar.selectbox(
            "Value Column (Optional)",
            options=st.session_state.get("ecommerce_data_raw_columns", []),
            index=value_default,
            help="Select a value column for revenue/value-based cohort analysis",
            key=f"value_column_selector_{selected_dataset}"  # Make key unique per dataset
        )
        
        # Show aggregation function only if a value column is selected
        if value_column and value_column != "None":
            aggregation_function = st.sidebar.selectbox(
                "Aggregation Function *",
                options=[None, "sum", "mean", "count", "median", "nunique"],
                index=0,  # Default to None
                help="How to aggregate values when a value column is selected",
                key="aggregation_function_selector"
            )
            st.sidebar.info("💡 Tip: 'sum' is recommended for revenue analysis, 'count' for transaction counts.")
        else:
            # Set to None when no value column is selected
            st.session_state["aggregation_function_selector"] = None
            st.sidebar.info("ℹ️ Select a value column above to enable aggregation options.")

    # Analysis Parameters in main area
    st.header("⚙️ Analysis Parameters")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # Period mapping for better display
        period_options = {
            "Daily": "D",
            "Weekly": "W", 
            "Monthly": "M",
            "Quarterly": "Q",
            "Yearly": "Y"
        }
        
        selected_period_display = st.selectbox(
            "Cohort Period",
            options=list(period_options.keys()),
            index=2,  # Default to Monthly
            help="Select the time period for grouping cohorts",
            key="cohort_period_display"
        )
        st.caption("Sets the cohort grouping period (controls table rows).")
        cohort_period = period_options[selected_period_display]
    
    with col2:
        period_duration = st.selectbox(
            "Period Duration (days)",
            options=[1, 7, 30, 90, 180, 365],
            index=2,  # Default to 30 days
            help="Number of days to track cohort behavior",
            key="period_duration_selector"
        )
        st.caption("Sets the duration for each cohort period (controls table columns).")
    
    with col3:
        # Generate Analysis Button
        can_generate = (
            st.session_state.get(f"date_column_selector_{selected_dataset}") and 
            st.session_state.get(f"customer_id_column_selector_{selected_dataset}") and
            st.session_state.get(f"date_column_selector_{selected_dataset}") != "None" and
            st.session_state.get(f"customer_id_column_selector_{selected_dataset}") != "None"
        )
        
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        generate_button = st.button(
            "🔄 Update Analysis",
            disabled=not can_generate,
            type="primary",
            help="Generate cohort analysis with current settings",
            key="generate_cohort_analysis_button"
        )
        
        if not can_generate:
            st.warning("⚠️ Select required columns")
    
    # Generate analysis when button is clicked
    if generate_button and can_generate:
        with st.spinner("Generating cohort analysis..."):
            value_col = st.session_state.get(f"value_column_selector_{selected_dataset}") if st.session_state.get(f"value_column_selector_{selected_dataset}") != "None" else None
            agg_func = st.session_state.get("aggregation_function_selector")
            
            handle_generate_cohort_data(
                data=st.session_state.get("ecommerce_data_raw"),
                date_column=st.session_state.get(f"date_column_selector_{selected_dataset}"),
                customer_id_column=st.session_state.get(f"customer_id_column_selector_{selected_dataset}"),
                cohort_period=cohort_period,
                period_duration=period_duration,
                value_column=value_col,
                aggregation_function=agg_func,
                output_format="pivot"
            )
        st.success("✅ Analysis generated successfully!")
    
    # Auto-generate on first load if columns are set
    elif can_generate and "cohort_data" not in st.session_state:
        with st.spinner("Generating initial cohort analysis..."):
            value_col = st.session_state.get(f"value_column_selector_{selected_dataset}") if st.session_state.get(f"value_column_selector_{selected_dataset}") != "None" else None
            agg_func = st.session_state.get("aggregation_function_selector")
            
            handle_generate_cohort_data(
                data=st.session_state.get("ecommerce_data_raw"),
                date_column=st.session_state.get(f"date_column_selector_{selected_dataset}"),
                customer_id_column=st.session_state.get(f"customer_id_column_selector_{selected_dataset}"),
                cohort_period=cohort_period,
                period_duration=period_duration,
                value_column=value_col,
                aggregation_function=agg_func,
                output_format="pivot"
            )

else:
    # Welcome message when no data is loaded
    st.info("Please wait while we load the default dataset...")

# Results Display
if st.session_state.get("cohort_data") is not None:
    st.header("📈 Analysis Results")
    
    # Absolute Values Heatmap with controls
    # Get current settings to determine the title
    current_value_col = st.session_state.get(f"value_column_selector_{selected_dataset}")
    current_agg_func = st.session_state.get("aggregation_function_selector")
    is_using_value_column = current_value_col and current_value_col != "None"
    
    if is_using_value_column and current_agg_func:
        heatmap_title = f"Cohort Analysis - {current_agg_func.title()} of {current_value_col}"
    else:
        heatmap_title = "Cohort Analysis - User Count"
    
    st.subheader(heatmap_title)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        color_scale_absolute = st.selectbox(
            "Color Scale",
            options=["Turbo", "Viridis", "Plasma", "Blues", "Reds", "Greens"],
            index=0,
            help="Select the color scheme for absolute values heatmap",
            key="color_scale_absolute"
        )
    with col2:
        reverse_colors_absolute = st.checkbox(
            "Reverse Colors",
            value=False,
            help="Reverse the color scale direction",
            key="reverse_colors_absolute"
        )
    with col3:
        show_colorscale_absolute = st.checkbox(
            "Show Color Scale",
            value=False,
            help="Display the color scale legend on heatmaps",
            key="show_colorscale_absolute"
        )
        
    # Generate absolute values heatmap
    final_color_scale_absolute = f"{color_scale_absolute}{'_r' if reverse_colors_absolute else ''}"
    cohort_heatmap = plot_cohort_heatmap(
        cohort_data=st.session_state.cohort_data,
        title=heatmap_title,
        color_scale=final_color_scale_absolute,
        show_colorscale=st.session_state.get("show_colorscale_absolute", True)
    )
    
    st.plotly_chart(cohort_heatmap, use_container_width=True)

    st.expander("How to interpret the heatmap? And what you can learn from them?", expanded=False).markdown("""
    **How to Read the Chart**

    **Rows (Cohorts)**  
    Each row represents a specific cohort, which is a group of users who signed up or made their first transaction in the same period (e.g., January 2024). The first column shows the initial size of that cohort.

    **Columns (Time Elapsed)**  
    The columns track the activity of each cohort over subsequent periods after they were acquired (e.g., Month 1, Month 2, etc.). Month 0 represents the initial acquisition period.

    **Cell Values (Active Users)**  
    Each cell shows the absolute count of users from a specific cohort who were active during that follow-up period. For example, the number in the "January 2024" row and "Month 3" column is the exact number of users acquired in January who came back in April.

    **Color Intensity**  
    The color provides a quick visual guide. Darker shades indicate a higher number of active users, making it easy to spot strong-performing cohorts and engagement trends.

    **What You Can Learn From This Chart?**

    This chart provides the raw data needed to assess business health and track whether your user retention is improving.

    Here are a few examples of insights you can gather:

    - **Track Acquisition:** You can see exactly how many users you acquired in a given period. For instance, "We acquired 421 users in the January 2021 cohort."
    - **Monitor Raw Retention:** You can track the raw number of users who return over time. For example, "Of the 421 users from the January cohort, 107 came back in Month 1, and 118 in Month 2."
    - **Compare Cohort Performance:** By comparing rows, you can see if newer cohorts are retaining more users than older ones.
    """)
    
    # Show data table checkbox for absolute values
    if is_using_value_column and current_agg_func:
        checkbox_label = f"Show {current_agg_func.title()} of {current_value_col} Data"
    else:
        checkbox_label = "Show User Count Data"
        
    show_absolute_data = st.checkbox(
        checkbox_label,
        value=True,
        key="show_absolute_data"
    )
    
    if show_absolute_data:
        st.session_state.cohort_data_fixed_index = st.session_state.cohort_data.copy()
        st.session_state.cohort_data_fixed_index = st.session_state.cohort_data_fixed_index.reset_index()
        # covert datetime to date
        st.session_state.cohort_data_fixed_index['cohort_period'] = st.session_state.cohort_data_fixed_index['cohort_period'].dt.date
        st.dataframe(st.session_state.cohort_data_fixed_index, use_container_width=True, hide_index=True)
    
    # Retention Rates Heatmap with controls (only show if no value column is used)
    if st.session_state.get("cohort_data_percent") is not None:
        # Check if we're using a value column
        current_value_col = st.session_state.get(f"value_column_selector_{selected_dataset}")
        is_using_value_column = current_value_col and current_value_col != "None"
        
        if not is_using_value_column:
            st.subheader("Retention Rates Heatmap (%)")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                color_scale_retention = st.selectbox(
                    "Color Scale",
                    options=["Turbo", "Viridis", "Plasma", "Blues", "Reds", "Greens"],
                    index=3,  # Default to Viridis for retention
                    help="Select the color scheme for retention rates heatmap",
                    key="color_scale_retention"
                )
            with col2:
                reverse_colors_retention = st.checkbox(
                    "Reverse Colors", 
                    value=False,
                    help="Reverse the color scale direction",
                    key="reverse_colors_retention"
                )

            with col3:
                show_colorscale_retention = st.checkbox(
                    "Show Color Scale",
                    value=False,
                    help="Display the color scale legend on heatmaps",
                    key="show_colorscale_retention"
                )
            
            # Generate retention rates heatmap
            final_color_scale_retention = f"{color_scale_retention}{'_r' if reverse_colors_retention else ''}"
            cohort_heatmap_percent = plot_cohort_heatmap(
                cohort_data=st.session_state.cohort_data_percent,
                title="Cohort Analysis - Retention Rates (%)",
                color_scale=final_color_scale_retention,
                show_colorscale=st.session_state.get("show_colorscale_retention", True)
            )
            
            st.plotly_chart(cohort_heatmap_percent, use_container_width=True)
            
            # Show data table checkbox for retention rates
            show_retention_data = st.checkbox(
                "Show Retention Rates Data",
                value=False,
                key="show_retention_data"
            )
            
            if show_retention_data:
                st.session_state.cohort_data_percent_fixed_index = st.session_state.cohort_data_percent.copy()
                st.session_state.cohort_data_percent_fixed_index = st.session_state.cohort_data_percent_fixed_index.reset_index()
                # covert datetime to date
                st.session_state.cohort_data_percent_fixed_index['cohort_period'] = st.session_state.cohort_data_percent_fixed_index['cohort_period'].dt.date
                st.dataframe(st.session_state.cohort_data_percent_fixed_index, use_container_width=True, hide_index=True)
        else:
            st.info("📊 **Note:** Retention rate analysis is only available for user count analysis (when no value column is selected). Currently showing value-based cohort analysis.")

# Footer

# Add links to sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**Useful Links:**")
st.sidebar.markdown("- <a href='https://github.com/krinya/repeatradar' target='_blank' rel='noopener'>📡 RepeatRadar Package GitHub Repo</a>", unsafe_allow_html=True)
st.sidebar.markdown("- <a href='https://krinya.github.io/repeatradar/' target='_blank' rel='noopener'>📦 RepeatRadar Documentation</a>", unsafe_allow_html=True)
st.sidebar.markdown("- <a href='https://github.com/krinya/repeatradar_demo' target='_blank' rel='noopener'>🖥️ Dashboard GitHub Repo</a>", unsafe_allow_html=True)


st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    📦 RepeatRadar Package Demo | Built with Streamlit | 
    <a href='https://krinya.github.io/repeatradar/' style='color: #666;' target='_blank' rel='noopener'>Documentation</a> |
    <a href='https://github.com/krinya/repeatradar' style='color: #666;' target='_blank' rel='noopener'>Package GitHub Repo</a> |
    <a href='https://github.com/krinya/repeatradar_demo' style='color: #666;' target='_blank' rel='noopener'>Dashboard GitHub Repo</a>
</div>
""", unsafe_allow_html=True)
