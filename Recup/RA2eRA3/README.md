# Sistema de Gerenciamento de Sensores IoT com Flask

Sistema completo de gerenciamento de sensores IoT com autenticação de usuários e operações CRUD, utilizando Flask e MySQL.

## 📋 Funcionalidades

### Autenticação
- ✅ Sistema de login e registro de usuários
- ✅ Proteção de rotas com Flask-Login
- ✅ Senhas criptografadas com hash
- ✅ Mensagens flash para feedback ao usuário

### CRUD de Sensores
- ✅ **Create** - Cadastrar novos sensores
- ✅ **Read** - Visualizar lista de sensores no dashboard
- ✅ **Update** - Editar informações dos sensores
- ✅ **Delete** - Remover sensores do sistema

### Dados do Sensor
Cada sensor contém:
- Nome
- Marca
- Modelo
- Unidade de medida
- Tópico MQTT
- Status (Ativo/Inativo)

## 🗄️ Estrutura do Banco de Dados MySQL

### Tabela: users
```sql
- id (INT, PRIMARY KEY, AUTO_INCREMENT)
- username (VARCHAR(50), UNIQUE, NOT NULL)
- email (VARCHAR(100), UNIQUE, NOT NULL)
- password (VARCHAR(256), NOT NULL)
- created_at (TIMESTAMP)
```

### Tabela: sensors
```sql
- id (INT, PRIMARY KEY, AUTO_INCREMENT)
- name (VARCHAR(100), NOT NULL)
- brand (VARCHAR(50), NOT NULL)
- model (VARCHAR(50), NOT NULL)
- unit (VARCHAR(20), NOT NULL)
- topic (VARCHAR(100), NOT NULL)
- is_active (BOOLEAN, DEFAULT TRUE)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

## 🚀 Como Configurar e Executar

### 1. Pré-requisitos
- Python 3.8 ou superior
- MySQL Server instalado e rodando
- pip (gerenciador de pacotes Python)

### 2. Instalar Dependências

```bash
cd RA3/ex24
pip install -r requirements.txt
```

### 3. Configurar o Banco de Dados MySQL

#### Opção A: Usando o script SQL fornecido
```bash
# No MySQL, execute:
mysql -u root -p < database.sql
```

O script criará:
- Banco de dados `sensor_system`
- Tabelas `users` e `sensors`
- Usuário admin padrão
- Alguns sensores de exemplo

#### Opção B: Criar manualmente
```sql
CREATE DATABASE sensor_system;
USE sensor_system;
```

Depois execute o conteúdo do arquivo `database.sql`.

### 4. Configurar Variáveis de Ambiente (Opcional)

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_NAME=sensor_system
SECRET_KEY=chave-secreta-aleatoria
```

Se não criar o arquivo `.env`, o sistema usará valores padrão.

### 5. Executar a Aplicação

```bash
python main.py
```

A aplicação estará disponível em: `http://localhost:5000`

### 6. Fazer Login

**Credenciais padrão:**
- **Usuário:** admin
- **Senha:** admin

## 📁 Estrutura de Arquivos

```
ex24/
├── main.py                    # Arquivo principal da aplicação
├── requirements.txt           # Dependências Python
├── database.sql              # Script SQL para criar banco
├── .env.example              # Exemplo de configuração
├── controllers/
│   ├── auth_controller.py    # Rotas de autenticação
│   └── sensor_controller.py  # Rotas CRUD de sensores
├── models/
│   ├── db.py                 # Configuração SQLAlchemy
│   ├── user.py               # Model User
│   └── sensor.py             # Model Sensor
├── templates/
│   ├── base.html             # Template base
│   ├── login.html            # Página de login
│   ├── register.html         # Página de registro
│   ├── dashboard.html        # Dashboard principal
│   ├── register_sensor.html  # Cadastro de sensor
│   └── edit_sensor.html      # Edição de sensor
└── static/
    └── css/
        └── style.css         # Estilos CSS
```

## 🎯 Como Usar

### 1. Acessar o Sistema
- Abra `http://localhost:5000` no navegador
- Faça login com as credenciais padrão ou crie uma nova conta

### 2. Gerenciar Sensores

#### Adicionar Sensor
1. No dashboard, clique em "Adicionar Sensor"
2. Preencha os campos:
   - Nome do Sensor
   - Marca
   - Modelo
   - Unidade de Medida
   - Tópico MQTT
   - Status (Ativo/Inativo)
3. Clique em "Cadastrar Sensor"

#### Editar Sensor
1. No card do sensor, clique em "Editar"
2. Modifique os campos desejados
3. Clique em "Salvar Alterações"

#### Deletar Sensor
1. No card do sensor, clique em "Deletar"
2. Confirme a exclusão

### 3. Criar Novos Usuários
1. No login, clique em "Cadastre-se aqui"
2. Preencha username, email e senha
3. Faça login com as novas credenciais

## 🔧 Tecnologias Utilizadas

- **Flask** - Framework web
- **Flask-Login** - Gerenciamento de sessões
- **Flask-SQLAlchemy** - ORM para banco de dados
- **MySQL** - Banco de dados relacional
- **PyMySQL** - Driver Python para MySQL
- **Werkzeug** - Criptografia de senhas
- **HTML/CSS** - Interface do usuário

## 🛡️ Segurança

- ✅ Senhas armazenadas com hash (nunca em texto plano)
- ✅ Proteção de rotas sensíveis com `@login_required`
- ✅ Validação de dados do formulário
- ✅ Mensagens de erro e sucesso apropriadas
- ✅ Prevenção de SQL Injection (SQLAlchemy ORM)

## 🎨 Interface

O sistema possui uma interface moderna e responsiva com:
- Gradiente de cores vibrante
- Cards para visualização de sensores
- Badges de status (Ativo/Inativo)
- Formulários intuitivos
- Navegação simplificada
- Mensagens flash coloridas

## 📝 Exemplos de Sensores

O script SQL já cria alguns sensores de exemplo:
1. **Temperatura Sala 1** - DHT22, medição em °C
2. **Umidade Sala 1** - DHT22, medição em %
3. **Pressão Atmosférica** - BMP280, medição em hPa

## 🔄 Próximos Passos (Melhorias Futuras)

- [ ] Integração com MQTT para receber dados reais
- [ ] Gráficos de leituras dos sensores
- [ ] Histórico de leituras
- [ ] Sistema de alertas
- [ ] API REST
- [ ] Roles de usuário (Admin/User)
- [ ] Dashboard com estatísticas

## ⚠️ Troubleshooting

### Erro de conexão com MySQL
```
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")
```
**Solução:** Verifique se o MySQL está rodando e as credenciais estão corretas.

### Erro de importação
```
ModuleNotFoundError: No module named 'flask'
```
**Solução:** Execute `pip install -r requirements.txt`

### Banco de dados não existe
```
sqlalchemy.exc.OperationalError: (1049, "Unknown database 'sensor_system'")
```
**Solução:** Execute o script `database.sql` no MySQL.

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências estão instaladas
2. Confirme que o MySQL está rodando
3. Verifique os logs de erro no terminal

## 📄 Licença

Projeto educacional para fins de aprendizado.

---

**Desenvolvido com Flask** 🐍 | **Banco de Dados MySQL** 🗄️
