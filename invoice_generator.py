import streamlit as st
import io

st.set_page_config(page_title="Professional Invoice Maker", layout="wide")

# --- STEP 1: INITIALIZATION (Error Fix) ---
if 'items' not in st.session_state:
    st.session_state.items = [{"desc": "NEW BODY 7 FIT", "qty": 1, "rate": 30000.0}] # Example item

st.title("📑 Professional Sales Invoice Maker")

# --- Sidebar Setup ---
with st.sidebar:
    st.header("🏢 Business Info")
    company = st.text_input("Company Name", "MG MOTORS")
    logo = st.file_uploader("Upload Logo", type=['png', 'jpg'])

# --- Main Layout ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("👤 Customer Details")
    customer = st.text_input("Name", "AGARWAL ENTERPRISE")
    mobile = st.text_input("Mobile", "9998944200")

with col2:
    st.subheader("📄 Invoice Info")
    inv_no = st.text_input("Invoice Number", "495")
    inv_date = st.date_input("Date")

# --- Items Section (Where the error was) ---
st.subheader("🛒 Items & Services")

# Loop through items securely
for i, item in enumerate(st.session_state.items):
    c1, c2, c3 = st.columns([3, 1, 1])
    # Unique keys add karna zaroori hai error se bachne ke liye
    st.session_state.items[i]['desc'] = c1.text_input(f"Desc {i}", item['desc'], key=f"d_{i}")
    st.session_state.items[i]['qty'] = c2.number_input(f"Qty {i}", value=item['qty'], key=f"q_{i}")
    st.session_state.items[i]['rate'] = c3.number_input(f"Rate {i}", value=item['rate'], key=f"r_{i}")

if st.button("➕ Add Another Item"):
    st.session_state.items.append({"desc": "", "qty": 1, "rate": 0.0})
    st.rerun() # Page refresh to show new row
