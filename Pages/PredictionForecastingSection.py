import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import LSTM, Dense
from prophet import Prophet

def prediction_forecasting():
    st.title("Savings Prediction & Forecasting for Individual Employees")

    if 'uploaded_data' not in st.session_state:
        st.error("No data uploaded. Please upload a CSV file on the main page.")
        return
    data = st.session_state['uploaded_data']

    if 'Employee' in data.columns:
        unique_employees = data['Employee'].unique()
        selected_employee = st.selectbox("Select Employee for Predictions:", unique_employees)
        employee_data = data[data['Employee'] == selected_employee]

        if employee_data.empty:
            st.error("No data found for the selected employee.")
            return

        current_monthly_savings = employee_data['Savings for Property (£)'].iloc[0]
        current_monthly_expenses = employee_data['Monthly Income (£)'].iloc[0] - current_monthly_savings

        st.subheader("Initial Values (Month 1)")
        st.write(f"Savings: £{current_monthly_savings:.2f}")
        st.write(f"Expenses: £{current_monthly_expenses:.2f}")

        st.subheader("Input Changes for Next 5 Months")
        changes = []
        for i in range(5):
            col1, col2 = st.columns(2)
            with col1:
                savings_change = st.number_input(f"Month {i + 2} Savings Change", value=current_monthly_savings, step=10.0)
            with col2:
                expenses_change = st.number_input(f"Month {i + 2} Expenses Change", value=current_monthly_expenses, step=10.0)
            changes.append((savings_change, expenses_change))

        next_month = pd.Timestamp.now() + pd.DateOffset(months=1)
        next_month_start = next_month.replace(day=1)
        dates = pd.date_range(start=next_month_start, periods=5, freq='M')

        savings = [current_monthly_savings] * 5
        expenses = [current_monthly_expenses] * 5

        df = pd.DataFrame({'ds': dates, 'savings': savings, 'expenses': expenses})

        for i, (savings_change, expenses_change) in enumerate(changes):
            new_date = df['ds'].iloc[-1] + pd.DateOffset(months=i + 1)
            new_savings = df['savings'].iloc[-1] + savings_change - current_monthly_savings
            new_expenses = df['expenses'].iloc[-1] + expenses_change - current_monthly_expenses
            new_row = pd.DataFrame({'ds': [new_date], 'savings': [new_savings], 'expenses': [new_expenses]})
            df = pd.concat([df, new_row], ignore_index=True)

        predictions_summary = {}

        # ARIMA Model
        arima_model = ARIMA(df['savings'], order=(1, 1, 1))
        arima_results = arima_model.fit()
        arima_forecast = arima_results.forecast(steps=6)
        predictions_summary['ARIMA Forecast'] = arima_forecast.values.tolist()

        # LSTM Model
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df[['savings', 'expenses']])

        X, y = [], []
        for i in range(len(scaled_data) - 6):
            X.append(scaled_data[i:i + 6])
            y.append(scaled_data[i + 6])
        X, y = np.array(X), np.array(y)
        model = Sequential([
            LSTM(50, activation='relu', input_shape=(6, 2)),
            Dense(2)
        ])
        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=50, verbose=0)
        last_6_months = scaled_data[-6:]
        lstm_forecast = []

        for _ in range(6):
            next_month = model.predict(last_6_months.reshape(1, 6, 2))
            lstm_forecast.append(next_month[0])
            last_6_months = np.vstack((last_6_months[1:], next_month))
        lstm_forecast_inv_scaled = scaler.inverse_transform(lstm_forecast)
        predictions_summary['LSTM Forecast'] = lstm_forecast_inv_scaled[:, 0].tolist()

        # Prophet Model
        prophet_df = df[['ds', 'savings']].rename(columns={'savings': 'y'})
        m = Prophet()
        m.fit(prophet_df)
        future = m.make_future_dataframe(periods=2, freq='ME')
        forecast_prophet = m.predict(future)
        predictions_summary['Prophet Forecast'] = forecast_prophet['yhat'].tail(6).values.tolist()

        # Create DataFrame for plotting with adjusted future dates starting from five months from today
        future_dates_arima_lstm = pd.date_range(start=pd.Timestamp.now() + pd.DateOffset(months=5), periods=6, freq='M')

        plot_df = pd.DataFrame({
            'Date': future_dates_arima_lstm,
            'ARIMA Forecast': predictions_summary['ARIMA Forecast'],
            'LSTM Forecast': predictions_summary['LSTM Forecast'],
            'Prophet Forecast': predictions_summary['Prophet Forecast']
        })

        # Plotting using Plotly
        fig = px.line(plot_df, x='Date',
                      y=['ARIMA Forecast', 'LSTM Forecast', 'Prophet Forecast'],
                      labels={'value': 'Savings (£)', 'variable': 'Model'},
                      title=f"Savings Forecast for {selected_employee}")

        st.plotly_chart(fig)

        st.subheader("Predictions Summary for Savings")
        # summary with future dates
        plot_df['Date'] += pd.DateOffset(months=0)
        st.write(plot_df)
    else:
        st.warning("No 'Employee' column found in the data.")

if __name__ == "__main__":
    prediction_forecasting()
