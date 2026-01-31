import pandas as pd

def check_compliance(row):
    """
    Determines compliance status and color based on waste data.
    """
    reason = row.get("reason", "N/A")
    used = row.get("used_kg", 0)
    recycled = row.get("recycled_kg", 0)

    # Rule 1: Exemptions
    if reason in ["Confidential Records", "Under Gov Retention Policy"]:
        return "EXEMPT", "#2196F3" # Blue

    # Avoid division by zero
    if used == 0:
        return "N/A", "#808080"
    
    recycling_rate = (recycled / used) * 100

    # Rule 3: Non-Compliant
    if recycling_rate < 30:
        return "NON-COMPLIANT", "#FF4B4B" # Red
    
    # Rule 4: Gold Standard
    if recycling_rate > 70:
        return "GOLD STANDARD", "#00C853" # Green
    
    # Rule 5: Standard
    return "STANDARD", "#FFA726" # Orange

def apply_compliance_rules(df):
    """
    Applies compliance logic to a dataframe and adds 'Status' and 'Color' columns.
    """
    if df.empty:
        df["Status"] = []
        df["Color"] = []
        return df

    results = df.apply(check_compliance, axis=1)
    # unzip results
    df["Status"] = [res[0] for res in results]
    df["Color"] = [res[1] for res in results]
    return df
