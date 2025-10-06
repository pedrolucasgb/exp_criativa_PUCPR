from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return """
<html>
  <head><title>Minha Casa - Menu Principal</title></head>
  <body>
    <h2>Minha Casa</h2>
    <h3>Menu Principal:</h3>
    <ul>
      <li><a href="/quarto">Quarto</a></li>
      <li><a href="/banheiro">Banheiro</a></li>
    </ul>
  </body>
</html>
"""


@app.route('/quarto')
def quarto():
    return """
<html>
  <head><title>Quarto</title></head>
  <body>
    <h2>Quarto</h2>
    <h3>Escolha:</h3>
    <ul>
      <li><a href="/quarto/sensor/luminosidade">Sensor de luminosidade</a></li>
      <li><a href="/quarto/actuator/interruptor">Interruptor</a></li>
    </ul>
    <p><a href="/">Voltar ao menu</a></p>
  </body>
</html>
"""


@app.route('/banheiro')
def banheiro():
    return """
<html>
  <head><title>Banheiro</title></head>
  <body>
    <h2>Banheiro</h2>
    <h3>Escolha:</h3>
    <ul>
      <li><a href="/banheiro/sensor/umidade">Sensor de umidade</a></li>
      <li><a href="/banheiro/actuator/lampada">Lâmpada inteligente</a></li>
    </ul>
    <p><a href="/">Voltar ao menu</a></p>
  </body>
</html>
"""


@app.route('/<room>/sensor/<name>')
def show_sensor(room, name):
    # Simple page showing the selected sensor name and a back link
    return f"""
<html>
  <head><title>Sensor</title></head>
  <body>
    <h2>Sensor selecionado</h2>
    <p>Comodo: {room}</p>
    <p>Sensor: {name}</p>
    <p><a href="/{room}">Voltar</a></p>
    <p><a href="/">Menu Principal</a></p>
  </body>
</html>
"""


@app.route('/<room>/actuator/<name>')
def show_actuator(room, name):
    # Simple page showing the selected actuator name and a back link
    return f"""
<html>
  <head><title>Atuador</title></head>
  <body>
    <h2>Atuador selecionado</h2>
    <p>Comodo: {room}</p>
    <p>Atuador: {name}</p>
    <p><a href="/{room}">Voltar</a></p>
    <p><a href="/">Menu Principal</a></p>
  </body>
</html>
"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
