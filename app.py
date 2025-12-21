import streamlit as st
import pandas as pd

st.set_page_config(page_title="Microloan Matchmaking", layout="wide")
st.title("💸 Microloan Matchmaking Web App")

# Initialize session state
if "borrowers" not in st.session_state:
    st.session_state.borrowers = []
if "lenders" not in st.session_state:
    st.session_state.lenders = []

# Tabs for Borrower, Lender, Matches
tab1, tab2, tab3 = st.tabs(["Register Borrower","Register Lender","View Matches"])

# --- Tab 1: Borrower Registration ---
with tab1:
    st.header("Borrower Registration")
    b_name = st.text_input("Name", key="b_name")
    b_amount = st.number_input("Loan Amount Needed", min_value=0)
    b_interest = st.number_input("Max Interest Rate (%)", min_value=0.0, max_value=100.0)
    b_purpose = st.selectbox("Loan Purpose", ["Business", "Education", "Medical", "Other"])
    if st.button("Register Borrower"):
        st.session_state.borrowers.append({
            "Name": b_name,
            "Amount": b_amount,
            "MaxInterest": b_interest,
            "Purpose": b_purpose
        })
        st.success(f"Borrower {b_name} registered!")

# --- Tab 2: Lender Registration ---
with tab2:
    st.header("Lender Registration")
    l_name = st.text_input("Name", key="l_name")
    l_funds = st.number_input("Available Funds", min_value=0)
    l_interest = st.number_input("Min Interest Rate (%)", min_value=0.0, max_value=100.0)
    l_purpose = st.selectbox("Preferred Loan Purpose", ["Any", "Business", "Education", "Medical", "Other"])
    if st.button("Register Lender"):
        st.session_state.lenders.append({
            "Name": l_name,
            "Funds": l_funds,
            "MinInterest": l_interest,
            "Purpose": l_purpose
        })
        st.success(f"Lender {l_name} registered!")

# --- Tab 3: View Matches ---
with tab3:
    st.header("Potential Matches")
    matches = []
    for borrower in st.session_state.borrowers:
        for lender in st.session_state.lenders:
            # Match logic
            if (borrower["Amount"] <= lender["Funds"] and
                borrower["MaxInterest"] >= lender["MinInterest"] and
                (lender["Purpose"] == "Any" or lender["Purpose"] == borrower["Purpose"])):
                matches.append({
                    "Borrower": borrower["Name"],
                    "Lender": lender["Name"],
                    "Amount": borrower["Amount"],
                    "Interest": max(borrower["MaxInterest"], lender["MinInterest"]),
                    "Purpose": borrower["Purpose"]
                })
    if matches:
        st.table(pd.DataFrame(matches))
    else:
        st.info("No matches found yet.")
