import pandas as pd
import requests
import numpy as np

df = pd.read_csv(r"data\dataset\UDPLag.csv", nrows=5, low_memory=False)
df = df.apply(pd.to_numeric, errors="coerce")

if "Label" in df.columns:
    df = df.drop(columns=["Label"])

df = df.select_dtypes(include=[np.number])

df = df.replace([np.inf, -np.inf], 0)
df = df.fillna(0)

expected = 75
if df.shape[1] < expected:
    for i in range(df.shape[1], expected):
        df[f"dummy_{i}"] = 0
elif df.shape[1] > expected:
    df = df.iloc[:, :expected]

data = df.to_dict(orient="records")

url = "http://localhost:5000/api/traffic"
res = requests.post(url, json=data)

print("[RESPUESTA]", res.status_code)
print(res.json())
