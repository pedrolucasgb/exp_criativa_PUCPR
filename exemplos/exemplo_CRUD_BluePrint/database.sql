-- Script SQL para criar o banco de dados e tabelas para o sistema de sensores

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS sensor_system;

-- Usar o banco de dados
USE sensor_system;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(256) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabela de sensores
CREATE TABLE IF NOT EXISTS sensors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    topic VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Inserir usuário admin padrão (senha: admin)
-- Hash gerado com: generate_password_hash('admin')
INSERT INTO users (username, email, password) 
VALUES ('admin', 'admin@admin.com', 'scrypt:32768:8:1$eKRy4JbFMrV8D5eK$8d4c8e3a8f5e6b7c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2')
ON DUPLICATE KEY UPDATE username=username;

-- Inserir alguns sensores de exemplo
INSERT INTO sensors (name, brand, model, unit, topic, is_active) VALUES
('Temperatura Sala 1', 'DHT', 'DHT22', '°C', '/sensor/temp/sala1', TRUE),
('Umidade Sala 1', 'DHT', 'DHT22', '%', '/sensor/humidity/sala1', TRUE),
('Pressão Atmosférica', 'BMP', 'BMP280', 'hPa', '/sensor/pressure/outdoor', TRUE)
ON DUPLICATE KEY UPDATE name=name;
