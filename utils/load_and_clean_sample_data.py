import pandas as pd
import streamlit as st

def load_ecommerc_data_sample1():
    """
    Load a sample e-commerce dataset.
    
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

def load_ecommerc_data_sample2():
    """
    Load a second sample e-commerce dataset.
    
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

def load_ecommerc_data(selected_dataset):
    """
    Function to load the selected e-commerce dataset.
    This function is called when the user clicks the 'Load Data' button.
    """
   
    if selected_dataset == "E-commerce Data 1":
        # Load the first sample dataset
        st.session_state.ecommerce_data_raw = load_ecommerc_data_sample1()
        st.session_state.ecommerce_data_raw_columns = [None] + st.session_state.ecommerce_data_raw.columns.tolist()
    elif selected_dataset == "E-commerce Data 2":
        # Load the second sample dataset
        st.session_state.ecommerce_data_raw = load_ecommerc_data_sample2()
        st.session_state.ecommerce_data_raw_columns = [None] + st.session_state.ecommerce_data_raw.columns.tolist()
    else:
        st.session_state.ecommerce_data_raw = None
        st.session_state.ecommerce_data_raw_columns = None