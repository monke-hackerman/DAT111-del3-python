import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import os

# Initialize and train finno model
if os.path.exists("output.csv"):
    df = pd.read_csv("output.csv").copy()
    
    # Filter out extreme outliers (houseing market be like) if necessary
    df = df[df['m2'] > 0]
    
    # Predicts price per m2 directly (in 1000 of NOK per m2)
    X = df[['x', 'y', 'm2', 'house_type', 'standard']]
    y = (df['sales_price'] / df['m2']) / 1000.0  
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
else:
    model = None

def predict_price(x, y, m2, house_type, standard):
    if model is not None:
        # Predict price per m2
        pred_price_per_m2 = model.predict([[x, y, m2, house_type, standard]])[0]
        return float(pred_price_per_m2 * m2)
    else:
        # When output is missing
        base_price_per_m2 = 55.0  # in 1000
        return float(m2 * base_price_per_m2 * (standard / 2.0))