import pandas as pd

file_path = 'personal_finance_employees_V1.csv'
finance_data = pd.read_csv(file_path)

# Calculate the mean of the "Water Bill (£)" and "Monthly Outing (£)" column, ignoring NaN values
water_bill_avg = finance_data['Water Bill (£)'].mean()
monthly_bill_avg = finance_data['Monthly Outing (£)'].mean()

# Fill NaN values with the calculated average
finance_data['Water Bill (£)'] = finance_data['Water Bill (£)'].fillna(water_bill_avg)
finance_data['Sky Sports (£)'] = finance_data['Sky Sports (£)'].fillna(0)
finance_data['Other Expenses (£)'] = finance_data['Other Expenses (£)'].fillna(0)
finance_data['Savings for Property (£)'] = finance_data['Savings for Property (£)'].fillna(0)
finance_data['Monthly Outing (£)'] = finance_data['Monthly Outing (£)'].fillna(monthly_bill_avg)

# Save the modified dataset to a new file
output_file_path = 'personal_finance_employees_filled.csv'
finance_data.to_csv(output_file_path, index=False)
