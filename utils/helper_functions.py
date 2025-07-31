import streamlit as st
import pandas as pd
from repeatradar import generate_cohort_data, plot_cohort_heatmap
 
def handle_generate_cohort_data(data, date_column, customer_id_column, cohort_period, period_duration, value_column=None, aggregation_function=None, output_format='pivot', **kwargs):

        # Handle the case where value_column is provided but aggregation_function is None
        if value_column and value_column != "None" and aggregation_function is None:
            aggregation_function = "sum"  # Default to sum when value column is used
        
        # If no value column, set both to None
        if not value_column or value_column == "None":
            value_column = None
            aggregation_function = None

        # Dataframe output
        with st.spinner("Generating cohort analysis..."):
            st.session_state.cohort_data = generate_cohort_data(
                data=data,
                date_column=date_column,
                user_column=customer_id_column,
                cohort_period=cohort_period,
                period_duration=period_duration,
                calculate_retention_rate=False,
                value_column=value_column,
                aggregation_function=aggregation_function,
                output_format=output_format,
            )

            # Only generate retention rate data when no value column is used
            # Retention rate calculation is only available for user count analysis
            if value_column is None:
                st.session_state.cohort_data_percent = generate_cohort_data(
                    data=data,
                    date_column=date_column,
                    user_column=customer_id_column,
                    cohort_period=cohort_period,
                    period_duration=period_duration,
                    calculate_retention_rate=True,
                    value_column=None,  # Always None for retention rate
                    aggregation_function=None,  # Always None for retention rate
                    output_format=output_format,
                )
            else:
                # When using value column, create a copy without retention rates
                st.session_state.cohort_data_percent = st.session_state.cohort_data.copy()

            # Heatmap output
            if st.session_state.cohort_data is not None:
                st.session_state.cohort_heatmap = plot_cohort_heatmap(cohort_data=st.session_state.cohort_data,
                                                                    title="Cohort Heatmap",
                                                                    color_scale="Turbo", # make this advanced function via dropdown if you can also make it reversible with adding '_r' to the color scale name
                                                                    show_colorscale=False # make this advanced function via dropdown
                                                                    ) 
                
                # Only create retention heatmap if retention data is available
                if value_column is None and st.session_state.cohort_data_percent is not None:
                    st.session_state.cohort_heatmap_percent = plot_cohort_heatmap(cohort_data=st.session_state.cohort_data_percent,
                                                                                title="Cohort Heatmap Percent",
                                                                                color_scale="Turbo", # make this advanced function via dropdown if you can also make it reversible with adding '_r' to the color scale name
                                                                                show_colorscale=False # make this advanced function via dropdown
                                                                                )
            
            # Reset index for the dataframes with keeping the index
            if st.session_state.cohort_data_percent is not None:
                st.session_state.cohort_data_percent.reset_index(drop=False, inplace=True)

                # try to convert 'cohort_period' from datetime yyyy-mm-dd to just yyyy-mm-dd
                if "cohort_period" in st.session_state.cohort_data_percent.columns:
                    st.session_state.cohort_data_percent["cohort_period"] = st.session_state.cohort_data_percent["cohort_period"].dt.strftime('%Y-%m-%d')
            
            st.session_state.cohort_data.reset_index(drop=False, inplace=True)

            # try to convert 'cohort_period' from datetime yyyy-mm-dd to just yyyy-mm-dd
            if "cohort_period" in st.session_state.cohort_data.columns:
                st.session_state.cohort_data["cohort_period"] = st.session_state.cohort_data["cohort_period"].dt.strftime('%Y-%m-%d')