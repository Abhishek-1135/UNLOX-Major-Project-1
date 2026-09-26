import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_trends(path="trend_data.csv", periods=4):
    df = pd.read_csv(path)
    output = []
    for keyword, group in df.groupby("keyword"):
        group = group.sort_values("week").reset_index(drop=True)
        X = np.arange(len(group)).reshape(-1,1)
        y = group["trend_score"].values
        model = LinearRegression().fit(X, y)
        future_x = np.arange(len(group), len(group)+periods).reshape(-1,1)
        preds = model.predict(future_x)
        for i, pred in enumerate(preds, 1):
            output.append([keyword, i, round(float(pred),2)])
    return pd.DataFrame(output, columns=["keyword","future_week","forecast_score"])
