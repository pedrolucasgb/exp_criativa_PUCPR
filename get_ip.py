"""
Script auxiliar para descobrir o IP local do computador
"""
import socket

def get_local_ip():
    try:
        # Cria um socket UDP (não precisa realmente conectar)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Conecta a um endereço externo (não envia dados)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    ip = get_local_ip()
    print("=" * 50)
    print(f"🌐 IP do seu computador na rede local: {ip}")
    print("=" * 50)
    print("\n📝 Use este IP no código da ESP32:")
    print(f'   BROKER = "{ip}"')
    print("\n🔧 Também altere no ex_mqtt.py se necessário:")
    print(f'   mqtt_client.connect("{ip}", 1883)')
    print("=" * 50)
