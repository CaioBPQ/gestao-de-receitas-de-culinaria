import mysql.connector
from mysql.connector import Error
import os

# Configurações padrão de conexão (assuma localhost e credenciais locais).
# O usuário pode sobrescrever via variáveis de ambiente:
# DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_connection():
    config = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD', ''),
        'database': os.environ.get('DB_NAME', 'ReceitasDB'),
        'raise_on_warnings': True
    }
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except Error as e:
        # Se o banco não existe (errno 1049), tentar criar executando o script SQL do projeto
        errno = getattr(e, 'errno', None)
        if errno == 1049:
            # localizar o arquivo SQL: permitir override por variável de ambiente DB_SQL_PATH
            sql_path = os.environ.get('DB_SQL_PATH')
            if not sql_path:
                # procurar arquivo relativo ao diretório do projeto
                base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                candidate = os.path.join(base, 'SQL banco de dados', 'banco_receitas.sql')
                if os.path.exists(candidate):
                    sql_path = candidate
            try:
                if sql_path and os.path.exists(sql_path):
                    init_db(sql_path)
                else:
                    raise RuntimeError(f"Banco '{config.get('database')}' não encontrado e arquivo SQL para criação não foi localizado. Defina DB_SQL_PATH ou crie o banco manualmente.")
            except Exception as ex:
                raise RuntimeError(f"Falha ao criar o banco de dados automaticamente: {ex}")

            # tentar reconectar após criação
            try:
                conn = mysql.connector.connect(**config)
                return conn
            except Error as e2:
                raise RuntimeError(f"Erro ao conectar ao banco de dados após criar o schema: {e2}")

        raise RuntimeError(f"Erro ao conectar ao banco de dados: {e}")

def init_db(sql_file_path=None):
    """Inicializa o banco executando o arquivo SQL fornecido (opcional)."""
    conn = None
    try:
        # conecta sem database para permitir criação
        config = {
            'host': os.environ.get('DB_HOST', 'localhost'),
            'user': os.environ.get('DB_USER', 'root'),
            'password': os.environ.get('DB_PASSWORD', '')
        }
        # ler e preparar SQL
        if not sql_file_path or not os.path.exists(sql_file_path):
            raise RuntimeError('Arquivo SQL para inicialização não encontrado: ' + str(sql_file_path))
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql = f.read()
        import re
        sql = re.sub(r"\bXML\b", "TEXT", sql, flags=re.IGNORECASE)

        # executar CREATE DATABASE usando conexão sem database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # procurar por CREATE DATABASE <name> ou usar DB_NAME
        db_name = os.environ.get('DB_NAME', 'ReceitasDB')
        # executar create database if not exists explicitly
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        conn.commit()
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass

        # reconectar com database e executar statements de criação de tabelas
        config_with_db = config.copy()
        config_with_db['database'] = db_name
        conn2 = mysql.connector.connect(**config_with_db)
        cursor2 = conn2.cursor()
        # remover statements CREATE DATABASE e USE para não re-executar
        statements = []
        for statement in sql.split(';'):
            stmt = statement.strip()
            if not stmt:
                continue
            low = stmt.lower()
            if low.startswith('create database') or low.startswith('use '):
                continue
            statements.append(stmt)

        for stmt in statements:
            cursor2.execute(stmt)
        conn2.commit()
        try:
            cursor2.close()
        except Exception:
            pass
        try:
            conn2.close()
        except Exception:
            pass
    except Error as e:
        raise RuntimeError(f"Erro ao inicializar o banco: {e}")
    finally:
        # já fechamos conexões explicitamente acima
        pass

def insert_receita(receita):
    """Insere uma receita e seus ingredientes. Espera dicionário com chaves:
    nome, tempo_preparacao, num_pessoas, dificuldade, categoria, preparacao (string), ingredientes (lista de dicts com 'nome','quantidade','unidade')
    Retorna o id da receita inserida.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        insert_sql = (
            "INSERT INTO Receita (Nome, TempoPreparacao, NumPessoas, Dificuldade, Categoria, Preparacao) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(insert_sql, (
            receita['nome'],
            int(receita.get('tempo_preparacao') or 0),
            int(receita.get('numero_de_pessoas') or receita.get('num_pessoas') or 0),
            receita.get('dificuldade'),
            receita.get('categoria'),
            receita.get('preparacao')
        ))
        receita_id = cursor.lastrowid
        # inserir ingredientes (garantir existência na tabela Ingrediente)
        for ing in receita.get('ingredientes', []):
            # checar ou inserir ingrediente na tabela Ingrediente
            cursor.execute("SELECT CodigoIngrediente FROM Ingrediente WHERE Ingrediente=%s", (ing['nome'],))
            row = cursor.fetchone()
            if row:
                codigo_ing = row[0]
            else:
                cursor.execute("INSERT INTO Ingrediente (Ingrediente) VALUES (%s)", (ing['nome'],))
                codigo_ing = cursor.lastrowid

            # inserir na tabela associativa
            cursor.execute(
                "INSERT INTO IngredientesDaReceita (CodigoReceita, CodigoIngrediente, Quantidade, Medida) VALUES (%s, %s, %s, %s)",
                (receita_id, codigo_ing, int(ing.get('quantidade') or 0), ing.get('unidade'))
            )

        conn.commit()
        return receita_id
    except Error as e:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def list_receitas():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT CodigoReceita, Nome, TempoPreparacao, NumPessoas, Dificuldade, Categoria, Preparacao FROM Receita")
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()

def get_receita(codigo_receita):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT CodigoReceita, Nome, TempoPreparacao, NumPessoas, Dificuldade, Categoria, Preparacao FROM Receita WHERE CodigoReceita=%s", (codigo_receita,))
        row = cursor.fetchone()
        if not row:
            return None
        # buscar ingredientes
        cursor.execute(
            "SELECT i.CodigoIngrediente, i.Ingrediente, ir.Quantidade, ir.Medida FROM Ingrediente i JOIN IngredientesDaReceita ir ON i.CodigoIngrediente=ir.CodigoIngrediente WHERE ir.CodigoReceita=%s",
            (codigo_receita,)
        )
        ingredientes = cursor.fetchall()
        row['ingredientes'] = ingredientes
        return row
    finally:
        cursor.close()
        conn.close()

def update_receita(codigo_receita, field, value):
    # atualizar apenas campos simples na tabela Receita
    allowed = {
        'nome': 'Nome',
        'tempo_preparacao': 'TempoPreparacao',
        'numero_de_pessoas': 'NumPessoas',
        'dificuldade': 'Dificuldade',
        'categoria': 'Categoria',
        'preparacao': 'Preparacao'
    }
    if field not in allowed:
        raise ValueError('Campo não permitido para atualização')
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = f"UPDATE Receita SET {allowed[field]}=%s WHERE CodigoReceita=%s"
        cursor.execute(sql, (value, codigo_receita))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()

def delete_receita(codigo_receita):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # deletar associacoes primeiro
        cursor.execute("DELETE FROM IngredientesDaReceita WHERE CodigoReceita=%s", (codigo_receita,))
        cursor.execute("DELETE FROM Receita WHERE CodigoReceita=%s", (codigo_receita,))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()
