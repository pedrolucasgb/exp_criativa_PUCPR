# Exercício 9 - Sistema de Roles e Gerenciamento de Usuários

Este exercício implementa um sistema completo de gerenciamento de usuários com roles (Admin e User).

## Funcionalidades Implementadas

### 1. Sistema de Roles
- **Modelo Role** (`models/user/roles.py`)
  - Campos: id, name, description
  - Métodos: save_role(), get_single_role(), get_role()
  - Roles criados automaticamente: "Admin" e "User"

### 2. Modelo de Usuário Atualizado
- **Modelo User** (`models/user/users.py`)
  - Campos: id, role_id, username, email, password (hash)
  - Relacionamento 1:N com Role
  - Métodos implementados:
    - `save_user()` - Criar novo usuário
    - `get_users()` - Listar todos os usuários
    - `get_single_user()` - Buscar usuário específico
    - `update_user()` - Atualizar usuário
    - `delete_user()` - Remover usuário
    - `check_password()` - Validar senha (com hash)

### 3. Controller de Usuários
- **Blueprint** `users_controller.py` com rotas:
  - `/users/register_user` - Formulário de cadastro
  - `/users/add_user` - Criar novo usuário
  - `/users/list_users` - Listar todos os usuários
  - `/users/edit_user/<id>` - Editar usuário
  - `/users/update_user/<id>` - Salvar alterações
  - `/users/delete_user/<id>` - Remover usuário

### 4. Templates HTML
- `register_user.html` - Formulário de cadastro com seleção de role
- `list_users.html` - Listagem de usuários com badges (Admin/User)
- `edit_user.html` - Formulário de edição (senha opcional)

### 5. Segurança
- ✅ Senhas armazenadas com hash (werkzeug.security)
- ✅ Validação de senha com `check_password()`
- ✅ Proteção contra auto-exclusão
- ✅ Login requer autenticação

## Como Usar

### 1. Inicializar o Banco de Dados
Ao rodar `python main.py`, o banco é automaticamente criado com:
- 2 Roles: "Admin" e "User"
- 1 Usuário Admin padrão:
  - **Username:** admin
  - **Password:** admin
  - **Email:** admin@admin.com

### 2. Login
- Acesse: `http://127.0.0.1:5000/login`
- Use credenciais: `admin` / `admin`

### 3. Gerenciar Usuários
- Menu: **Users** (na navegação)
- **Register New User:** Criar usuário e escolher role (Admin ou User)
- **Edit:** Modificar dados do usuário (senha opcional)
- **Delete:** Remover usuário (não pode deletar a si mesmo)

## Estrutura de Arquivos

```
ex09/
├── models/
│   └── user/
│       ├── __init__.py
│       ├── roles.py      # Modelo Role
│       └── users.py      # Modelo User (com roles)
├── controllers/
│   └── users_controller.py  # CRUD de usuários
├── templates/
│   ├── register_user.html
│   ├── list_users.html
│   └── edit_user.html
└── main.py               # Inicialização com roles
```

## Diferenças entre Admin e User

Atualmente ambos têm acesso completo. Para restringir:
1. Use `current_user.role.name` nos templates
2. Adicione decoradores personalizados nos controllers

Exemplo:
```python
{% if current_user.role.name == 'Admin' %}
    <a href="...">Admin Only</a>
{% endif %}
```

## Próximos Passos (Opcional)
- Implementar permissões diferenciadas por role
- Dashboard com estatísticas de usuários
- Auditoria de ações dos usuários
