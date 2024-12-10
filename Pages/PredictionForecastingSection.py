import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def prediction_forecasting():
    st.title("Salary Prediction & Forecasting for Individual Employee")

    if 'uploaded_data' not in st.session_state:
        st.error("No data uploaded. Please upload a CSV file on the main page.")
        return

    data = st.session_state['uploaded_data']

    if 'Employee' in data.columns:
        unique_employees = data['Employee'].unique()
        selected_employee = st.selectbox("Select Employee for Prediction:", unique_employees)

        employee_data = data[data['Employee'] == selected_employee]

        if employee_data.empty:
            st.error("No data found for the selected employee.")
            return

        current_monthly_income = employee_data['Monthly Income (£)'].iloc[0]
    else:
        st.warning("No 'Employee' column found in the data.")
        return

    # Display current monthly income (first month)
    st.write(f"Month 1 Income for {selected_employee}: £{current_monthly_income:.2f}")

    # Input fields for the second and third months
    month2_income = st.number_input("Month 2 Income (£):", value=float(current_monthly_income), step=0.01)
    month3_income = st.number_input("Month 3 Income (£):", value=float(current_monthly_income), step=0.01)

    # Calculate average monthly change
    avg_monthly_change = (month3_income - current_monthly_income) / 2

    # Generate predictions for 48 months
    forecasted_salaries = [current_monthly_income, month2_income, month3_income]
    for month in range(4, 49):
        next_salary = forecasted_salaries[-1] + avg_monthly_change
        forecasted_salaries.append(next_salary)

    # Display line chart
    plt.figure(figsize=(16, 8))

    x_values = range(1, 49)
    plt.plot(x_values[:3], forecasted_salaries[:3], marker='o', linestyle='-', color='b', markersize=8, label='Input Months')
    plt.plot(x_values[3:], forecasted_salaries[3:], marker='o', linestyle='-', color='green', markersize=8, label='Predicted Months')

    plt.title(f"Forecasted Monthly Salaries for {selected_employee}", fontsize=20)
    plt.xlabel("Month", fontsize=16)
    plt.ylabel("Salary (£)", fontsize=16)
    plt.xticks(x_values, [str(i) for i in x_values], fontsize=14, rotation=45)
    plt.grid(True)
    plt.legend()

    max_salary = max(forecasted_salaries) * 1.1
    min_salary = min(forecasted_salaries) * 0.9
    plt.ylim(min_salary, max_salary)

    st.pyplot(plt)

    # Display predictions for years 1, 2, 3, and 4
    st.subheader("Salary Predictions for Years 1-4")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write("Year 1 (Month 12)")
        st.write(f"£{forecasted_salaries[0]:.2f}")
        st.write(f"£{forecasted_salaries[1]:.2f}")
        st.write(f"£{forecasted_salaries[2]:.2f}")
        st.write(f"£{forecasted_salaries[3]:.2f}")
        st.write(f"£{forecasted_salaries[4]:.2f}")
        st.write(f"£{forecasted_salaries[5]:.2f}")
        st.write(f"£{forecasted_salaries[6]:.2f}")
        st.write(f"£{forecasted_salaries[7]:.2f}")
        st.write(f"£{forecasted_salaries[8]:.2f}")
        st.write(f"£{forecasted_salaries[9]:.2f}")
        st.write(f"£{forecasted_salaries[10]:.2f}")
        st.write(f"£{forecasted_salaries[11]:.2f}")

    with col2:
        st.write("Year 2 (Month 24)")
        st.write(f"£{forecasted_salaries[12]:.2f}")
        st.write(f"£{forecasted_salaries[13]:.2f}")
        st.write(f"£{forecasted_salaries[14]:.2f}")
        st.write(f"£{forecasted_salaries[15]:.2f}")
        st.write(f"£{forecasted_salaries[16]:.2f}")
        st.write(f"£{forecasted_salaries[17]:.2f}")
        st.write(f"£{forecasted_salaries[18]:.2f}")
        st.write(f"£{forecasted_salaries[19]:.2f}")
        st.write(f"£{forecasted_salaries[20]:.2f}")
        st.write(f"£{forecasted_salaries[21]:.2f}")
        st.write(f"£{forecasted_salaries[22]:.2f}")
        st.write(f"£{forecasted_salaries[23]:.2f}")

    with col3:
        st.write("Year 3 (Month 36)")
        st.write(f"£{forecasted_salaries[24]:.2f}")
        st.write(f"£{forecasted_salaries[25]:.2f}")
        st.write(f"£{forecasted_salaries[26]:.2f}")
        st.write(f"£{forecasted_salaries[27]:.2f}")
        st.write(f"£{forecasted_salaries[28]:.2f}")
        st.write(f"£{forecasted_salaries[29]:.2f}")
        st.write(f"£{forecasted_salaries[30]:.2f}")
        st.write(f"£{forecasted_salaries[31]:.2f}")
        st.write(f"£{forecasted_salaries[32]:.2f}")
        st.write(f"£{forecasted_salaries[33]:.2f}")
        st.write(f"£{forecasted_salaries[34]:.2f}")
        st.write(f"£{forecasted_salaries[35]:.2f}")

    with col4:
        st.write("Year 4 (Month 48)")
        st.write(f"£{forecasted_salaries[36]:.2f}")
        st.write(f"£{forecasted_salaries[37]:.2f}")
        st.write(f"£{forecasted_salaries[38]:.2f}")
        st.write(f"£{forecasted_salaries[39]:.2f}")
        st.write(f"£{forecasted_salaries[40]:.2f}")
        st.write(f"£{forecasted_salaries[41]:.2f}")
        st.write(f"£{forecasted_salaries[42]:.2f}")
        st.write(f"£{forecasted_salaries[43]:.2f}")
        st.write(f"£{forecasted_salaries[44]:.2f}")
        st.write(f"£{forecasted_salaries[45]:.2f}")
        st.write(f"£{forecasted_salaries[46]:.2f}")
        st.write(f"£{forecasted_salaries[47]:.2f}")

if __name__ == "__main__":
    prediction_forecasting()
