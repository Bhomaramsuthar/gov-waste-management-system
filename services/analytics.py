import pandas as pd

def calculate_kpis(df):
    """
    Calculates high-level KPIs from the dataframe.
    """
    if df.empty:
        return {
            "total_paper_used": 0,
            "national_recycling_rate": 0,
            "sensitive_paper_stored": 0
        }

    total_used = df["used_kg"].sum()
    total_recycled = df["recycled_kg"].sum()
    
    # National Rate
    if total_used > 0:
        national_rate = (total_recycled / total_used) * 100
    else:
        national_rate = 0
        
    # Sensitive Paper Stored (Exempt items often imply storage of sensitive/confidential material)
    # Based on the requirement: Total "Sensitive/Confidential" Paper Stored (kg)
    # We look for doc_type="Confidential" or reason="Confidential Records"
    sensitive_mask = (df["doc_type"] == "Confidential") | (df["reason"] == "Confidential Records")
    sensitive_stored = df[sensitive_mask]["storage_kg"].sum()

    return {
        "total_paper_used": round(total_used, 2),
        "national_recycling_rate": round(national_rate, 1),
        "sensitive_paper_stored": round(sensitive_stored, 2)
    }

def aggregate_by_dept(df):
    """
    Aggregates data by department for visualization.
    """
    if df.empty:
        return pd.DataFrame(columns=["department", "used_kg", "recycled_kg"])
        
    agg = df.groupby("department")[["used_kg", "recycled_kg"]].sum().reset_index()
    return agg

def aggregate_reasons(df):
    """
    Counts reasons for compliance distribution.
    """
    if df.empty:
        return pd.DataFrame(columns=["reason", "count"])
    
    # We are interested in "Reasons for Non-Recycling" which maps to the 'reason' column 
    # broadly, or specifically where recycling is low. 
    # The prompt says: "Donut Chart: Reasons for Non-Recycling (Compliance distribution)."
    # We will just count the 'reason' column values.
    
    return df["reason"].value_counts().reset_index().rename(columns={"index": "reason", "reason": "count", "count": "count"})
