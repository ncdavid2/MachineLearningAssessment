import pandas as pd

file_path = 'personal_finance_employees_V1.csv'
finance_data = pd.read_csv(file_path)

# Calculate the mean of the "Water Bill (£)" column, ignoring NaN values
water_bill_avg = finance_data['Water Bill (£)'].mean()

# Fill NaN values in "Water Bill (£)" with the calculated average
finance_data['Water Bill (£)'] = finance_data['Water Bill (£)'].fillna(water_bill_avg)
finance_data['Sky Sports (£)'] = finance_data['Sky Sports (£)'].fillna(0)

# Save the modified dataset to a new file
output_file_path = 'personal_finance_employees_filled.csv'
finance_data.to_csv(output_file_path, index=False)
