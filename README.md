# Gerenciador de Receitas

Este projeto é um gerenciador simples de receitas em Python que se integra com um banco MySQL.

Estrutura:
- `python/main.py` - interface CLI para adicionar, consultar e gerir receitas.
- `python/db.py` - módulo de conexão e operações básicas com o banco MySQL.
- `SQL banco de dados/banco_receitas.sql` - arquivo SQL para criar o banco e as tabelas.
- `requirements.txt` - dependências Python.

Instalação e execução (Windows - PowerShell):

1. Criar e ativar um ambiente virtual (opcional, recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependências:

```powershell
pip install -r requirements.txt
```

3. Criar o banco de dados executando o script SQL (no MySQL client ou MySQL Workbench):

Abra o MySQL e execute o conteúdo de `"SQL banco de dados/banco_receitas.sql"`.

4. (Opcional) configurar variáveis de ambiente se necessário:

```powershell
$env:DB_HOST = 'localhost'
$env:DB_USER = 'root'
$env:DB_PASSWORD = 'sua_senha'
$env:DB_NAME = 'ReceitasDB'
```

5. Executar o programa:

```powershell
python .\python\main.py
```

Observações:
- O `db.py` espera o banco `ReceitasDB` criado. Se quiser automatizar a criação, chame `db.init_db()` apontando para o arquivo SQL.
- As entradas de ingredientes convertem a quantidade para inteiro ao inserir no banco; ajuste conforme necessário.
