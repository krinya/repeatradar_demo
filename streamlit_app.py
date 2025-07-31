import streamlit as st
import pandas as pd
from repeatradar import generate_cohort_data, plot_cohort_heatmap
from utils.load_and_clean_sample_data import load_ecommerc_data
from utils.helper_functions import handle_generate_cohort_data

# --- Page Configuration ---
st.set_page_config(
    page_title="RepeatRadar | Cohort Analysis Demo",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar Controls (top) ---
# --- Header and Introduction ---
st.title("📡 RepeatRadar: Interactive Cohort Analysis")
st.markdown("""
Welcome to the interactive demo for **RepeatRadar**, a Python package I developed for streamlined cohort analysis. This dashboard showcases the package's core functionality and demonstrates my ability to build and document end-to-end data science projects.

**Purpose of this Dashboard:**
- **Demonstrate `RepeatRadar`:** Interactively explore cohort analysis on sample e-commerce data.
- **Showcase My Skills:** Highlight my capabilities in package development, data visualization, and creating user-friendly applications with Streamlit.

This tool allows you to generate and visualize user retention and value-based cohorts with just a few clicks. For a deeper dive into the package, visit the [official documentation](https://krinya.github.io/repeatradar/).
""")

# --- Quickstart Guide ---
with st.expander("🚀 Quickstart: Using the `RepeatRadar` Package", expanded=False):
    st.markdown("""
    You can easily install the package using pip:
    ```bash
    pip install repeatradar
    ```

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

# --- Initial Data Loading ---
if "ecommerce_data_raw" not in st.session_state:
    with st.spinner("Loading default e-commerce dataset..."):
        load_ecommerc_data("E-commerce Data 1")
    st.success("✅ Default dataset loaded successfully!")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Configuration")

st.sidebar.subheader("1. Select a Dataset")
selected_dataset = st.sidebar.selectbox(
    "Choose a sample dataset to analyze:",
    options=["E-commerce Data 1", "E-commerce Data 2", "Upload Your Own (Coming Soon)"],
    index=0,
    key="main_dataset_selector"
)

if st.sidebar.button("📥 Load Dataset", type="primary"):
    with st.spinner(f"Loading {selected_dataset}..."):
        load_ecommerc_data(selected_dataset)
    # Clear existing analysis when switching datasets
    if "cohort_data" in st.session_state:
        del st.session_state.cohort_data
    if "cohort_data_percent" in st.session_state:
        del st.session_state.cohort_data_percent
    st.success(f"✅ {selected_dataset} loaded successfully!")

st.sidebar.checkbox("Show Dataset Overview", value=False, key="dataset_overview_checkbox")
st.sidebar.caption("This will display the loaded dataset on the main screen.")


# --- Main Content Area ---
if st.session_state.get("ecommerce_data_raw") is not None:
    # --- Column Mapping in Sidebar ---

    # --- Auto-detect columns for cohort analysis ---
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



    columns_list = st.session_state.get("ecommerce_data_raw_columns", [])
    date_column, customer_id_column, default_value_col = get_auto_columns(selected_dataset, columns_list)

    # --- Value Column and Aggregation Function Selection (Sidebar) ---

    # Restrict value column options based on dataset
    if selected_dataset == "E-commerce Data 1":
        allowed_value_cols = [col for col in ['InvoiceNo', 'Quantity', 'StockCode', 'TotalPrice'] if col in columns_list]
    elif selected_dataset == "E-commerce Data 2":
        allowed_value_cols = [col for col in ['Sales', 'Profit', 'Product'] if col in columns_list]
    else:
        allowed_value_cols = []
    value_column_options = [None] + allowed_value_cols
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Advanced analysis options are available for value-based analysis.")
    value_column = st.sidebar.selectbox(
        "Value Column (Optional)",
        options=value_column_options,
        index=0,  # Always default to None
        help="Select a numeric column for value-based analysis (e.g., revenue).",
        key=f"value_column_selector_{selected_dataset}"
    )
    st.sidebar.caption("If you select a value column, click 'Generate Analysis' to update the results.")

    # Only show aggregation function if a value column is selected
    if value_column:
        st.sidebar.info("💡 **Tip:** Use 'sum' if you selected Price or 'nunique' for invoce releted columns.")
        aggregation_function = st.sidebar.selectbox(
            "Aggregation Function *",
            options=[None, "sum", "mean", "count", "median", "nunique"],
            index=0,  # Always default to None
            help="Choose how to aggregate the value column (e.g., sum for total revenue).",
            key="aggregation_function_selector"
        )
        is_value_analysis = aggregation_function is not None
    else:
        aggregation_function = None
        is_value_analysis = False

    # --- Dataset Overview ---
    if st.session_state.get("dataset_overview_checkbox"):
        st.header("📊 Dataset Overview")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.info(f"**Current Dataset:** `{selected_dataset}`")
        with col2:
            st.metric("Transaction Count", f"{st.session_state.ecommerce_data_raw.shape[0]:,}")
        with col3:
            st.metric("Total Columns", st.session_state.ecommerce_data_raw.shape[1])
        
        if st.checkbox("👁️ Show Raw Data Preview", value=False):
            with st.expander("📋 Raw Data Preview", expanded=True):
                rows_to_show = st.number_input("Number of rows to display:", min_value=5, max_value=1000, value=100, step=5)
                st.dataframe(
                    st.session_state.ecommerce_data_raw.head(rows_to_show),
                    use_container_width=True,
                    hide_index=True
                )


    # --- Analysis Parameters ---
    st.header("🔬 Analysis Parameters")
    st.markdown("Define the parameters for the cohort calculation. Choose how to group users and the timeframe for tracking their behavior.")

    col1, col2 = st.columns(2)

    with col1:
        period_options = {"Daily": "D", "Weekly": "W", "Monthly": "M", "Quarterly": "Q", "Yearly": "Y"}
        selected_period_display = st.selectbox(
            "Cohort Grouping",
            options=list(period_options.keys()),
            index=2,  # Default to Monthly
            help="Select the time period for grouping cohorts (e.g., all users who joined in the same month)."
        )
        cohort_period = period_options[selected_period_display]

    with col2:
        period_duration = st.selectbox(
            "Tracking Duration (days)",
            options=[1, 7, 30, 90, 180, 365],
            index=2,  # Default to 30 days
            help="Set the length of each period for tracking cohort activity."
        )


    # --- Generate Analysis ---
    can_generate = date_column is not None and customer_id_column is not None


    # Only auto-run on very first load (when cohort_data is not in session_state)
    if can_generate and "cohort_data" not in st.session_state:
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
        st.success("✅ Analysis complete!")

    # Keep the button for manual rerun if user wants to change parameters in the future
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
            st.session_state["_last_auto_run_dataset"] = selected_dataset
            st.session_state["_last_auto_run_date_col"] = date_column
            st.session_state["_last_auto_run_cust_col"] = customer_id_column
            st.session_state["_last_auto_run_period"] = cohort_period
            st.session_state["_last_auto_run_duration"] = period_duration
        st.success("✅ Analysis complete!")

    if not can_generate:
        st.warning("⚠️ Could not auto-detect required columns for cohort analysis. Please check your dataset.")

    # --- Results Display ---

    if st.session_state.get("cohort_data") is not None:
        st.header("📈 Results")

        if is_value_analysis:
            heatmap_title = f"Cohort Analysis: Sum of {value_column}"
            main_metric_label = f"Sum of {value_column}"
        else:
            heatmap_title = "Cohort Analysis: Active Users"
            main_metric_label = "User Count"

        st.subheader(heatmap_title)


        with st.container(border=True):
            st.markdown("**Heatmap Customization**")
            c1, c2, c3 = st.columns(3)
            with c1:
                color_scale = st.selectbox("Color Scale", ["Turbo", "Viridis", "Plasma", "Blues", "Reds", "Greens"], key="color_scale")
            with c2:
                reverse_colors = st.checkbox("Reverse Colors", key="reverse_colors")
            with c3:
                show_colorscale = st.checkbox("Show Legend", value=True, key="show_colorscale")

        final_color_scale = f"{color_scale}{'_r' if reverse_colors else ''}"
        cohort_heatmap = plot_cohort_heatmap(
            cohort_data=st.session_state.cohort_data,
            title=heatmap_title,
            color_scale=final_color_scale,
            show_colorscale=show_colorscale
        )
        st.plotly_chart(cohort_heatmap, use_container_width=True)

        with st.expander("💡 How to Interpret This Heatmap"):
            st.markdown(f"""
            This heatmap visualizes how groups of users (cohorts) behave over time.

            - **Rows (Cohort Period):** Each row is a cohort of users who made their first transaction in that specific time period (e.g., `2011-01`). The `cohort_size` column shows the total number of unique users in that cohort.
            - **Columns (Periods Since Acquisition):** The columns track the activity of each cohort in subsequent periods after they joined. `Period 0` is their acquisition period.
            - **Cell Values ({main_metric_label}):** Each cell shows the metric for a cohort in a given period. For example, the value in the `2011-01` row and `Period 1` column shows the total `{main_metric_label.lower()}` from that cohort in their second period.
            - **Color Intensity:** The color helps you quickly spot trends. Darker shades typically indicate higher values, making it easy to see which cohorts are most valuable or when engagement drops off.
            """)

        if st.checkbox(f"Show Raw Data Table ({main_metric_label})", value=True):
            df_display = st.session_state.cohort_data.copy().reset_index()
            df_display['cohort_period'] = df_display['cohort_period'].dt.date
            st.dataframe(df_display, use_container_width=True, hide_index=True)

        # --- Retention Rate Analysis (only if applicable) ---
        if st.session_state.get("cohort_data_percent") is not None and not is_value_analysis:
            st.subheader("Cohort Analysis: Retention Rate (%)")
            with st.container(border=True):
                st.markdown("**Heatmap Customization (Retention %)**")
                rc1, rc2, rc3 = st.columns(3)
                with rc1:
                    retention_color_scale = st.selectbox(
                        "Color Scale",
                        ["Turbo", "Viridis", "Plasma", "Blues", "Reds", "Greens"],
                        index=5,
                        key="retention_color_scale"
                    )
                with rc2:
                    retention_reverse_colors = st.checkbox("Reverse Colors", key="retention_reverse_colors")
                with rc3:
                    retention_show_colorscale = st.checkbox("Show Legend", value=True, key="retention_show_colorscale")

            retention_final_color_scale = f"{retention_color_scale}{'_r' if retention_reverse_colors else ''}"
            retention_heatmap = plot_cohort_heatmap(
                cohort_data=st.session_state.cohort_data_percent,
                title="User Retention Rate (%)",
                color_scale=retention_final_color_scale,
                show_colorscale=retention_show_colorscale
            )
            st.plotly_chart(retention_heatmap, use_container_width=True)

            if st.checkbox("Show Raw Data Table (Retention %)", value=False):
                df_percent_display = st.session_state.cohort_data_percent.copy().reset_index()
                df_percent_display['cohort_period'] = df_percent_display['cohort_period'].dt.date
                st.dataframe(df_percent_display, use_container_width=True, hide_index=True)
        elif is_value_analysis:
            st.info("ℹ️ **Note:** Retention rate analysis (in %) is available for user count analysis. To see it, use a dataset with no value column.")

else:
    st.info("⏳ Please wait while the default dataset is being loaded...")

# --- Footer ---
st.markdown("---")
st.sidebar.markdown("---")
st.sidebar.markdown("**Project Links**")
st.sidebar.markdown("- <a href='https://github.com/krinya/repeatradar' target='_blank'>📡 `RepeatRadar` Package (GitHub)</a>", unsafe_allow_html=True)
st.sidebar.markdown("- <a href='https://krinya.github.io/repeatradar/' target='_blank'>📦 Package Documentation</a>", unsafe_allow_html=True)
st.sidebar.markdown("- <a href='https://github.com/krinya/repeatradar_demo' target='_blank'>🖥️ Dashboard Source Code</a>", unsafe_allow_html=True)

footer_text = """
<div style='text-align: center; color: #888; font-size: 0.9em;'>
    <p>Built by Kristof Menyhert | 
    <a href='https://github.com/krinya/repeatradar' style='color: #888;' target='_blank'>GitHub</a> | 
    <a href='' style='color: #888;' target='_blank'>LinkedIn</a>
    </p>
</div>
"""
st.markdown(footer_text, unsafe_allow_html=True)
