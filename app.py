import numpy as np
import streamlit as st

st.set_page_config(page_title="Expense Tracker", layout="centered")

st.title("💰 Expense Tracker Dashboard")

st.write("Analyze your daily spending using NumPy-powered analytics.")

# -------------------------------
# Generate Expenses
# -------------------------------
st.header("📅 Generate Expenses")

n_days = st.number_input("Number of Days", min_value=1, value=30)

if st.button("Generate Expenses"):
    categories_list = np.array(
        ["Food", "Transport", "Shopping", "Bills", "Entertainment"]
    )

    days = np.array([f"Day {i+1}" for i in range(int(n_days))])
    expenses = np.random.randint(100, 2001, size=int(n_days))
    categories = np.random.choice(categories_list, size=int(n_days))

    data = np.column_stack((days, expenses, categories))

    st.session_state["data"] = data

# Display Table
if "data" in st.session_state:
    st.subheader("📋 Expense Table")
    st.dataframe(st.session_state["data"], use_container_width=True)


# -------------------------------
# Summary
# -------------------------------
st.header("📊 Expense Summary")

def expense_summary(data):
    expenses = data[:, 1].astype(float)

    total = np.sum(expenses)
    avg = np.mean(expenses)

    highest_idx = np.argmax(expenses)
    highest_day = data[highest_idx, 0]
    highest_amount = expenses[highest_idx]

    above_avg = np.sum(expenses > avg)

    return total, avg, highest_day, highest_amount, above_avg


if st.button("Compute Summary"):
    if "data" not in st.session_state:
        st.error("Generate data first!")
    else:
        data = st.session_state["data"]

        total, avg, highest_day, highest_amount, above_avg = expense_summary(data)

        st.write(f"**Total Spending:** ₹{total:.2f}")
        st.write(f"**Average Daily Spending:** ₹{avg:.2f}")

        st.write("---")
        st.write(f"**Highest Spending Day:** {highest_day} — ₹{highest_amount:.2f}")

        st.write("---")
        st.write(f"**Days Above Average:** {above_avg}")


# -------------------------------
# Category Breakdown
# -------------------------------
st.header("🗂 Category Breakdown")

def category_breakdown(data):
    categories = data[:, 2]
    expenses = data[:, 1].astype(float)

    unique = np.unique(categories)
    totals = {}

    for cat in unique:
        totals[cat] = np.sum(expenses[categories == cat])

    highest = max(totals, key=totals.get)
    lowest = min(totals, key=totals.get)

    return totals, highest, lowest


if st.button("Analyze Categories"):
    if "data" not in st.session_state:
        st.error("Generate data first!")
    else:
        data = st.session_state["data"]

        totals, highest, lowest = category_breakdown(data)

        for cat, val in totals.items():
            st.write(f"**{cat}** — ₹{val:.2f}")

        st.write("---")
        st.write(f"**Highest Spending Category:** {highest}")
        st.write(f"**Lowest Spending Category:** {lowest}")


# -------------------------------
# High Spending Filter
# -------------------------------
st.header("🔥 High Spending Days")

threshold = st.number_input("Threshold (₹)", value=1500)

def high_spending(data, threshold):
    expenses = data[:, 1].astype(float)
    days = data[:, 0]

    mask = expenses > threshold
    return days[mask], expenses[mask]


if st.button("Find High Spending Days"):
    if "data" not in st.session_state:
        st.error("Generate data first!")
    else:
        data = st.session_state["data"]

        filtered_days, filtered_expenses = high_spending(data, threshold)

        if len(filtered_days) == 0:
            st.warning("No days exceeded the threshold.")
        else:
            for d, e in zip(filtered_days, filtered_expenses):
                st.write(f"{d} — ₹{e:.2f}")
