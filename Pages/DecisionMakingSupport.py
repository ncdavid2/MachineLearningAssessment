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

    # Current Savings
    st.subheader("Current Savings Analysis")
    target_col = 'Savings for Property (£)'

    try:
        current_savings = data[target_col].iloc[-1]  # Get the latest savings value

        # Set Savings Goal
        savings_goal = st.number_input("Set Your Savings Target (£):", min_value=0.0, step=100.0)

    except Exception as e:
        st.error(f"Error retrieving current savings: {e}")

    # Interactivity and Real-Time Updates
    st.subheader("Adjust Current Savings")
    try:
        real_time_savings = st.slider("Adjust Current Savings (£):", min_value=0, max_value=int(current_savings + 5000),
                                      value=int(current_savings))
        updated_goal_status = "Met" if real_time_savings >= savings_goal else "Not Met"
        st.write(f"Updated Goal Status: {updated_goal_status}")

        if updated_goal_status == "Not Met":
            remaining_amount = savings_goal - real_time_savings
            st.warning(f"You still need to save £{remaining_amount:.2f} to meet your target.")

            # Calculate required monthly, weekly, and daily savings based on adjusted savings
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

            # Suggest areas to save money
            st.subheader("Consider the following to save money:")

            expenses_to_check = ['Sky Sports (£)', 'Netflix (£)', 'Amazon Prime (£)', 'Monthly Outing (£)']
            for expense in expenses_to_check:
                if expense in data.columns:
                    non_zero_count = (data[expense] > 0).sum()
                    if non_zero_count > 0:
                        avg_expense = data[data[expense] > 0][expense].mean()
                        st.write(f"- {expense[:-4]} (£{avg_expense:.2f}/month)")
                        st.write(f"  Applies to {non_zero_count} out of {len(data)} employees")

        else:
            st.success("You have met your adjusted savings goal!")

    except Exception as e:
        st.error(f"Real-time updates error: {e}")


if __name__ == "__main__":
    decision_making_support()
