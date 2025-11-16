import pyodbc
import re
from contextlib import contextmanager
# CORREÇÃO: Revertendo para importação absoluta
from api.config import get_config 

# Carrega a string de conexão principal do arquivo .env
DB_CONN_STR = get_config("DB_CONN_STR", "")
# Define o nome do banco de dados do projeto
DB_NAME = "AgroSpaceBR"

def _get_db_specific_conn_str():
    """Gera uma string de conexão que aponta especificamente para o banco 'AgroSpaceBR'."""
    if not DB_CONN_STR:
        raise ValueError("A variável 'DB_CONN_STR' não foi definida no arquivo .env")

    pattern = re.compile(r'(DATABASE|INITIAL CATALOG)\s*=\s*[^;]+', re.IGNORECASE)
    
    if pattern.search(DB_CONN_STR):
        modified_conn_str = pattern.sub(f'DATABASE={DB_NAME}', DB_CONN_STR)
    else:
        modified_conn_str = DB_CONN_STR.rstrip(';') + f';DATABASE={DB_NAME};'
        
    return modified_conn_str

@contextmanager
def get_conn(autocommit=True):
    """Fornece uma conexão com o banco de dados 'AgroSpaceBR'."""
    conn_str = _get_db_specific_conn_str()
    conn = None
    try:
        conn = pyodbc.connect(conn_str, autocommit=autocommit)
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def query_all(sql, params=()):
    """Executa uma consulta e retorna todas as linhas como uma lista de dicionários."""
    with get_conn(autocommit=True) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results

def query_one(sql, params=()):
    """Executa uma consulta e retorna a primeira linha como um dicionário, ou None."""
    with get_conn(autocommit=True) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        return None

def execute_non_query(sql, params=()):
    """Executa um comando (INSERT, UPDATE, DELETE) e confirma a transação."""
    with get_conn(autocommit=False) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        
        new_id = None
        if sql.strip().upper().startswith("INSERT"):
            try:
                cursor.execute("SELECT @@IDENTITY AS NewId")
                new_id = cursor.fetchone().NewId
            except pyodbc.Error:
                pass 
                
        conn.commit()
        return new_id

