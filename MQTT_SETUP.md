# 🔧 Configuração MQTT - Flask + ESP32

## 📋 Pré-requisitos

1. **Instalar um broker MQTT** (escolha uma opção):
   - **Mosquitto** (recomendado): https://mosquitto.org/download/
   - **EMQX**: https://www.emqx.io/downloads

2. **Instalar dependências Python**:
   ```bash
   pip install flask paho-mqtt
   ```

## 🚀 Passo a Passo

### 1️⃣ Descobrir o IP do seu computador na rede local

Execute no PowerShell:
```powershell
ipconfig
```

Procure por **"Adaptador de Rede sem Fio Wi-Fi"** ou **"Ethernet"** e anote o **IPv4**, por exemplo: `192.168.0.105`

### 2️⃣ Iniciar o broker MQTT

**Se instalou Mosquitto:**
```powershell
mosquitto -v
```

Ou configure como serviço do Windows para iniciar automaticamente.

### 3️⃣ Atualizar o código da ESP32

No código da ESP32, troque:
```python
BROKER = "localhost"
```

Por:
```python
BROKER = "192.168.0.105"  # ⬅️ Cole o IP do SEU computador aqui
```

### 4️⃣ Executar o servidor Flask

```powershell
python ex_mqtt.py
```

### 5️⃣ Gravar o código na ESP32

Use Thonny, uPyCraft ou ampy para enviar o código MicroPython para a ESP32.

### 6️⃣ Testar

- Acesse no navegador: `http://localhost:5000/`
- Você verá os dados de temperatura e umidade sendo atualizados!

## 🧪 Testando sem ESP32

Você pode simular publicações MQTT usando o terminal:

```powershell
# Publicar temperatura
mosquitto_pub -h localhost -t "esp32/temperatura" -m "25"

# Publicar umidade
mosquitto_pub -h localhost -t "esp32/umidade" -m "60"
```

## 🔍 Verificando se está funcionando

1. O broker MQTT deve mostrar conexões
2. O terminal do Flask deve mostrar as mensagens recebidas
3. A ESP32 deve imprimir no console serial: "Conectado ao broker MQTT!"

## ⚠️ Problemas comuns

### ESP32 não conecta ao WiFi
- Verifique o SSID e senha
- Certifique-se que a ESP32 está dentro do alcance do WiFi

### ESP32 não conecta ao broker MQTT
- Verifique se o broker está rodando: `netstat -an | findstr 1883`
- Confirme que o IP está correto (não use "localhost" na ESP32!)
- Verifique o firewall do Windows

### Dados não aparecem no Flask
- Verifique se os tópicos estão corretos
- Teste com `mosquitto_pub` primeiro
