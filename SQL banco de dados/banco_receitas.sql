
CREATE DATABASE IF NOT EXISTS ReceitasDB;
USE ReceitasDB;

-- Tabela Receita
CREATE TABLE Receita (
    CodigoReceita INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(100) NOT NULL,
    TempoPreparacao INT NOT NULL,
    NumPessoas INT NOT NULL,
    Dificuldade VARCHAR(30) NOT NULL,
    Categoria VARCHAR(30) NOT NULL,
    Preparacao XML NOT NULL
);

-- Tabela Ingrediente
CREATE TABLE Ingrediente (
    CodigoIngrediente INT PRIMARY KEY AUTO_INCREMENT,
    Ingrediente VARCHAR(50) NOT NULL
);

-- Tabela IngredientesDaReceita (tabela associativa)
CREATE TABLE IngredientesDaReceita (
    CodigoReceita INT NOT NULL,
    CodigoIngrediente INT NOT NULL,
    Quantidade NUMERIC(18,0) NOT NULL,
    Medida VARCHAR(20) NOT NULL,
    PRIMARY KEY (CodigoReceita, CodigoIngrediente),
    FOREIGN KEY (CodigoReceita) REFERENCES Receita(CodigoReceita),
    FOREIGN KEY (CodigoIngrediente) REFERENCES Ingrediente(CodigoIngrediente)
);
