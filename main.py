import streamlit as st
import pandas as pd
import time

# Service Imports
from services import db_manager, analytics, rules_engine, visualizations, ml_engine, report_gen

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Gov Waste Mgmt",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS ("Midnight Official" Theme)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Global Background and Text */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FAFAFA !important;
        font-family: 'Arial', sans-serif;
    }
    
    /* Custom Header Banner */
    .gov-header {
        background: linear-gradient(90deg, #002B5C 0%, #001f42 100%);
        padding: 1.5rem;
        border-bottom: 3px solid #D4AF37;
        margin-bottom: 2rem;
        border-radius: 4px;
        text-align: center;
    }
    .gov-title {
        color: #D4AF37;
        font-size: 2.2em;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
    }
    .gov-subtitle {
        color: #FAFAFA;
        font-size: 1.1em;
        margin-top: 5px;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #1E2329;
        border: 1px solid #D4AF37;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
    }
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        color: #D4AF37;
    }
    .metric-label {
        color: #FAFAFA;
        font-size: 0.9em;
        text-transform: uppercase;
    }
    </style>
    
    <div class="gov-header">
        <div class="gov-title">GOVERNMENT PAPER WASTE MANAGEMENT SYSTEM</div>
        <div class="gov-subtitle">Ministry of Environment & Administrative Reforms</div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------------------------------
st.sidebar.markdown("## 🏛️ Filter Controls")

# Departments & Months Lists
DEPARTMENTS = [
    "General Admin", "Finance", "Health", "Education", "Public Works", 
    "Revenue", "Legal", "HR", "IT/E-Gov", "Records & Archives"
]
MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]
YEARS = [str(y) for y in range(2000, 2030)] # 2000 to 2029

selected_dept = st.sidebar.multiselect("Select Department", DEPARTMENTS, default=DEPARTMENTS)
selected_month = st.sidebar.multiselect("Select Month", MONTHS, default=MONTHS)
selected_year = st.sidebar.multiselect("Select Year", YEARS, default=["2025", "2026"])

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
raw_df = db_manager.fetch_data()

# --- DATA CLEANING & YEAR HANDLING (User Patch) ---
if not raw_df.empty:
    # 1. Handle missing 'year' column by creating it
    if 'year' not in raw_df.columns:
        raw_df['year'] = '2025' # Initialize
    
    # 2. Convert created_at if exists
    if 'created_at' in raw_df.columns:
        raw_df['created_at'] = pd.to_datetime(raw_df['created_at'], errors='coerce')
        # Extract Year from created_at
        raw_df['year'] = raw_df['created_at'].dt.year.astype(str)
    
    # Ensure it's string for filtering
    if 'year' in raw_df.columns:
        raw_df['year'] = raw_df['year'].astype(str)
        # Handle NaN if any failures (default to 2025 as fallback only for corrupted rows)
        raw_df['year'] = raw_df['year'].replace('nan', '2025')
    else:
        # Fallback if no created_at
        raw_df['year'] = '2025'
# ------------------------------------------------

# Filter Data
filtered_df = raw_df.copy()

# DEBUG PRINTS
if not raw_df.empty:
    print(f"DEBUG: Unique Depts in DB: {raw_df['department'].unique()}")
    print(f"DEBUG: Unique Months in DB: {raw_df['month'].unique()}")

if not filtered_df.empty:
    # Ensure year column matches string for filtering
    if 'year' in filtered_df.columns:
        filtered_df['year'] = filtered_df['year'].astype(str)
        
    if selected_dept:
        filtered_df = filtered_df[filtered_df['department'].isin(selected_dept)]
    if selected_month:
        filtered_df = filtered_df[filtered_df['month'].isin(selected_month)]
    if selected_year and 'year' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['year'].isin(selected_year)]

    # Apply Logic
    filtered_df = rules_engine.apply_compliance_rules(filtered_df)
    
    # Calculate KPIs
    kpis = analytics.calculate_kpis(filtered_df)
else:
    kpis = {"total_paper_used": 0, "national_recycling_rate": 0, "sensitive_paper_stored": 0}
    filtered_df = pd.DataFrame(columns=["department", "month", "doc_type", "used_kg", "storage_kg", "recycled_kg", "reason", "Status", "Color"])


# -----------------------------------------------------------------------------
# AI FORECASTING & REPORTS
# -----------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("## 🤖 AI Forecasting & Reports")

target_dept = st.sidebar.selectbox("Select Dept for Report", DEPARTMENTS)
report_type = st.sidebar.radio("Report Type", ["Monthly", "Yearly"])

if st.sidebar.button("Generate AI Report"):
    # Filter data for this specific department
    st.sidebar.info(f"Generating for: {target_dept}")
    
    # Filter data for this specific department
    dept_data = raw_df[raw_df['department'] == target_dept]
    
    # Prediction
    predictor = ml_engine.WastePredictor()
    pred_val, warning, avg_usage = predictor.predict_next_month(dept_data)
    
    # Display Prediction Card in Sidebar
    st.sidebar.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Predicted Waste (Next Month)</div>
        <div class="metric-value">{pred_val} kg</div>
        <div style="font-size: 0.8em; color: {'#FF4B4B' if warning else '#00C853'}">
            {'⚠️ Limit Exceeded' if warning else '✅ Within Limits'}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate PDF
    try:
        pdf_bytes = report_gen.generate_dept_pdf(target_dept, dept_data, report_type)
        
        st.sidebar.download_button(
            label="📄 Download AI Report",
            data=pdf_bytes,
            file_name=f"{target_dept}_Waste_Report_{report_type}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.sidebar.error(f"Error generating report: {e}")





# -----------------------------------------------------------------------------
# TABS
# -----------------------------------------------------------------------------
tab1, tab2 = st.tabs(["📊 DASHBOARD", "📝 DATA ENTRY"])

with tab1:
    # --- Top Row: KPIs ---
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Paper Used</div>
            <div class="metric-value">{kpis['total_paper_used']} kg</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        val = kpis['national_recycling_rate']
        color = "#00C853" if val > 70 else "#FF4B4B" if val < 30 else "#FFA726"
        st.markdown(f"""
        <div class="metric-card" style="border-color: {color};">
            <div class="metric-label">National Recycling Rate</div>
            <div class="metric-value" style="color: {color};">{val}%</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Sensitive Paper Stored</div>
            <div class="metric-value">{kpis['sensitive_paper_stored']} kg</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Middle Row: Charts ---
    row2_1, row2_2 = st.columns([2, 1])
    
    with row2_1:
        st.markdown("### Departmental Performance")
        dept_agg = analytics.aggregate_by_dept(filtered_df)
        chart_bar = visualizations.plot_usage_vs_recycled(dept_agg)
        st.altair_chart(chart_bar, use_container_width=True)
        
    with row2_2:
        st.markdown("### Compliance Reasons")
        chart_pie = visualizations.plot_compliance_distribution(filtered_df)
        st.altair_chart(chart_pie)

    st.markdown("---")

    # --- Bottom Row: Data Table ---
    st.markdown("### 📋 Detailed Audit Logs")
    
    def color_status(val):
        color = "#FFA726" # Standard
        if val == "EXEMPT": color = "#2196F3"
        elif val == "NON-COMPLIANT": color = "#FF4B4B"
        elif val == "GOLD STANDARD": color = "#00C853"
        return f'background-color: {color}; color: black; font-weight: bold;'

    if not filtered_df.empty:
        # Display specific columns
        display_cols = ["id", "department", "month", "year", "doc_type", "used_kg", "recycled_kg", "reason", "Status"]
        # Handle case where id might not be in df if manually created or depending on db fetch
        cols_in_df = [c for c in display_cols if c in filtered_df.columns]
        
        st.dataframe(
            filtered_df[cols_in_df].style.map(color_status, subset=["Status"]),
            width=10000, # Using a large integer to force stretch if 'stretch' isn't supported for dataframe in this version, or relying on auto. 
            # Actually, let's try 'width="stretch"' as the warning explicitly suggested.
            # Warning: "For `use_container_width=True`, use `width='stretch'`."
        )
    else:
        st.info("No data available. Add entries in the Data Entry tab.")

    st.markdown("---")
    
    # --- New Section: AI & Predictive Analytics ---
    st.markdown("## 🤖 AI & Predictive Analytics")
    
    # Only run if we have data and departments (specifically aiming for specific dept analysis usually, but let's aggregate if multiple selected)
    # The requirement asks for "Predicted Waste for March 2026", usually context specific.
    # We will use 'raw_df' to get the full 2025 history for the model, filtered by selected departments.
    
    if not filtered_df.empty:
        # Prepare data for ML (filtered by selected departments in 'filtered_df', assuming it contains 2025/2026 mixed)
        # Note: filtered_df is already filtered by sidebar.
        # But for ML, we need 2025 specifically.
        
        # We need to act on the filtered selection.
        selected_depts_list = selected_dept if selected_dept else DEPARTMENTS
        
        # Get data for these departments
        ml_data = raw_df[raw_df['department'].isin(selected_depts_list)]
        
        predictor = ml_engine.WastePredictor()
        ml_result = predictor.train_and_predict(ml_data)
        
        if ml_result and ml_result["status"] != "No Data":
            pred_mars = ml_result["predicted_values"]["Mar"]
            limit_2025 = ml_result["sustainability_limit"]
            delta = pred_mars - limit_2025
            
            # 1. Metric Card
            c_ml_1, c_ml_2 = st.columns([1, 2])
            
            with c_ml_1:
                st.metric(
                    label="Predicted Waste (March 2026)", 
                    value=f"{pred_mars} kg", 
                    delta=f"{delta:.1f} kg vs 2025 Avg",
                    delta_color="inverse" # If positive (more waste), it's bad (red).
                )
                
                # Status Alert
                if ml_result["status"] == "⚠️ High Alert":
                    st.error(f"Status: {ml_result['status']}")
                else:
                    st.success(f"Status: {ml_result['status']}")

            with c_ml_2:
                # 2. Comparison Chart (Altair)
                # Prepare 2025 Line (Actual)
                df_train = ml_result["training_data"]
                df_train['Type'] = 'Actual 2025'
                
                # Prepare 2026 Prediction Line
                # Construct dataframe for Jan-Mar 2026
                pred_dict = ml_result["predicted_values"]
                df_pred = pd.DataFrame([
                    {"month": "Jan", "used_kg": pred_dict["Jan"], "Type": "Predicted 2026"},
                    {"month": "Feb", "used_kg": pred_dict["Feb"], "Type": "Predicted 2026"},
                    {"month": "Mar", "used_kg": pred_dict["Mar"], "Type": "Predicted 2026"}
                ])
                
                # Combine for chart
                # We need to order months correctly.
                # Just simplified plotting: Month on X, kg on Y, Color by Type.
                chart_data = pd.concat([
                    df_train[["month", "used_kg", "Type"]],
                    df_pred
                ])
                
                month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                
                chart_comparison = visualizations.plot_prediction_comparison(chart_data, month_order)
                st.altair_chart(chart_comparison, use_container_width=True)
                
        else:
            st.info("Insufficient 2025 data to generate predictions.")


with tab2:
    st.markdown("### 📝 Submit New Waste Audit")
    
    with st.form("entry_form"):
        c1, c2 = st.columns(2)
        
        with c1:
            dept_input = st.selectbox("Department", DEPARTMENTS)
            month_input = st.selectbox("Month", MONTHS)
            year_input = st.selectbox("Year", YEARS, index=25) # Default to 2025/2026 range
            doc_type_input = st.selectbox("Document Type", ["Bills", "Files", "Report", "Legal Records", "Confidential"])
        
        with c2:
            used_input = st.number_input("Paper Used (kg)", min_value=0.0, step=0.1)
            recycled_input = st.number_input("Paper Recycled (kg)", min_value=0.0, step=0.1)
            storage_input = st.number_input("Paper Stored (kg)", min_value=0.0, step=0.1)
        
        reason_input = st.selectbox("Reason for Storage/Non-Recycling", ["N/A", "Under Gov Retention Policy", "Confidential Records", "Pending Audit", "Other"])
        
        submitted = st.form_submit_button("Submit Audit Record")
        
        if submitted:
            # Validate business rule logic consistency if needed, but primary job is just to save
            new_entry = {
                "department": dept_input,
                "month": month_input,
                "year": year_input,
                "doc_type": doc_type_input,
                "doc_type": doc_type_input,
                "used_kg": used_input,
                "recycled_kg": recycled_input,
                "storage_kg": storage_input,
                "reason": reason_input
            }
            
            success, msg = db_manager.save_entry(new_entry)
            if success:
                st.success("Record submitted successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Failed to submit record: {msg}")
