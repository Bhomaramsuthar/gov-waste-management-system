import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# Initialize connection
def init_connection():
    """
    Initializes Supabase connection using Streamlit secrets.
    """
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        # Check if we are in a dev environment without secrets
        # For safety, we return None and let the app handle the error state gracefully
        return None

def fetch_data():
    """
    Fetches all data from the 'waste_logs' table.
    """
    supabase = init_connection()
    if not supabase:
        st.error("Database connection failed. Please check secrets.")
        return pd.DataFrame()

    try:
        response = supabase.table("waste_logs").select("*").execute()
        data = response.data
        if data:
            print(f"DEBUG: Fetched {len(data)} rows from DB.") # Debug
            return pd.DataFrame(data)
        else:
            print("DEBUG: Fetched 0 rows (empty response).") # Debug
            return pd.DataFrame()
    except Exception as e:
        print(f"DEBUG: Error in fetch_data: {e}") # Debug
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def save_entry(entry_data):
    """
    Inserts a new record into 'waste_logs'.
    Handling historical data: Constructs 'created_at' from 'year' if provided.
    """
    supabase = init_connection()
    if not supabase:
        return False, "Database connection failed"

    try:
        # Handle Year logic to prevent "Column not found" error
        # Pop 'year' so it doesn't get sent to DB (which lacks the column)
        target_year = entry_data.pop("year", None) 
        target_month = entry_data.get("month", "Jan")
        
        if target_year:
            # Construct created_at from Year/Month
            month_map = {
                "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
            }
            m_num = month_map.get(target_month, "01")
            
            # Create timestamp: YYYY-MM-01 T10:00:00
            entry_data["created_at"] = f"{target_year}-{m_num}-01T10:00:00"
        else:
            # Fallback to current time
            entry_data["created_at"] = datetime.now().isoformat()
        
        response = supabase.table("waste_logs").insert(entry_data).execute()
        return True, "Success"
    except Exception as e:
        return False, str(e)
