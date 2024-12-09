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
    expense_columns = ['Monthly Income (£)', 'Electricity Bill (£)', 'Gas Bill (£)', 'Groceries (£)', 'Transportation (£)', 'Sky Sports (£)', 'Other Expenses (£)', 'Savings for Property (£)', 'Monthly Outing (£)']
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

    # Interpret correlations
    st.subheader("Correlation Insights")
    for i in range(len(selected_categories)):
        for j in range(i+1, len(selected_categories)):
            corr = correlation_matrix.iloc[i, j]
            if abs(corr) > 0.5:
                st.write(f"**{selected_categories[i]}** and **{selected_categories[j]}** have a {'strong positive' if corr > 0 else 'strong negative'} correlation ({corr:.2f}).")
                if 'Savings for Property (£)' in [selected_categories[i], selected_categories[j]]:
                    other_category = selected_categories[j] if selected_categories[i] == 'Savings for Property (£)' else selected_categories[i]
                    if corr > 0:
                        st.write(f"Consider maintaining or increasing {other_category} to potentially boost savings.")
                    else:
                        st.write(f"Consider reducing {other_category} to potentially increase savings.")

    # Optimization suggestions
    st.subheader("Optimization Suggestions")
    if 'Savings for Property (£)' in selected_categories:
        savings_corr = correlation_matrix['Savings for Property (£)'].sort_values(ascending=False)
        st.write("To potentially increase savings, consider:")
        for category, corr in savings_corr.items():
            if category != 'Savings for Property (£)':
                if corr > 0.3:
                    st.write(f"- Increasing {category}")
                elif corr < -0.3:
                    st.write(f"- Reducing {category}")
    else:
        st.write("Please include 'Savings for Property (£)' in your selection to see optimization suggestions.")

if __name__ == "__main__":
    correlation_analysis()