import streamlit as st
from supabase import create_client

# Load secrets
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]

# Connect
supabase = create_client(url, key)

# Insert a fake test record
data = {
    "department": "Test Dept",
    "month": "Jan",
    "doc_type": "Test",
    "used_kg": 10.5
}
response = supabase.table("waste_logs").insert(data).execute()

print("✅ Success! Data inserted:", response.data)