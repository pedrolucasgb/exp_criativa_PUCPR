"""
Script de diagnóstico para verificar configuração MQTT
"""
import socket
import subprocess
import sys

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Erro: {e}"

def check_port(host, port):
    """Verifica se uma porta está aberta"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

def check_mosquitto_installed():
    """Verifica se Mosquitto está instalado"""
    try:
        result = subprocess.run(
            ["mosquitto", "-h"], 
            capture_output=True, 
            text=True,
            timeout=3
        )
        return True
    except:
        return False

def check_mosquitto_running():
    """Verifica se Mosquitto está rodando"""
    try:
        result = subprocess.run(
            ["netstat", "-an"], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        return ":1883" in result.stdout
    except:
        return False

print("=" * 60)
print("🔍 DIAGNÓSTICO MQTT - ESP32 + Flask")
print("=" * 60)

# 1. IP Local
print("\n📡 1. ENDEREÇO IP LOCAL:")
ip = get_local_ip()
print(f"   IP: {ip}")

# 2. Mosquitto instalado?
print("\n🦟 2. MOSQUITTO:")
mosquitto_installed = check_mosquitto_installed()
if mosquitto_installed:
    print("   ✅ Mosquitto está instalado")
else:
    print("   ❌ Mosquitto NÃO está instalado")
    print("   📥 Baixe em: https://mosquitto.org/download/")

# 3. Mosquitto rodando?
mosquitto_running = check_mosquitto_running()
if mosquitto_running:
    print("   ✅ Mosquitto está RODANDO na porta 1883")
else:
    print("   ❌ Mosquitto NÃO está rodando")
    print("   💡 Execute: mosquitto -v")

# 4. Porta 1883 acessível?
print("\n🔌 3. CONECTIVIDADE:")
localhost_ok = check_port("127.0.0.1", 1883)
if localhost_ok:
    print("   ✅ Porta 1883 acessível em localhost")
else:
    print("   ❌ Porta 1883 NÃO acessível em localhost")

if isinstance(ip, str) and not ip.startswith("Erro"):
    ip_ok = check_port(ip, 1883)
    if ip_ok:
        print(f"   ✅ Porta 1883 acessível em {ip}")
    else:
        print(f"   ❌ Porta 1883 NÃO acessível em {ip}")

# 5. Recomendações
print("\n" + "=" * 60)
print("📋 PRÓXIMOS PASSOS:")
print("=" * 60)

if not mosquitto_installed:
    print("\n1️⃣ INSTALAR MOSQUITTO:")
    print("   • Baixe: https://mosquitto.org/download/")
    print("   • Instale (versão Windows)")
    print("   • Reinicie este script")

elif not mosquitto_running:
    print("\n1️⃣ INICIAR MOSQUITTO:")
    print("   Opção A - Terminal separado:")
    print("   mosquitto -v")
    print()
    print("   Opção B - Como serviço Windows:")
    print("   net start mosquitto")

else:
    print("\n✅ TUDO CONFIGURADO!")
    print("\n📝 Use estas configurações:")
    print(f"\n   No Flask (ex_mqtt.py):")
    print(f'   mqtt_client.connect("localhost", 1883)')
    print(f"\n   Na ESP32:")
    print(f'   BROKER = "{ip}"')

print("\n" + "=" * 60)
