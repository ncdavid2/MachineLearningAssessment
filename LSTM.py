import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import LSTM, Dense

#to start the page use: streamlit run LSTM.py

# File Upload Section
if "uploaded_data" not in st.session_state:
    st.session_state["uploaded_data"] = None

#File Upload and Basic Validation
st.title("Personal Finance Management System with LSTM and Interactive Features")

uploaded_file = st.file_uploader("Upload your CSV file:", type=["csv"])
if uploaded_file is not None:
    try:
        # Read uploaded CSV file
        data = pd.read_csv(uploaded_file)
        st.session_state['uploaded_data'] = data
        st.write("Data Preview:", data.head())
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()
elif st.session_state["uploaded_data"] is not None:
        data = st.session_state["uploaded_data"]
        st.write("Data Preview (from session):", data.head())
else:
    st.warning("Please upload a CSV file to proceed.")
    st.stop()
