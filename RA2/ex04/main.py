from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/sensors')
def sensors():
  return render_template('sensors.html')


@app.route('/actuators')
def actuators():
  actuators = {
    'rele': 'Relé',
    'servo': 'Servo',
    'led': 'LED'
  }
  return render_template('acturator.html', actuators=actuators)


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
  return render_template('item.html', title=title, room=room, name=name)


@app.route('/<room>/actuator/<name>')
def show_actuator(room, name):
  title = 'Atuador selecionado'
  return render_template('item.html', title=title, room=room, name=name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
