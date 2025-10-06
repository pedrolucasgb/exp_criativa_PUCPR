from flask import Flask, render_template

app = Flask(__name__)

# Example dictionaries to represent sensors and actuators state
sensores = {'Umidade': 22, 'Temperatura': 23, 'Luminosidade': 1034}
atuadores = {'Interruptor': 'off', 'Lampada': 'on', 'Rele': 'off'}


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/sensors')
def sensors():
  return render_template('sensors.html', sensores=sensores)


@app.route('/actuators')
def actuators():
  return render_template('acturator.html', actuators=atuadores)


@app.route('/quarto')
def quarto():
  items = [('/quarto/sensor/luminosidade', 'Sensor de luminosidade'),
       ('/quarto/actuator/interruptor', 'Interruptor')]
  return render_template('room.html', room_name='Quarto', items=items)


@app.route('/banheiro')
def banheiro():
  items = [('/banheiro/sensor/umidade', 'Sensor de umidade'),
       ('/banheiro/actuator/lampada', 'Lâmpada inteligente')]
  return render_template('room.html', room_name='Banheiro', items=items)


@app.route('/<room>/sensor/<name>')
def show_sensor(room, name):
  title = 'Sensor selecionado'
  # try to find value by name (case-insensitive key match)
  value = None
  for k, v in sensores.items():
    if k.lower() == name.lower() or k.lower() == name.replace('-', ' ').lower():
      value = v
      break
  return render_template('item.html', title=title, room=room, name=name, value=value)


@app.route('/<room>/actuator/<name>')
def show_actuator(room, name):
  title = 'Atuador selecionado'
  # try to find actuator state by name
  state = None
  for k, v in atuadores.items():
    if k.lower() == name.lower() or k.lower() == name.replace('-', ' ').lower():
      state = v
      break
  return render_template('item.html', title=title, room=room, name=name, state=state)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
