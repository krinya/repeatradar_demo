import pandas as pd
import streamlit as st


@st.cache_data(ttl=86400)  # Cache for 24 hours (86400 seconds)
def load_ecommerce_data_sample1():
    """
    Load a sample e-commerce dataset with 24-hour caching.
    
    Returns:
        pd.DataFrame: A DataFrame containing the sample e-commerce data.
    """
    ecommerce_data = pd.read_csv('data/ecommerce_data_1.csv',
                             encoding='ISO-8859-1',
                             dtype={'CustomerID': str, 'InvoiceID': str})
    
    ecommerce_data['InvoiceDateTime'] = ecommerce_data['InvoiceDate'].apply(lambda x: pd.to_datetime(x, format='%m/%d/%Y %H:%M'))
    ecommerce_data['InvoiceDate'] = ecommerce_data['InvoiceDateTime'].dt.date
    ecommerce_data['TotalPrice'] = ecommerce_data['Quantity'] * ecommerce_data['UnitPrice'] 

    ecommerce_data = ecommerce_data.dropna(axis = 0, subset = ['CustomerID'])
    ecommerce_data.drop_duplicates(inplace = True)

    return ecommerce_data

@st.cache_data(ttl=86400)  # Cache for 24 hours (86400 seconds)
def load_ecommerce_data_sample2():
    """
    Load a second sample e-commerce dataset with 24-hour caching.
    
    Returns:
        pd.DataFrame: A DataFrame containing the second sample e-commerce data.
    """
    ecommerce_data = pd.read_csv('data/ecommerce_data_2.csv')
    
    ecommerce_data['OrderedDateTime'] = ecommerce_data['Order_Date'] + ' ' + ecommerce_data['Time']
    ecommerce_data['OrderedDateTime'] = pd.to_datetime(ecommerce_data['OrderedDateTime'], format='%Y-%m-%d %H:%M:%S')

    ecommerce_data = ecommerce_data.dropna(axis = 0, subset = ['OrderedDateTime'])
    ecommerce_data = ecommerce_data.dropna(axis = 0, subset = ['Customer_Id'])
    
    ecommerce_data.drop_duplicates(inplace = True)

    return ecommerce_data

@st.cache_data(ttl=86400)  # Cache for 24 hours
def get_dataset_columns(dataset_name):
    """
    Get the column list for a specific dataset with caching.
    
    Args:
        dataset_name (str): Name of the dataset
        
    Returns:
        list: List of column names with None prepended
    """
    if dataset_name == "E-commerce Data 1":
        data = load_ecommerce_data_sample1()
    elif dataset_name == "E-commerce Data 2":
        data = load_ecommerce_data_sample2()
    else:
        return [None]
    
    return [None] + data.columns.tolist()



def load_ecommerce_data(selected_dataset):
    """
    Function to load the selected e-commerce dataset using cached data loaders.
    This function efficiently loads data with 24-hour caching across sessions.
    
    Args:
        selected_dataset (str): Name of the dataset to load
    """
    if selected_dataset == "E-commerce Data 1":
        # Load the first sample dataset using cached function
        st.session_state.ecommerce_data_raw = load_ecommerce_data_sample1()
        st.session_state.ecommerce_data_raw_columns = get_dataset_columns("E-commerce Data 1")
    elif selected_dataset == "E-commerce Data 2":
        # Load the second sample dataset using cached function
        st.session_state.ecommerce_data_raw = load_ecommerce_data_sample2()
        st.session_state.ecommerce_data_raw_columns = get_dataset_columns("E-commerce Data 2")
    else:
        st.session_state.ecommerce_data_raw = None
        st.session_state.ecommerce_data_raw_columns = None