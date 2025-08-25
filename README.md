# 🛡️ Firewall-AI

Este proyecto implementa un **sistema de detección de ataques de denegación de servicio (DoS/DDoS)** basado en **Inteligencia Artificial**.  
El sistema captura tráfico de red, lo procesa y clasifica en tiempo real mediante modelos de **Machine Learning / Deep Learning**, principalmente **XGBoost**, entrenado con datasets de flujos de red.

---

## 📂 Estructura del proyecto

Firewall-AI/
├── backend/ # API en Flask (detección y predicciones)
│ ├── app.py
│ └── model/firewall_xgb.pkl
│
├── frontend/ # Interfaz en Vue.js
│ ├── src/views
│ ├── src/components
│ └── src/router
│
├── data/dataset/ # Datasets CSV para pruebas
│ ├── DrDoS_DNS.csv
│ └── UDPLag.csv
│
├── simulate_traffic.py # Simulador de tráfico (desde CSV o PCAP)
├── test_prediction.py # Script de pruebas rápidas
└── venv310/ # Entorno virtual de Python 3.10

yaml
Copiar
Editar

---

## ⚙️ Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/TU_USUARIO/Firewall-AI.git
cd Firewall-AI
2. Crear entorno virtual
En Windows (PowerShell):

bash
Copiar
Editar
py -3.10 -m venv venv310
.\venv310\Scripts\activate
3. Instalar dependencias
bash
Copiar
Editar
pip install --upgrade pip
pip install -r requirements.txt
⚠️ Si alguna librería falla en Windows (ej. pyflowmeter), usar la versión adaptada:
pip install git+https://github.com/DavidRamosArchilla/pyflowmeter.git

🚀 Ejecución
1. Iniciar backend (Flask)
bash
Copiar
Editar
cd backend
python app.py
Servidor activo en: http://localhost:5000

2. Probar predicciones rápidas
bash
Copiar
Editar
python test_prediction.py
Ejemplo de salida:

json
Copiar
Editar
{
  "predictions": [
    {"flow_id": 0, "type": "Normal", "confidence": 0.95},
    {"flow_id": 1, "type": "DDoS Attack", "confidence": 0.99}
  ]
}
3. Simular tráfico desde PCAP/CSV
bash
Copiar
Editar
python simulate_traffic.py
Envía tráfico en intervalos al endpoint /api/traffic.

4. Iniciar frontend (Vue.js)
bash
Copiar
Editar
cd frontend/firewall-frontend
npm install
npm run serve
Disponible en: http://localhost:8080

📊 Dataset
El sistema se entrenó y probó con datasets de ataques DDoS de la University of New Brunswick (CIC-DDoS2019).
Los CSV procesados deben colocarse en la carpeta:

bash
Copiar
Editar
data/dataset/
🧠 Modelo de IA
Algoritmo principal: XGBoost (Gradient Boosting)

Precisión obtenida en validación: 99%

El modelo entrenado se encuentra en:

bash
Copiar
Editar
backend/model/firewall_xgb.pkl
🖼️ Resultados esperados
Backend prediciendo ataques en tiempo real.

Frontend mostrando tráfico con etiquetas Normal / Ataque.

Simulador reproduciendo flujos desde datasets o PCAP.
