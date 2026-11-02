import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, RidgeCV
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error

FEATURE_COLS = ["x", "y", "m2", "house_type", "standard"]
CATEGORICAL_FEATURES = ["house_type", "standard"]

def build_and_train_model():    
    global model
    df:DataFrame = pd.read_csv("output.csv")
    X = df[FEATURE_COLS].copy()
    y = df["sales_price"].values

    x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
    )

    model = HistGradientBoostingRegressor(
        categorical_features=CATEGORICAL_FEATURES,
        random_state=42,
        max_iter=200,
        learning_rate=0.05,
        min_samples_leaf=15
    )
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    for i in range(0, min(len(y_test),10)):
        print(f"Price: {y_test[i]:>10,.0f}  Predicted: {y_pred[i]:>10,.0f}")
    print(f"R-squared: {r2_score(y_test, y_pred):.2f}")
    print(f"MAE      : {mean_absolute_error(y_test, y_pred):.0f}")

def predict_price(x, y, m2:int,house_type, standard) -> float:
    x_house = pd.DataFrame(
        [[x, y, m2, house_type, standard]], 
        columns=FEATURE_COLS
    )
    pred = model.predict(x_house)[0]
    return float(pred)


y_columns=["x","y","m2","house_type","standard"]
p_degree = 3
model = LinearRegression()

poly = PolynomialFeatures(degree=p_degree)
build_and_train_model()

print(f"m2  {predict_price(100,100, 200,1, 1)}") # just test one..
