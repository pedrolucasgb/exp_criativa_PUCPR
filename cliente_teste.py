"""
Script para testar o envio de mensagens para o ESP32
"""
import requests

# URL do servidor Flask
BASE_URL = "http://127.0.0.1:5000"

def enviar_mensagem(msg):
    """Envia uma mensagem para o ESP32"""
    try:
        response = requests.post(
            f"{BASE_URL}/enviar",
            json={"mensagem": msg}
        )
        print(f"✅ Resposta: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")

def ver_dados():
    """Consulta os últimos dados recebidos do ESP"""
    try:
        response = requests.get(f"{BASE_URL}/dados")
        print(f"📊 Dados: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")

def ver_status():
    """Verifica o status do servidor"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"🔍 Status: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 TESTE DO SERVIDOR MQTT")
    print("=" * 50)
    
    # Testa o status
    print("\n1. Verificando status...")
    ver_status()
    
    # Envia uma mensagem
    print("\n2. Enviando mensagem 'status'...")
    enviar_mensagem("status")
    
    # Envia outra mensagem
    print("\n3. Enviando mensagem 'ligar_led'...")
    enviar_mensagem("ligar_led")
    
    # Consulta dados recebidos
    print("\n4. Consultando dados recebidos do ESP...")
    ver_dados()
    
    print("\n" + "=" * 50)
    print("✅ Teste concluído!")
    print("=" * 50)
