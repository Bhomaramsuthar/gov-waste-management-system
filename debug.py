import streamlit as st
import os

st.title("🕵️ Secrets Debugger")

# 1. Check if file exists
file_path = ".streamlit/secrets.toml"
if os.path.exists(file_path):
    st.success(f"✅ Found secrets file at: {file_path}")
else:
    st.error(f"❌ Could not find file at: {file_path}")
    st.info("Make sure you are running this command from the 'Edunet' folder!")

# 2. Check if Streamlit can read it
try:
    url = st.secrets["supabase"]["url"]
    st.success("✅ Successfully read [supabase] URL!")
    st.write(f"URL starts with: {url[:15]}...")
except FileNotFoundError:
    st.error("❌ Streamlit cannot find the secrets file.")
except KeyError:
    st.error("❌ File found, but missing [supabase] header or keys.")
    st.code("[supabase]\nurl = '...'\nkey = '...'", language="toml")
    