-- Script SQL para criar o banco de dados e tabelas para o sistema de restaurante

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS restaurante;

-- Usar o banco de dados
USE restaurante;

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(256) NOT NULL,
    tipo VARCHAR(20) NOT NULL DEFAULT 'cliente',
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_tipo (tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de Itens do Cardápio
CREATE TABLE IF NOT EXISTS itens_cardapio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    categoria VARCHAR(50) NOT NULL,
    preco FLOAT NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_categoria (categoria),
    INDEX idx_disponivel (disponivel)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de Comandas
CREATE TABLE IF NOT EXISTS comandas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_mesa INT NOT NULL,
    cliente_id INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'aberta',
    valor_total FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fechada_at TIMESTAMP NULL,
    paga_at TIMESTAMP NULL,
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
    INDEX idx_status (status),
    INDEX idx_cliente (cliente_id),
    INDEX idx_mesa (numero_mesa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de Itens da Comanda
CREATE TABLE IF NOT EXISTS itens_comanda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comanda_id INT NOT NULL,
    item_cardapio_id INT NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    preco_unitario FLOAT NOT NULL,
    subtotal FLOAT NOT NULL,
    observacoes VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (comanda_id) REFERENCES comandas(id) ON DELETE CASCADE,
    FOREIGN KEY (item_cardapio_id) REFERENCES itens_cardapio(id),
    INDEX idx_comanda (comanda_id),
    INDEX idx_item (item_cardapio_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de Pagamentos
CREATE TABLE IF NOT EXISTS pagamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comanda_id INT NOT NULL,
    valor FLOAT NOT NULL,
    forma_pagamento VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pendente',
    processado_por_id INT,
    observacoes VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processado_at TIMESTAMP NULL,
    FOREIGN KEY (comanda_id) REFERENCES comandas(id) ON DELETE CASCADE,
    FOREIGN KEY (processado_por_id) REFERENCES usuarios(id),
    INDEX idx_status (status),
    INDEX idx_comanda (comanda_id),
    INDEX idx_forma_pagamento (forma_pagamento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Inserir usuários padrão
INSERT INTO usuarios (nome, email, senha, tipo) VALUES
('Caixa Principal', 'caixa@restaurante.com', 'scrypt:32768:8:1$BHqB8x9YGzRKU7KY$d8a9c5f5c3b1e2a7f4d6c8b9e0a1f2d3c4b5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1', 'caixa'),
('Atendente 1', 'atendente@restaurante.com', 'scrypt:32768:8:1$BHqB8x9YGzRKU7KY$d8a9c5f5c3b1e2a7f4d6c8b9e0a1f2d3c4b5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1', 'atendente'),
('Cliente Teste', 'cliente@email.com', 'scrypt:32768:8:1$BHqB8x9YGzRKU7KY$d8a9c5f5c3b1e2a7f4d6c8b9e0a1f2d3c4b5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1', 'cliente')
ON DUPLICATE KEY UPDATE nome=nome;

-- Inserir itens do cardápio
INSERT INTO itens_cardapio (nome, descricao, categoria, preco) VALUES
-- Bebidas
('Refrigerante', 'Coca-Cola, Guaraná ou Fanta', 'bebida', 5.00),
('Suco Natural', 'Laranja, Limão ou Maracujá', 'bebida', 8.00),
('Cerveja', 'Cerveja pilsen 350ml', 'bebida', 7.00),
('Água Mineral', 'Água sem gás 500ml', 'bebida', 3.00),
-- Comidas
('X-Burger', 'Hambúrguer, queijo, alface e tomate', 'comida', 25.00),
('X-Salada', 'Hambúrguer, queijo, alface, tomate e milho', 'comida', 28.00),
('X-Bacon', 'Hambúrguer, queijo, bacon e molho especial', 'comida', 30.00),
('Batata Frita', 'Porção de batata frita crocante', 'comida', 18.00),
('Pastel', 'Pastel de carne, queijo ou frango', 'comida', 12.00),
-- Sobremesas
('Pudim', 'Pudim de leite condensado', 'sobremesa', 10.00),
('Sorvete', 'Sorvete 2 bolas (vários sabores)', 'sobremesa', 12.00),
('Brownie', 'Brownie de chocolate com sorvete', 'sobremesa', 15.00)
ON DUPLICATE KEY UPDATE nome=nome;

