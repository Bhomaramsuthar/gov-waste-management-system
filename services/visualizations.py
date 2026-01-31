import altair as alt
import pandas as pd

# Color Palette
GOLD = "#D4AF37"
NAVY = "#002B5C"
OFF_WHITE = "#FAFAFA"
BG_COLOR = "#0E1117" # Matching app background for seamless look, or transparent

def plot_usage_vs_recycled(df_agg):
    """
    Bar Chart: Paper Used vs. Recycled per Department.
    """
    if df_agg.empty:
        return alt.Chart(pd.DataFrame({"x":[]})).mark_bar()

    # Melt for grouped bar chart structure
    df_melt = df_agg.melt("department", var_name="Type", value_name="Kilograms")
    
    chart = alt.Chart(df_melt).mark_bar().encode(
        x=alt.X("department", axis=alt.Axis(title="Department", labelColor=OFF_WHITE, titleColor=OFF_WHITE)),
        y=alt.Y("Kilograms", axis=alt.Axis(title="Weight (kg)", labelColor=OFF_WHITE, titleColor=OFF_WHITE)),
        xOffset="Type:N", # Grouped Bar Chart logic
        color=alt.Color("Type", scale=alt.Scale(domain=["used_kg", "recycled_kg"], range=[NAVY, GOLD]), legend=alt.Legend(title="Metric", labelColor=OFF_WHITE, titleColor=OFF_WHITE)),
        tooltip=["department", "Type", "Kilograms"]
    ).properties(
        title=alt.TitleParams("Paper Used vs. Recycled", color=GOLD),
        background="transparent"
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        gridColor="#333333"
    )
    
    return chart

def plot_compliance_distribution(df):
    """
    Donut Chart: Reasons for Non-Recycling (Compliance distribution).
    """
    if df.empty:
        return alt.Chart(pd.DataFrame({"x":[]})).mark_arc()
        
    reason_counts = df["reason"].value_counts().reset_index()
    # rename columns to ensure consistency regardless of pandas version
    reason_counts.columns = ["reason", "count"]
    
    base = alt.Chart(reason_counts).encode(
        theta=alt.Theta("count", stack=True)
    )
    
    
    # Custom color scale to match the theme
    domain_reasons = ["N/A", "Under Gov Retention Policy", "Confidential Records", "Pending Audit", "Other"]
    range_colors = ["#FFA726", "#2196F3", "#002B5C", "#FF4B4B", "#D4AF37"]
    
    pie = base.mark_arc(outerRadius=80, innerRadius=50).encode(
        color=alt.Color("reason", scale=alt.Scale(domain=domain_reasons, range=range_colors), legend=alt.Legend(title="Reason", labelColor=OFF_WHITE, titleColor=OFF_WHITE)),
        tooltip=["reason", "count"]
    ).properties(
        title=alt.TitleParams("Reasons for Non-Recycling", color=GOLD),
        background="transparent"
    )
    
    return pie

def plot_compliance_rates(df):
    """
    Extra: Scatter plot or similar if needed. Not strictly requested but useful.
    For now, adhering strictly to requested charts.
    """
    pass

def plot_prediction_comparison(data, month_order):
    """
    Dual-Line Chart: Actual 2025 vs Predicted 2026.
    """
    base = alt.Chart(data).encode(
        x=alt.X("month", sort=month_order, axis=alt.Axis(title="Month", labelColor=OFF_WHITE, titleColor=OFF_WHITE)),
        y=alt.Y("used_kg", axis=alt.Axis(title="Waste (kg)", labelColor=OFF_WHITE, titleColor=OFF_WHITE)),
        color=alt.Color("Type", scale=alt.Scale(domain=['Actual 2025', 'Predicted 2026'], range=['#2196F3', '#FF4B4B']), legend=alt.Legend(title="Type", labelColor=OFF_WHITE, titleColor=OFF_WHITE))
    )
    
    line = base.mark_line().encode(
        strokeDash=alt.condition(
            alt.datum.Type == 'Predicted 2026',
            alt.value([5, 5]),  # Dotted for prediction
            alt.value([0])      # Solid for actual
        )
    )
    
    points = base.mark_point(filled=True, size=60)
    
    return (line + points).properties(
        title=alt.TitleParams("2025 Actual vs 2026 Prediction", color=GOLD),
        background="transparent"
    )
