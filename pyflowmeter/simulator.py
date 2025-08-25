import time
import requests
import json
import subprocess
import os

class Simulator:
    def __init__(self):
        pass

    def simulate_from_file(self, pcap_path, server_url, interval=5):
        """
        Simula tráfico leyendo un archivo PCAP y enviando los flujos al backend.

        pcap_path: Ruta al archivo .pcap
        server_url: URL del endpoint del backend (ej. http://localhost:5000/api/traffic)
        interval: Intervalo de envío en segundos
        """

        if not os.path.exists(pcap_path):
            print(f"Error: El archivo {pcap_path} no existe.")
            return

        print(f"[SIMULADOR] Iniciando simulación desde: {pcap_path}")
        print(f"[SIMULADOR] Enviando datos a: {server_url}")
        print(f"[SIMULADOR] Intervalo: {interval} segundos")

        # En el TFG original aquí se ejecutaba PyFlowmeter modificado para extraer features
        # Como no tenemos esa versión, simularemos datos para pruebas

        fake_flows = [
            {"flow_id": "flow_1", "feature1": 0.12, "feature2": 0.88},
            {"flow_id": "flow_2", "feature1": 0.33, "feature2": 0.45},
            {"flow_id": "flow_3", "feature1": 0.55, "feature2": 0.66}
        ]

        while True:
            try:
                print(f"[SIMULADOR] Enviando {len(fake_flows)} flujos...")
                r = requests.post(server_url, json=fake_flows)
                print(f"[SIMULADOR] Respuesta del servidor: {r.status_code} - {r.text}")
            except Exception as e:
                print(f"[SIMULADOR] Error al enviar datos: {e}")

            time.sleep(interval)
