from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)
CORS(app)

with open("model/firewall_xgb.pkl", "rb") as f:
    model = pickle.load(f)
print("[INFO] Modelo XGBoost cargado correctamente")

try:
    model_features = model.get_booster().feature_names
    if not model_features:
        model_features = None
except Exception:
    model_features = None
    print("[WARN] El modelo no tiene feature_names, se usará detección por tamaño.")

EXPECTED_N = getattr(model, "n_features_in_", 75)

LABEL_MAP = {
    0: "Normal",
    1: "Ataque DDoS",
    2: "Inyección SQL",
    3: "PortScan",
    4: "Botnet"
}

last_predictions = []

def prepare_df(flows):
    df = pd.DataFrame(flows)

    if "Label" in df.columns:
        df = df.drop(columns=["Label"])

    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    df = df.select_dtypes(include=[np.number])

    if model_features:
        overlap = [c for c in model_features if c in df.columns]
        overlap_ratio = len(overlap) / len(model_features)
        print(f"[DEBUG] Overlap con features del modelo: {len(overlap)}/{len(model_features)} ({overlap_ratio:.0%})")
        if overlap_ratio >= 0.6:  # umbral razonable
            missing = [c for c in model_features if c not in df.columns]
            if missing:
                for c in missing:
                    df[c] = 0.0
                print(f"[WARN] Añadidas columnas faltantes (relleno 0): {len(missing)}")
            df = df[model_features]
            return df

    if df.shape[1] < EXPECTED_N:
        for i in range(df.shape[1], EXPECTED_N):
            df[f"dummy_{i}"] = 0.0
    elif df.shape[1] > EXPECTED_N:
        df = df.iloc[:, :EXPECTED_N]
    print(f"[DEBUG] Usando fallback por tamaño: {df.shape[1]} columnas (esperadas {EXPECTED_N})")
    return df

@app.route("/api/traffic", methods=["POST"])
def traffic_post():
    global last_predictions
    try:
        flows = request.get_json()
        if not flows:
            return jsonify({"error": "No se recibieron datos"}), 400

        df = prepare_df(flows)
        print(f"[DEBUG] Shape final para el modelo: {df.shape}")

        preds = model.predict(df)
        proba = model.predict_proba(df)

        results = []
        for i, pred in enumerate(preds):
            label = LABEL_MAP.get(int(pred), str(pred))
            conf = float(np.max(proba[i])) if proba is not None else None
            results.append({"flow_id": int(i), "type": label, "confidence": conf})

        last_predictions = results
        return jsonify({"predictions": results}), 200

    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/api/traffic", methods=["GET"])
def traffic_get():
    return jsonify({"predictions": last_predictions})

@app.route("/api/labels", methods=["GET"])
def labels():
    return jsonify(LABEL_MAP)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
