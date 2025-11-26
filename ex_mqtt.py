from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt

# ---------------- CONFIG ----------------
BROKER = "broker.mqttdashboard.com"
TOPIC_SEND = "exp.criativas/pcparaesp"      # PC → ESP
TOPIC_RECEIVE = "exp.criativas/espparapc"   # ESP → PC

# Armazena último dado enviado pelo ESP
ultimo_dado = {"msg": None}

app = Flask(__name__)

# ------------- CALLBACK MQTT ---------------

def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker, código:", rc)
    client.subscribe(TOPIC_RECEIVE)

def on_message(client, userdata, msg):
    global ultimo_dado
    payload = msg.payload.decode()
    print("Recebido:", payload)
    ultimo_dado["msg"] = payload

# ------------- CONFIGURA CLIENTE MQTT ----------------

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883)
client.loop_start()  # roda em background

# ---------------- ROTAS FLASK ----------------

@app.route("/")
def index():
    return jsonify({
        "status": "online",
        "ultimo_dado": ultimo_dado["msg"]
    })

@app.route("/enviar", methods=["POST"])
def enviar_msg():
    """
    Envia uma mensagem para o ESP32
    Exemplo de uso:
    POST /enviar
    { "mensagem": "status" }
    """
    data = request.json
    if not data or "mensagem" not in data:
        return jsonify({"erro": "Você precisa enviar um JSON com 'mensagem'"}), 400

    mensagem = data["mensagem"]
    client.publish(TOPIC_SEND, mensagem)
    return jsonify({"enviado": mensagem})

@app.route("/dados")
def pegar_dados():
    """Retorna a última mensagem recebida do ESP"""
    return jsonify({"ultimo_dado": ultimo_dado["msg"]})

# ------------- INICIAR SERVIDOR --------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
