import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import os
from sklearn.metrics import r2_score, mean_absolute_error

# Path to training data
file_path = "output.csv"

# Initialize and train te finno model
# Checks for the output.csv data, and if it has data
if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    df = pd.read_csv(file_path).copy()
    
    # Filter out extreme outliers (houseing market be like) if necessary
    df = df[df['m2'] > 0]
    
    # Predicts price per m2 directly (in 1000 of NOK per m2)
    feature_columns = ['x', 'y', 'm2', 'house_type', 'standard']
    X = df[feature_columns]
    y = (df['sales_price'] / df['m2']) / 1000.0  


    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Test the model and gv R^2 and MAE scores
    y_pred = model.predict(X)
    
    print(f"Model2, R-squared: {r2_score(y, y_pred):.2f}")
    print(f"Model2, MAE      : {mean_absolute_error(y, y_pred):.0f}")
else:
    # If porblems with reading data 
    model = None
    feature_columns = ['x', 'y', 'm2', 'house_type', 'standard']

def predict_price(x, y, m2, house_type, standard):
    if model is not None:
        # Create a DataFrame with column names to match training data and avoid warnings
        input_data = pd.DataFrame([[x, y, m2, house_type, standard]], columns=feature_columns)
        pred_price_per_m2 = model.predict(input_data)[0]
        return float(pred_price_per_m2 * m2)
    else:
        # When output is missing
        base_price_per_m2 = 55.0  # in 1000
        return float(m2 * base_price_per_m2 * (standard / 2.0))