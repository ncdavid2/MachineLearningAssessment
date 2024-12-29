import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression

def exploratory_data_analysis():
    st.title("Exploratory Data Analysis (EDA)")
    st.sidebar.title("EDA Navigation")

    if 'uploaded_data' not in st.session_state:
        st.error("No data uploaded. Please upload a CSV file on the main page.")
        return
    data = st.session_state['uploaded_data']

    # Create sidebar filters for employee selection
    st.sidebar.subheader("Filters")
    if 'Employee' in data.columns:
        unique_employees = data['Employee'].unique()

        if len(unique_employees) >= 5:
            default_selection = unique_employees[0:5].tolist()
        else:
            default_selection = unique_employees.tolist()

        selected_employees = st.sidebar.multiselect("Filter by Employees:", unique_employees, default=default_selection)
        data = data[data['Employee'].isin(selected_employees)]
    else:
        st.warning("No 'Employee' column found in the data.")

    visualizations = ["Spending Trends", "Spending Category Distributions", "Income vs Expenses"]
    selected_visualization = st.sidebar.radio("Select Visualization:", visualizations)

    # Spending Trends visualization
    if selected_visualization == "Spending Trends":
        st.subheader("Spending Trends")
        expense_columns = ['Electricity Bill (£)', 'Gas Bill (£)', 'Netflix (£)', 'Amazon Prime (£)', 'Groceries (£)',
                           'Transportation (£)', 'Water Bill (£)', 'Sky Sports (£)', 'Other Expenses (£)',
                           'Monthly Outing (£)']
        selected_expense = st.selectbox("Select Expense Category:", expense_columns)
        fig = px.bar(data, x='Employee', y=selected_expense, title=f"{selected_expense} by Employee")
        st.plotly_chart(fig)

        # Expense prediction for individual employee
        st.subheader("Expense Prediction for Individual Employee")
        selected_employee = st.selectbox("Select Employee for Prediction:", data['Employee'])
        if not selected_employee:
            st.error("It is necessary to select at least one employee to proceed.")
        else:
            employee_data = data[data['Employee'] == selected_employee]
            first_month_expense = employee_data[selected_expense].iloc[0]
            st.write(f"First Month's {selected_expense}: £{first_month_expense:.2f}")

            st.write("Enter your expected expenses for the next two months:")
            next_month_expense = st.number_input(
                "Next month expense (£):",
                min_value=0.0,
                value=first_month_expense,
                step=0.01
            )
            second_month_expense = st.number_input(
                "Second month expense (£):",
                min_value=0.0,
                value=first_month_expense,
                step=0.01
            )

            X = np.array(range(len(employee_data) + 2)).reshape(-1, 1)
            y = np.concatenate([
                employee_data[selected_expense].values,
                [next_month_expense, second_month_expense]
            ])

            # Create and train a linear regression model
            model = LinearRegression()
            model.fit(X, y)

            future_months = st.slider("Predict expenses for next n months:", 1, 12, 3)
            future_X = np.array(range(len(X), len(X) + future_months)).reshape(-1, 1)
            predictions = model.predict(future_X)
            historical_data = employee_data[selected_expense].values
            full_data = np.concatenate([historical_data, [next_month_expense, second_month_expense], predictions])

            fig_pred = px.line(
                x=range(len(full_data)),
                y=full_data,
                title=f"{selected_expense} Trend and Prediction for {selected_employee}"
            )
            fig_pred.add_vline(
                x=len(historical_data) - 1,
                line_dash="dash",
                annotation_text="Bill Months Given"
            )
            fig_pred.add_vline(
                x=len(historical_data) + 1,
                line_dash="dash",
                annotation_text="Predictions"
            )
            st.plotly_chart(fig_pred)

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
            total_expenses = data[expense_columns].sum()
            fig_pie = px.pie(values=total_expenses.values, names=total_expenses.index,
                             title="Overall Expense Distribution")
            st.plotly_chart(fig_pie)
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
            expense_columns = ['Electricity Bill (£)', 'Gas Bill (£)', 'Netflix (£)', 'Amazon Prime (£)',
                               'Groceries (£)',
                               'Transportation (£)', 'Water Bill (£)', 'Sky Sports (£)', 'Other Expenses (£)',
                               'Monthly Outing (£)']
            data['Total Expenses'] = data[expense_columns].sum(axis=1)
            data['Savings'] = data['Savings for Property (£)']
            fig = px.bar(data, x='Employee', y=['Monthly Income (£)', 'Total Expenses', 'Savings'],
                         title="Income vs Expenses and Savings by Employee", barmode='group')
            st.plotly_chart(fig)
            data['Savings Percentage'] = (data['Savings'] / data['Monthly Income (£)'] * 100)
            savings_percentage = data['Savings Percentage'].mean()

            st.write(f"Average Savings Percentage: {savings_percentage:.2f}%")
        except Exception as e:
            st.error(f"Error plotting income vs expenses: {e}")

if __name__ == "__main__":
    exploratory_data_analysis()