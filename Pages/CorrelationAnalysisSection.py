import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def correlation_analysis():
    st.title("Correlation Analysis")

    # Load data
    data = st.session_state['uploaded_data']

    # Select expense categories for analysis
    expense_columns = ['Monthly Income (£)', 'Water Bill (£)', 'Electricity Bill (£)', 'Gas Bill (£)', 'Groceries (£)', 'Transportation (£)', 'Sky Sports (£)', 'Other Expenses (£)', 'Savings for Property (£)', 'Monthly Outing (£)', 'Netflix (£)', 'Amazon Prime (£)']
    selected_categories = st.multiselect("Select categories for correlation analysis:", expense_columns, default=expense_columns[:5])

    if len(selected_categories) < 2:
        st.warning("Please select at least two categories for correlation analysis.")
        return

    # Calculate correlation matrix
    correlation_matrix = data[selected_categories].corr()

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
    plt.title("Correlation Heatmap")
    st.pyplot(fig)

if __name__ == "__main__":
    correlation_analysis()