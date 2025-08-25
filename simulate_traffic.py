import time
import requests
import pandas as pd
from scapy.all import rdpcap
import json

# Configuración
API_URL = "http://localhost:5000/api/traffic"
PCAP_FILE = r"pcap/PCAP-01-12_0500-0749/SAT-01-12-2018_0500.pcap"
INTERVAL = 5  # segundos entre envíos

def extract_flows_from_pcap(pcap_file, max_flows=5):
    """
    Ejemplo de extracción simplificada de flujos desde un pcap.
    ⚠️ Aquí deberías usar pyflowmeter o un parser real.
    """
    try:
        packets = rdpcap(pcap_file)
        flows = []
        for i, pkt in enumerate(packets[:max_flows]):
            flow = {
                "src_port": getattr(pkt.payload, "sport", 0),
                "dst_port": getattr(pkt.payload, "dport", 0),
                "pkt_len": len(pkt),
                "flow_duration": i * 10  # Dummy feature
            }
            flows.append(flow)
        return flows
    except Exception as e:
        print(f"[ERROR] No se pudieron extraer flujos del pcap: {e}")
        return []

def main():
    print(f"[SIMULADOR] Iniciando simulación desde: {PCAP_FILE}")
    print(f"[SIMULADOR] Enviando datos a: {API_URL}")
    print(f"[SIMULADOR] Intervalo: {INTERVAL} segundos")

    while True:
        flows = extract_flows_from_pcap(PCAP_FILE, max_flows=5)

        if not flows:
            print("[SIMULADOR] No se extrajeron flujos, esperando...")
            time.sleep(INTERVAL)
            continue

        print(f"[SIMULADOR] Enviando {len(flows)} flujos...")
        try:
            res = requests.post(API_URL, json=flows)
            if res.status_code == 200:
                data = res.json()
                for p in data.get("predictions", []):
                    print(f"   ➡️ Flow {p['flow_id']}: {p['label']} "
                          f"(confianza: {p['confidence']:.2f})")
            else:
                print(f"[SIMULADOR] Error {res.status_code}: {res.text}")
        except Exception as e:
            print(f"[SIMULADOR] Error al enviar datos: {e}")

        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
