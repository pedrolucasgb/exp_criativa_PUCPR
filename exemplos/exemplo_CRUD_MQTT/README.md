# Sistema IoT com MQTT + Flask + MySQL

Sistema completo de gerenciamento de sensores IoT que **recebe automaticamente dados via MQTT** e salva no banco de dados MySQL. Inspirado no `exemplo_CRUD_BluePrint` com funcionalidade MQTT integrada.

## 📡 Funcionalidades Principais

### 🔐 Autenticação
- Sistema de login e registro
- Proteção de rotas com Flask-Login
- Senhas criptografadas

### 📊 CRUD de Sensores
- Cadastrar sensores com tópico MQTT
- Editar informações dos sensores
- Deletar sensores
- Ativar/Desativar sensores

### 🌐 Integração MQTT
- **Recebimento automático** de mensagens MQTT
- Salva leituras no banco de dados MySQL
- Suporte para múltiplos sensores
- Wildcard topics (`/sensores/#`)
- Aceita JSON ou valores diretos

### 📈 Visualização de Dados
- Dashboard com sensores cadastrados
- Leituras atuais de todos os sensores
- Histórico completo de leituras
- Histórico individual por sensor

## 🗄️ Estrutura do Banco de Dados

### Tabelas Criadas

```sql
users (
    id, username, email, password, created_at
)

sensors (
    id, name, brand, model, unit, topic, is_active, created_at, updated_at
)

sensor_readings (
    id, sensor_id, value, read_datetime, created_at
)
```

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
cd exemplos/exemplo_CRUD_MQTT
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados MySQL

Execute o script SQL:

```bash
mysql -u root -p < database.sql
```

Ou manualmente:

```sql
CREATE DATABASE sensor_system;
USE sensor_system;
```

Depois execute o conteúdo de `database.sql`.

### 3. Configurar Variáveis de Ambiente

Copie `.env.example` para `.env` e ajuste:

```env
# Banco de Dados
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=sensor_system

# MQTT
MQTT_BROKER_URL=mqtt-dashboard.com
MQTT_BROKER_PORT=1883
MQTT_TOPIC=/sensores/#
```

### 4. Executar Aplicação

```bash
python main.py
```

Acesse: `http://localhost:5000`

**Credenciais padrão:**
- Username: `admin`
- Password: `admin`

## 📡 Como Funciona o MQTT

### 1. Cadastrar Sensor

No dashboard, cadastre um sensor com:
- Nome: `Temperatura Sala 1`
- Marca: `DHT`
- Modelo: `DHT22`
- Unidade: `°C`
- **Tópico MQTT**: `/sensores/temp/sala1`

### 2. Enviar Dados via MQTT

O sistema escuta automaticamente mensagens MQTT. Envie dados no formato:

**Opção 1: JSON**
```json
{
  "value": 25.5
}
```

**Opção 2: JSON alternativo**
```json
{
  "valor": 25.5
}
```

**Opção 3: Valor direto**
```
25.5
```

### 3. Tópico MQTT

Publique no tópico **exato** do sensor:

```bash
mosquitto_pub -h mqtt-dashboard.com -t "/sensores/temp/sala1" -m '{"value": 25.5}'
```

### 4. Visualizar Dados

- **Dashboard**: Veja sensores cadastrados
- **Leituras Atuais**: Última leitura de cada sensor
- **Histórico**: Todas as leituras com timestamp
- **Histórico do Sensor**: Leituras de um sensor específico

## 📨 Formato de Mensagens MQTT

### JSON Completo
```json
{
  "value": 25.5,
  "timestamp": "2025-11-24T10:30:00"
}
```

### JSON Simples
```json
{
  "valor": 25.5
}
```

### Valor Direto
```
25.5
```

O sistema processa todos os formatos automaticamente!

## 🔧 Configuração MQTT

### Broker Público (Padrão)
```
Broker: mqtt-dashboard.com
Port: 1883
```

### Broker Privado
Edite `.env`:

```env
MQTT_BROKER_URL=seu.broker.com
MQTT_BROKER_PORT=1883
MQTT_USERNAME=usuario
MQTT_PASSWORD=senha
MQTT_TLS_ENABLED=False
```

## 📁 Estrutura de Arquivos

```
exemplo_CRUD_MQTT/
├── main.py                      # Aplicação principal com MQTT
├── requirements.txt             # Dependências
├── database.sql                 # Script SQL
├── .env.example                 # Exemplo de configuração
├── controllers/
│   ├── auth_controller.py       # Login/Registro
│   ├── sensor_controller.py     # CRUD de sensores
│   └── readings_controller.py   # Visualização de leituras
├── models/
│   ├── db.py                    # SQLAlchemy
│   ├── user.py                  # Model User
│   ├── sensor.py                # Model Sensor
│   └── sensor_reading.py        # Model SensorReading
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── register_sensor.html
│   ├── edit_sensor.html
│   ├── latest_readings.html     # Leituras atuais
│   ├── readings_history.html    # Histórico completo
│   └── sensor_readings.html     # Histórico por sensor
└── static/
    └── css/
        └── style.css
```

## 🎯 Fluxo de Dados

```
1. Sensor IoT → Publica MQTT → Broker
                                   ↓
2. Flask-MQTT ← Recebe mensagem ← Broker
       ↓
3. Model SensorReading.save_reading()
       ↓
4. MySQL Database (sensor_readings)
       ↓
5. Template → Visualização no Dashboard
```

## 💡 Exemplos de Uso

### Teste com Mosquitto

```bash
# Publicar temperatura
mosquitto_pub -h mqtt-dashboard.com -t "/sensores/temp/sala1" -m "25.5"

# Publicar umidade
mosquitto_pub -h mqtt-dashboard.com -t "/sensores/humidity/sala1" -m "60.3"

# Publicar JSON
mosquitto_pub -h mqtt-dashboard.com -t "/sensores/pressure/outdoor" -m '{"value": 1013.25}'
```

### Teste com Python (paho-mqtt)

```python
import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.connect("mqtt-dashboard.com", 1883)

# Enviar leitura
data = {"value": 25.5}
client.publish("/sensores/temp/sala1", json.dumps(data))
```

## 🐛 Troubleshooting

### Mensagens não estão sendo salvas

1. ✅ Verifique se o tópico MQTT do sensor está **exatamente igual**
2. ✅ Confirme que o sensor está **ativo** no dashboard
3. ✅ Veja os logs do terminal para erros
4. ✅ Teste conexão com o broker MQTT

### Erro de conexão MySQL

```
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")
```

**Solução:**
- Verifique se MySQL está rodando
- Confirme credenciais no `.env`
- Teste: `mysql -u root -p`

### Sensor não aparece

- Execute `database.sql` novamente
- Cadastre sensor manualmente no dashboard

## 📊 Recursos Extras

- ✅ Interface responsiva
- ✅ Mensagens flash coloridas
- ✅ Timestamps em todas as leituras
- ✅ Histórico ilimitado
- ✅ Suporte a múltiplos sensores
- ✅ Wildcards MQTT (`#`)
- ✅ Auto-reconnect MQTT
- ✅ Logs detalhados

## 🔐 Segurança

- Senhas com hash (Werkzeug)
- Proteção de rotas (@login_required)
- Validação de dados
- SQL Injection protection (SQLAlchemy ORM)
- MQTT TLS opcional

## 📚 Tecnologias

- **Flask** 3.0.0 - Framework web
- **Flask-Login** - Autenticação
- **Flask-SQLAlchemy** - ORM
- **Flask-MQTT** - Cliente MQTT
- **PyMySQL** - Driver MySQL
- **MySQL** - Banco de dados
- **python-dotenv** - Variáveis de ambiente

## 🚀 Próximas Melhorias

- [ ] Gráficos de leituras (Chart.js)
- [ ] Alertas quando valor ultrapassa limites
- [ ] API REST para dados
- [ ] WebSocket para atualização em tempo real
- [ ] Exportar dados para CSV
- [ ] Dashboard com estatísticas

## 📄 Licença

Projeto educacional para aprendizado de IoT, MQTT e Flask.

---

**Desenvolvido com Flask + MQTT + MySQL** 🚀📡
