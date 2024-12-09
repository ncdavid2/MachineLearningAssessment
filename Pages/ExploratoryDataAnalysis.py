import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression


def exploratory_data_analysis():
    # Set up the main title for the Streamlit app
    st.title("Exploratory Data Analysis (EDA)")
    st.sidebar.title("EDA Navigation")

    # Check if data has been uploaded
    if 'uploaded_data' not in st.session_state:
        st.error("No data uploaded. Please upload a CSV file on the main page.")
        return

    # Load the uploaded data from the session state
    data = st.session_state['uploaded_data']

    # Create sidebar filters for employee selection
    st.sidebar.subheader("Filters")
    if 'Employee' in data.columns:
        unique_employees = data['Employee'].unique()

        # Automatically select the first 5 employees
        default_selection = unique_employees[:5].tolist() if len(unique_employees) >= 5 else unique_employees.tolist()

        selected_employees = st.sidebar.multiselect("Filter by Employees:", unique_employees, default=default_selection)
        data = data[data['Employee'].isin(selected_employees)]
    else:
        st.warning("No 'Employee' column found in the data.")

    # Create a radio button for selecting different visualizations
    visualizations = ["Spending Trends", "Spending Category Distributions", "Income vs Expenses"]
    selected_visualization = st.sidebar.radio("Select Visualization:", visualizations)

    # Spending Trends visualization
    if selected_visualization == "Spending Trends":
        st.subheader("Spending Trends")
        expense_columns = ['Electricity Bill (£)', 'Gas Bill (£)', 'Netflix (£)', 'Amazon Prime (£)', 'Groceries (£)',
                           'Transportation (£)', 'Water Bill (£)', 'Sky Sports (£)', 'Other Expenses (£)',
                           'Monthly Outing (£)']
        selected_expense = st.selectbox("Select Expense Category:", expense_columns)

        # Create a bar chart of the selected expense for all employees
        fig = px.bar(data, x='Employee', y=selected_expense, title=f"{selected_expense} by Employee")
        st.plotly_chart(fig)

        # Expense prediction for individual employee
        st.subheader("Expense Prediction for Individual Employee")
        selected_employee = st.selectbox("Select Employee for Prediction:", data['Employee'])
        if not selected_employee:
            st.error("It is necessary to select at least one employee to proceed.")
        else:
            # Proceed with the prediction code for the selected employee
            employee_data = data[data['Employee'] == selected_employee]

            # Prepare data for the selected employee
            X = np.array(range(len(employee_data))).reshape(-1, 1)
            y = employee_data[selected_expense].values

            # Create and train a linear regression model
            model = LinearRegression()
            model.fit(X, y)

            # Make predictions for future months
            future_months = st.slider("Predict expenses for next n months:", 1, 12, 3)
            future_X = np.array(range(len(employee_data), len(employee_data) + future_months)).reshape(-1, 1)
            predictions = model.predict(future_X)

            # Plot the predictions
            fig_pred = px.line(x=range(len(employee_data) + future_months), y=list(y) + list(predictions),
                               title=f"{selected_expense} Trend and Prediction for {selected_employee}")
            fig_pred.add_vline(x=len(employee_data) - 1, line_dash="dash", annotation_text="Prediction Start")
            st.plotly_chart(fig_pred)

            # Display predicted values
            st.write(f"Predicted {selected_expense} for {selected_employee} for the next {future_months} months:")
            for i, pred in enumerate(predictions, 1):
                st.write(f"Month {i}: £{pred:.2f}")

    # Spending Category Distributions visualization
    elif selected_visualization == "Spending Category Distributions":
        st.subheader("Spending Category Distributions")
        try:
            expense_columns = ['Electricity Bill (£)', 'Gas Bill (£)', 'Netflix (£)', 'Amazon Prime (£)',
                               'Groceries (£)', 'Transportation (£)', 'Water Bill (£)', 'Sky Sports (£)',
                               'Other Expenses (£)', 'Monthly Outing (£)']
            # Create a pie chart of overall expense distribution
            total_expenses = data[expense_columns].sum()
            fig_pie = px.pie(values=total_expenses.values, names=total_expenses.index,
                             title="Overall Expense Distribution")
            st.plotly_chart(fig_pie)

            # Create a pie chart of expense distribution for a selected employee
            selected_employee = st.selectbox("Select Employee for Detailed Breakdown:", data['Employee'])
            employee_expenses = data[data['Employee'] == selected_employee][expense_columns].iloc[0]
            fig_employee_pie = px.pie(values=employee_expenses.values, names=employee_expenses.index,
                                      title=f"Expense Distribution for {selected_employee}")
            st.plotly_chart(fig_employee_pie)
        except Exception as e:
            st.error(f"Error plotting category distributions: {e}")

    # Income vs Expenses visualization
    elif selected_visualization == "Income vs Expenses":
        st.subheader("Income vs Expenses")
        try:
            # Calculate total expenses and savings for each employee
            data['Total Expenses'] = data[
                ['Electricity Bill (£)', 'Gas Bill (£)', 'Netflix (£)', 'Amazon Prime (£)', 'Groceries (£)',
                 'Transportation (£)', 'Water Bill (£)', 'Sky Sports (£)', 'Other Expenses (£)',
                 'Monthly Outing (£)']].sum(axis=1)
            data['Savings'] = data['Monthly Income (£)'] - data['Total Expenses']

            # Create a grouped bar chart of income, expenses, and savings
            fig = px.bar(data, x='Employee', y=['Monthly Income (£)', 'Total Expenses', 'Savings'],
                         title="Income vs Expenses and Savings by Employee", barmode='group')
            st.plotly_chart(fig)

            # Calculate and display average savings percentage
            savings_percentage = (data['Savings'] / data['Monthly Income (£)'] * 100).mean()
            st.write(f"Average Savings Percentage: {savings_percentage:.2f}%")
        except Exception as e:
            st.error(f"Error plotting income vs expenses: {e}")


# Run the main function when the script is executed
if __name__ == "__main__":
    exploratory_data_analysis()