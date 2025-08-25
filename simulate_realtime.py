import time
import pandas as pd
import requests
import numpy as np
import os

PCAP_CSV = r"data\dataset\UDPLag.csv"  
API_URL = "http://localhost:5000/api/traffic"
INTERVAL = 5  
BATCH_SIZE = 3  

if not os.path.exists(PCAP_CSV):
    raise FileNotFoundError(f"No se encontró el archivo: {PCAP_CSV}")

df = pd.read_csv(PCAP_CSV, low_memory=False)

if "Label" in df.columns:
    df = df.drop(columns=["Label"])
df = df.select_dtypes(include=[np.number])
df = df.replace([np.inf, -np.inf], 0).fillna(0)

expected = 75
if df.shape[1] < expected:
    for i in range(df.shape[1], expected):
        df[f"dummy_{i}"] = 0
elif df.shape[1] > expected:
    df = df.iloc[:, :expected]

print(f"[SIMULADOR] Iniciando simulación desde dataset: {PCAP_CSV}")
print(f"[SIMULADOR] Enviando a {API_URL} cada {INTERVAL}s, batch={BATCH_SIZE}")

idx = 0
while True:
    batch = df.iloc[idx: idx + BATCH_SIZE]
    if batch.empty:
        print("[SIMULADOR] Fin del dataset, reiniciando...")
        idx = 0
        continue

    data = batch.to_dict(orient="records")

    try:
        res = requests.post(API_URL, json=data, timeout=10)
        if res.status_code == 200:
            print("[SIMULADOR] Respuesta:", res.json())
        else:
            print(f"[SIMULADOR] Error {res.status_code} - {res.text}")
    except Exception as e:
        print("[SIMULADOR] Error al enviar:", str(e))

    idx += BATCH_SIZE
    time.sleep(INTERVAL)
