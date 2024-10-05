import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

# app title
st.title("mortgage calculator")

# input data
st.write("## Enter your details")

# user inputs
home_value1 = st.slider("Home Price", min_value=0, max_value=1000000)

col1, col2 = st.columns(2)

home_value = col1.number_input("Home Value", min_value=0, value=500000)
deposit = col1.number_input("Deposit", min_value=0, value=100000)
annual_interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, value=5.5)
loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)

# calculations
loan_principal = home_value - deposit
monthly_interest_rate = (annual_interest_rate/100)/12
number_of_payments = loan_term * 12
monthly_payment = (loan_principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1))

# display section
user_monthly_payment = monthly_payment
total_payments = monthly_payment * number_of_payments
total_interest_amount = total_payments - loan_principal

st.write("## Repayments")
col1, col2, col3 = st.columns(3)
col1.metric("monthly payment", user_monthly_payment)
col2.metric("total payments", total_payments)
col3.metric("total interest", total_interest_amount)


schedule = []
remaining_balance = loan_principal

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)  # Calculate the year into the loan
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)
# Display the data-frame as a chart.
st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.bar_chart(payments_df)
