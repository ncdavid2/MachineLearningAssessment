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
        st.write(f"Current Savings: £{current_savings:.2f}")

        # Set Savings Goal
        savings_goal = st.number_input("Set Your Savings Target (£):", min_value=0.0, step=100.0)

        # Calculate Additional Savings Needed
        if current_savings < savings_goal:
            additional_savings_needed = savings_goal - current_savings
            st.warning(f"You need to save an additional £{additional_savings_needed:.2f} to meet your target.")

    except Exception as e:
        st.error(f"Error retrieving current savings: {e}")

    # Step 5: Interactivity and Real-Time Updates
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

        else:
            st.success("You have met your adjusted savings goal!")

    except Exception as e:
        st.error(f"Real-time updates error: {e}")

if __name__ == "__main__":
    decision_making_support()