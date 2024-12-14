import streamlit as st
import pandas as pd


def decision_making_support():
    st.title("Decision-Making Support")

    # Load data
    if 'uploaded_data' in st.session_state:
        data = pd.DataFrame(st.session_state['uploaded_data'])
    else:
        st.error("No data uploaded.")
        return

    # Monthly Income
    st.subheader("Monthly Savings Analysis")
    income_col = 'Monthly Income (£)'

    if 'Employee' in data.columns:
        unique_employees = data['Employee'].unique()
        selected_employee = st.selectbox("Select Employee for Prediction:", unique_employees)

        employee_data = data[data['Employee'] == selected_employee]

        if employee_data.empty:
            st.error("No data found for the selected employee.")
            return

        monthly_income = employee_data[income_col].iloc[0]
    else:
        st.warning("No 'Employee' column found in the data.")
        return

    try:
        # Set Savings Goal
        savings_goal = st.number_input("Set Your Savings Target (£):", min_value=0.0, step=100.0)

    except Exception as e:
        st.error(f"Error retrieving monthly income: {e}")

    # Interactivity and Real-Time Updates
    st.subheader("Adjust savings from the Monthly Income")
    try:
        real_time_income = st.slider(
            "Adjust Savings:",
            min_value=0,
            max_value=int(monthly_income),
            value=int(),
        )

        current_savings = real_time_income

        updated_goal_status = "Met" if current_savings >= savings_goal else "Not Met"
        st.write(f"Updated Goal Status: {updated_goal_status}")

        if updated_goal_status == "Not Met":
            remaining_amount = savings_goal - current_savings
            st.warning(f"You still need to save £{remaining_amount:.2f} to meet your target.")

            if remaining_amount > 0:
                monthly_contribution_adjusted = remaining_amount / 12
                weekly_contribution_adjusted = remaining_amount / 52
                daily_contribution_adjusted = remaining_amount / 365

                st.write(
                    f"To meet your adjusted goal in one year, save an additional £{monthly_contribution_adjusted:.2f} per month.")
                st.write(
                    f"To meet your adjusted goal in one year, save an additional £{weekly_contribution_adjusted:.2f} per week.")
                st.write(
                    f"To meet your adjusted goal in one year, save an additional £{daily_contribution_adjusted:.2f} per day.")

            # Suggest areas to save money for the selected employee
            st.subheader("Consider the following to save money:")

            expenses_to_check = ['Sky Sports (£)', 'Netflix (£)', 'Amazon Prime (£)', 'Monthly Outing (£)']
            suggestions_made = False
            for expense in expenses_to_check:
                if expense in employee_data.columns and employee_data[expense].iloc[0] > 0:
                    expense_value = employee_data[expense].iloc[0]
                    st.write(f"- {expense[:-4]} (£{expense_value:.2f}/month)")
                    suggestions_made = True

            if not suggestions_made:
                st.write("No specific suggestions available based on current expenses.")

        else:
            st.success("You have met your adjusted savings goal!")

    except Exception as e:
        st.error(f"Real-time updates error: {e}")


if __name__ == "__main__":
    decision_making_support()
