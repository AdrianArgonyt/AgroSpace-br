import pyodbc
import re
from contextlib import contextmanager
from api.config import get_config # <-- ALTERADO

# Carrega a string de conexão principal do arquivo .env
DB_CONN_STR = get_config("DB_CONN_STR", "") # <-- ALTERADO
# Define o nome do banco de dados do projeto
DB_NAME = "AgroSpaceBR"

def _get_db_specific_conn_str():
    """
    Gera uma string de conexão que aponta especificamente para o banco 'AgroSpaceBR'.
    Isso evita problemas se a string original apontar para 'master' ou outro banco.
    """
    if not DB_CONN_STR:
        raise ValueError("A variável 'DB_CONN_STR' não foi definida no arquivo .env")

    # Expressão regular para encontrar e substituir o nome do banco de dados na string de conexão
    # Lida com 'DATABASE=outro_db' ou 'Initial Catalog=outro_db'
    pattern = re.compile(r'(DATABASE|INITIAL CATALOG)\s*=\s*[^;]+', re.IGNORECASE)
    
    if pattern.search(DB_CONN_STR):
        # Se a palavra-chave já existe, substitui o valor
        modified_conn_str = pattern.sub(f'DATABASE={DB_NAME}', DB_CONN_STR)
    else:
        # Se não existe, adiciona ao final da string
        modified_conn_str = DB_CONN_STR.rstrip(';') + f';DATABASE={DB_NAME};'
        
    return modified_conn_str

@contextmanager
def get_conn():
    """
    Gerenciador de contexto que fornece uma conexão com o banco de dados 'AgroSpaceBR'.
    Garante que a conexão seja sempre fechada, mesmo que ocorram erros.
    """
    conn_str = _get_db_specific_conn_str()
    conn = None
    try:
        conn = pyodbc.connect(conn_str, autocommit=False)
        yield conn
    except Exception as e:
        # Em caso de erro na conexão ou na transação, desfaz as alterações
        if conn:
            conn.rollback()
        # Propaga o erro para ser tratado nos níveis superiores
        raise e
    finally:
        # Garante que a conexão seja fechada
        if conn:
            conn.close()

def query_all(sql, params=()):
    """Executa uma consulta e retorna todas as linhas como uma lista de dicionários."""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        # Cria uma lista de dicionários a partir das linhas e nomes das colunas
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results

def query_one(sql, params=()):
    """Executa uma consulta e retorna a primeira linha como um dicionário, ou None se não houver resultados."""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        return None

def execute_non_query(sql, params=()):
    """Executa um comando que não retorna dados (INSERT, UPDATE, DELETE) e confirma a transação."""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

