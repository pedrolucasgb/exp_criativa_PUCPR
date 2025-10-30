from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# secret key for flash messages (only for development)
app.secret_key = 'dev-secret'

# simple user store: username -> password
users = {
  'admin': 'admin',
  'pedro': 'senha123',
  'guest': 'guest'
}

# Example dictionaries to represent sensors and actuators state
sensores = {'Umidade': 22, 'Temperatura': 23, 'Luminosidade': 1034}
# actuators values: 1 = ligado, 0 = desligado
atuadores = {'Interruptor': 1, 'Lampada': 1, 'Rele': 0}


@app.route('/')
def index():
  # render home with actions
  return render_template('home.html')


@app.route('/register_user')
def register_user():
  return render_template('register_user.html')


@app.route('/add_user', methods=['POST'])
def add_user():
  username = request.form.get('username')
  password = request.form.get('password')
  if not username or not password:
    flash('Usuário e senha são obrigatórios')
    return redirect(url_for('register_user'))
  if username in users:
    flash('Usuário já existe')
    return redirect(url_for('register_user'))
  users[username] = password
  flash('Usuário cadastrado com sucesso')
  return redirect(url_for('list_users'))


@app.route('/list_users')
def list_users_view():
  return render_template('list_users.html', users=users)


@app.route('/remove_user')
def remove_user():
  # placeholder: simple remove via query ?username=foo
  username = request.args.get('username')
  if username and username in users:
    users.pop(username)
    flash(f'Usuário {username} removido')
  else:
    flash('Informe ?username=<nome> para remover')
  return redirect(url_for('list_users_view'))


@app.route('/login')
def login():
  return render_template('login.html')


@app.route('/validate_user', methods=['POST'])
def validate_user():
  username = request.form.get('username')
  password = request.form.get('password')
  if not username or not password:
    flash('Por favor preencha usuário e senha')
    return redirect(url_for('login'))

  expected = users.get(username)
  if expected and expected == password:
    # sucesso (sem sessão real) — redireciona para dashboard
    return redirect(url_for('dashboard', user=username))
  else:
    flash('Usuário ou senha inválidos')
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
  user = request.args.get('user', 'desconhecido')
  return render_template('dashboard.html', user=user)


@app.route('/sensors')
def sensors():
  return render_template('sensors.html', sensores=sensores)


@app.route('/register_sensor')
def register_sensor():
  return render_template('register_sensor.html')


@app.route('/add_sensor', methods=['POST'])
def add_sensor():
  name = request.form.get('name')
  value = request.form.get('value')
  if not name:
    flash('Nome do sensor é obrigatório')
    return redirect(url_for('register_sensor'))
  try:
    val = float(value) if value else 0
  except ValueError:
    flash('Valor inválido')
    return redirect(url_for('register_sensor'))
  sensores[name] = val
  flash('Sensor cadastrado')
  return redirect(url_for('list_sensors'))


@app.route('/list_sensors')
def list_sensors():
  return render_template('list_sensors.html', sensores=sensores)


@app.route('/remove_sensor')
def remove_sensor():
  name = request.args.get('name')
  if name and name in sensores:
    sensores.pop(name)
    flash(f'Sensor {name} removido')
  else:
    flash('Informe ?name=<nome> para remover')
  return redirect(url_for('list_sensors'))


@app.route('/register_actuator')
def register_actuator():
  return render_template('register_actuator.html')


@app.route('/add_actuator', methods=['POST'])
def add_actuator():
  name = request.form.get('name')
  state = request.form.get('state')
  if not name:
    flash('Nome do atuador é obrigatório')
    return redirect(url_for('register_actuator'))
  try:
    st = int(state)
    if st not in (0, 1):
      raise ValueError()
  except Exception:
    flash('Estado inválido: informe 0 ou 1')
    return redirect(url_for('register_actuator'))
  atuadores[name] = st
  flash('Atuador cadastrado')
  return redirect(url_for('list_actuators'))


@app.route('/list_actuators')
def list_actuators():
  return render_template('list_actuators.html', actuators=atuadores)


@app.route('/remove_actuator')
def remove_actuator():
  name = request.args.get('name')
  if name and name in atuadores:
    atuadores.pop(name)
    flash(f'Atuador {name} removido')
  else:
    flash('Informe ?name=<nome> para remover')
  return redirect(url_for('list_actuators'))


@app.route('/actuators')
def actuators():
  return render_template('acturator.html', actuators=atuadores)


@app.route('/quarto')
def quarto():
  items = [('/quarto/sensor/luminosidade', 'Sensor de luminosidade'),
    ('/quarto/actuator/interruptor', 'Interruptor')]
  # items: label -> url
  items = {
    'Sensor de luminosidade': '/quarto/sensor/luminosidade',
    'Interruptor': '/quarto/actuator/interruptor'
  }
  return render_template('room.html', room_name='Quarto', items=items)


@app.route('/banheiro')
def banheiro():
  items = [('/banheiro/sensor/umidade', 'Sensor de umidade'),
    ('/banheiro/actuator/lampada', 'Lâmpada inteligente')]
  items = {
    'Sensor de umidade': '/banheiro/sensor/umidade',
    'Lâmpada inteligente': '/banheiro/actuator/lampada'
  }
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


@app.route('/<room>/devices/sensors')
def room_sensors(room):
  # pick sensors for the room (same example data)
  devices = sensores
  return render_template('sensors.html', sensores=devices, room_name=room)


@app.route('/<room>/devices/actuators')
def room_actuators(room):
  devices = atuadores
  return render_template('acturator.html', actuators=devices, room_name=room)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
