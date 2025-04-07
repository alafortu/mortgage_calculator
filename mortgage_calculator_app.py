import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Mortgage Calculator", layout="wide")

st.title("Mortgage Calculator")

# Sidebar inputs
st.sidebar.header("Mortgage Parameters")

mortgage_amount = st.sidebar.number_input("Mortgage Amount ($)", min_value=10000, max_value=10000000, value=300000, step=1000)
annual_interest_rate = st.sidebar.number_input("Annual Interest Rate (%)", min_value=0.1, max_value=20.0, value=5.0, step=0.1)
amortization_years = st.sidebar.number_input("Amortization Period - Years", min_value=0, max_value=35, value=25, step=1)
amortization_months = st.sidebar.number_input("Amortization Period - Months", min_value=0, max_value=11, value=0, step=1)
term_years = st.sidebar.number_input("Term (Years)", min_value=1, max_value=10, value=5, step=1)

payment_frequency = st.sidebar.selectbox(
    "Payment Frequency",
    ("Monthly", "Bi-Weekly", "Weekly", "Accelerated Bi-Weekly", "Accelerated Weekly")
)

double_payment = st.sidebar.checkbox("Double Payments", value=False)

# Frequency mapping
freq_map = {
    "Monthly": 12,
    "Bi-Weekly": 26,
    "Weekly": 52,
    "Accelerated Bi-Weekly": 26,
    "Accelerated Weekly": 52
}

payments_per_year = freq_map[payment_frequency]

# Adjust interest rate per period
periodic_interest_rate = (annual_interest_rate / 100) / payments_per_year

# Total number of payments over amortization
total_months = amortization_years * 12 + amortization_months
total_payments = total_months * payments_per_year / 12

# Calculate payment amount
if periodic_interest_rate > 0:
    payment = mortgage_amount * (periodic_interest_rate * (1 + periodic_interest_rate) ** total_payments) / ((1 + periodic_interest_rate) ** total_payments - 1)
else:
    payment = mortgage_amount / total_payments

# Adjust for accelerated payments (roughly equivalent to extra monthly payment per year)
if "Accelerated" in payment_frequency:
    payment = payment * 12 / payments_per_year

# Double payment option
if double_payment:
    payment *= 2

st.subheader("Payment Details")
st.write(f"**Regular Payment:** ${payment:,.2f} per period")
st.write(f"**Total Payments:** {total_payments}")
st.write(f"**Total Payment Amount:** ${payment * total_payments:,.2f}")

# Generate amortization schedule
balance = mortgage_amount
schedule = []

n = 1
while balance > 0:
    interest_payment = balance * periodic_interest_rate
    principal_payment = payment - interest_payment
    if principal_payment > balance:
        principal_payment = balance
        payment = interest_payment + principal_payment  # adjust last payment
    balance -= principal_payment
    # Stop before appending if balance is effectively zero
    if balance < 1e-6:
        balance = 0
        # Append final payment info
        schedule.append({
            "Payment #": n,
            "Payment": payment,
            "Principal": principal_payment,
            "Interest": interest_payment,
            "Balance": balance
        })
        break
    # Otherwise, append payment info
    schedule.append({
        "Payment #": n,
        "Payment": payment,
        "Principal": principal_payment,
        "Interest": interest_payment,
        "Balance": balance
    })
    n += 1

df = pd.DataFrame(schedule)

# Tabs for visualization
tab1, tab2, tab3 = st.tabs(["Reimbursement Histogram", "Amortization Table", "Balance Over Time"])

with tab1:
    st.subheader("Principal vs Interest Over Time")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df["Payment #"], df["Principal"], label="Principal", color="tab:blue")
    ax.bar(df["Payment #"], df["Interest"], bottom=df["Principal"], label="Interest", color="tab:orange")
    ax.set_xlabel("Payment Number")
    ax.set_ylabel("Amount ($)")
    ax.legend()
    st.pyplot(fig)

with tab2:
    st.subheader("Amortization Schedule")
    st.dataframe(df.style.format({
        "Payment": "${:,.2f}",
        "Principal": "${:,.2f}",
        "Interest": "${:,.2f}",
        "Balance": "${:,.2f}"
    }), use_container_width=True)

with tab3:
    st.subheader("Remaining Balance Over Time (Year-End)")
    years = []
    balances = []
    total_years = int(np.ceil(len(df) / payments_per_year))
    for year in range(1, total_years + 1):
        payment_idx = year * payments_per_year - 1
        if payment_idx >= len(df):
            payment_idx = len(df) - 1
        years.append(year)
        balances.append(df.iloc[payment_idx]["Balance"])
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(years, balances, marker='o')
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Remaining Balance ($)")
    ax2.set_title("Mortgage Balance at End of Each Year")
    ax2.grid(True)
    st.pyplot(fig2)