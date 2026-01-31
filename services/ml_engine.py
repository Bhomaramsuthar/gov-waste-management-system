
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class WastePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.month_map = {
            "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
            "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
        }

    def train_and_predict(self, df_dept):
        """
        Trains on 2025 data and predicts Jan, Feb, March of 2026.
        """
        # 1. Filter for 2025 Data (Training Set)
        # Ensure year column exists and is string '2025'
        if 'year' not in df_dept.columns:
            return None 
            
        df_2025 = df_dept[df_dept['year'] == '2025'].copy()
        
        if df_2025.empty:
            return {
                "predicted_values": {"Jan": 0, "Feb": 0, "Mar": 0},
                "sustainability_limit": 0,
                "status": "No Data"
            }

        # 2. Add Month Number
        df_2025['month_num'] = df_2025['month'].map(self.month_map)
        df_2025 = df_2025.sort_values('month_num')

        # 3. Train Model
        X = df_2025[['month_num']].values
        y = df_2025['used_kg'].values
        
        if len(X) > 0:
            self.model.fit(X, y)
        else:
             return {
                "predicted_values": {"Jan": 0, "Feb": 0, "Mar": 0},
                "sustainability_limit": 0,
                "status": "Insufficient Data"
            }

        # 4. Predict 2026 (Jan=13, Feb=14, Mar=15 relative to start
        future_months = np.array([[13], [14], [15]]) 
        predictions = self.model.predict(future_months)
        
        # Clip negative predictions to 0
        predictions = np.maximum(predictions, 0)
        
        pred_dict = {
            "Jan": round(predictions[0], 2),
            "Feb": round(predictions[1], 2),
            "Mar": round(predictions[2], 2)
        }

        # 5. Sustainability Limit (Baseline = 2025 Average)
        limit_2025 = round(y.mean(), 2)

        # 6. Status Check (March Prediction vs Limit)
        # "High Alert" if March > 1.1 * limit
        march_pred = pred_dict["Mar"]
        if march_pred > (1.1 * limit_2025):
            status = "⚠️ High Alert"
        else:
            status = "✅ Sustainable"

        return {
            "predicted_values": pred_dict,
            "sustainability_limit": limit_2025,
            "status": status,
            "training_data": df_2025 # Returning for visualization convenience
        }

    def predict_next_month(self, df_dept):
        """
        Legacy wrapper for PDF generation compatibility.
        Predicts 'Next Month' (mapping to March 2026 for consistency with new logic).
        Returns: (predicted_value, compliance_warning, avg_usage)
        """
        result = self.train_and_predict(df_dept)
        
        if not result or result["status"] in ["No Data", "Insufficient Data"]:
            return 0.0, False, 0.0
            
        # Use March prediction as the "Next Month" / Target prediction
        pred_val = result["predicted_values"]["Mar"]
        warning = result["status"] == "⚠️ High Alert"
        avg_usage = result["sustainability_limit"]
        
        return pred_val, warning, avg_usage
