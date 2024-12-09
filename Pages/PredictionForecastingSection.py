import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def prediction_forecasting():
    st.title("Salary Prediction & Forecasting for Individual Employee")

    # Check if data has been uploaded
    if 'uploaded_data' not in st.session_state:
        st.error("No data uploaded. Please upload a CSV file on the main page.")
        return

    # Load the uploaded data from the session state
    data = st.session_state['uploaded_data']

    # Create sidebar filters for employee selection
    if 'Employee' in data.columns:
        unique_employees = data['Employee'].unique()
        selected_employee = st.sidebar.selectbox("Select Employee for Prediction:", unique_employees)

        # Filter data for the selected employee
        employee_data = data[data['Employee'] == selected_employee]

        if employee_data.empty:
            st.error("No data found for the selected employee.")
            return

        # Get the current monthly income
        current_monthly_income = employee_data['Monthly Income (£)'].iloc[0]

    else:
        st.warning("No 'Employee' column found in the data.")
        return

    # Display current monthly income
    st.write(f"Current Monthly Income for {selected_employee}: £{current_monthly_income:.2f}")

    # Set parameters for forecasting
    annual_increase_rate = 0.03  # 3% annual increase
    initial_forecast_months = 12  # Forecasting for initial 12 months
    extended_forecast_months = 48  # Additional forecasting for 4 years (48 months)

    # Input for custom increases for all 12 months
    st.sidebar.header("Custom Salary Increases")
    custom_increases = {}

    for month in range(1, 13):  # Allowing input for all twelve months
        increase_amount = st.sidebar.number_input(f"Increase Amount for Month {month} (£):", min_value=0.0)
        custom_increases[month] = increase_amount

    # Calculate forecasted monthly income for initial 12 months
    forecasted_salaries_12_months = []
    forecasted_salaries_48_months = []

    current_salary = current_monthly_income

    # Calculate salaries for initial 12 months with adjustment logic
    for month in range(1, initial_forecast_months + 1):
        if month % 12 == 0:
            current_salary *= (1 + annual_increase_rate)

        # Apply custom increase and store salary before applying next month's logic
        previous_salary = current_salary
        current_salary += custom_increases.get(month, 0)

        forecasted_salaries_12_months.append(current_salary)

        # Revert to previous salary after applying increase
        if custom_increases.get(month, 0) > 0:
            current_salary = previous_salary

    # Calculate salaries for extended 4 years (48 months)
    for month in range(1, extended_forecast_months + 1):
        if month % 12 == 0:
            current_salary *= (1 + annual_increase_rate)

        forecasted_salaries_48_months.append(current_salary)

    # Combine both forecasts into one list for plotting
    total_forecasted_salaries = forecasted_salaries_12_months + forecasted_salaries_48_months

    # Display line chart with improved readability and spacing
    plt.figure(figsize=(16, 8))  # Increased size of the plot

    x_values = range(1, initial_forecast_months + extended_forecast_months + 1)

    plt.plot(x_values[:initial_forecast_months], forecasted_salaries_12_months, marker='o', linestyle='-', color='b',
             label='Forecast (Next 12 Months)', markersize=8)

    plt.plot(x_values[initial_forecast_months:], forecasted_salaries_48_months, marker='o', linestyle='-',
             color='orange',
             label='Forecast (Next 4 Years)', markersize=8)

    plt.title(f"Forecasted Monthly Salaries for {selected_employee}", fontsize=20)

    plt.xlabel("Month", fontsize=16)
    plt.ylabel("Salary (£)", fontsize=16)

    plt.xticks(x_values, [str(i) for i in x_values], fontsize=14)  # Just numbers on x-axis without "Month"

    plt.xticks(rotation=45)  # Rotate x-axis labels to avoid overlap

    plt.grid(True)

    plt.legend(fontsize=14)

    # Set limits to center lines better within plot area
    max_salary = max(total_forecasted_salaries) * 1.1  # Add some space above max salary
    min_salary = min(total_forecasted_salaries) * 0.9  # Add some space below min salary

    plt.ylim(min_salary, max_salary)

    # Show plot in Streamlit app above salary forecasts
    st.pyplot(plt)

    # Display forecasted salaries and total salary with bonus
    st.write(f"Forecasted Monthly Salaries for {selected_employee}:")

    # Displaying only the first year (12 months) separately
    for month, salary in enumerate(forecasted_salaries_12_months, start=1):
        st.write(f"Month {month}: £{salary:.2f}")

    # Displaying total salary including a bonus (the extra month's salary)
    total_salary_with_bonus = sum(forecasted_salaries_12_months) + current_monthly_income
    st.write(f"\nTotal Salary Including Current Month Bonus: £{total_salary_with_bonus:.2f}")


# Run the main function when the script is executed
if __name__ == "__main__":
    prediction_forecasting()