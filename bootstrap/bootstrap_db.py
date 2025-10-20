import pyodbc
import sys
import re
from pathlib import Path

# Adiciona o diretório raiz ao path do sistema para que possamos importar de 'api'
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Agora a importação funcionará corretamente
from api.config import get_config # <-- ALTERADO
from api.db import DB_NAME

def read_sql_script(filepath):
    """Lê um arquivo de script SQL, tentando diferentes codificações."""
    encodings = ['utf-8', 'cp1252', 'latin-1']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                print(f"Arquivo '{filepath.name}' lido com sucesso usando a codificação: {encoding}")
                return f.read()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Não foi possível decodificar o arquivo {filepath} com as codificações testadas.")

def main():
    """Função principal para executar o bootstrap do banco de dados."""
    try:
        # Carrega a string de conexão a partir da configuração
        db_conn_str = get_config("DB_CONN_STR") # <-- ALTERADO
        if not db_conn_str:
            print("ERRO: A variável 'DB_CONN_STR' não está definida no arquivo .env.", file=sys.stderr)
            sys.exit(1)

        # --- Passo 1: Conectar ao 'master' para garantir que o banco de dados exista ---
        print("Conectando ao banco de dados master...")
        # Remove/substitui a parte do DATABASE para conectar ao master
        master_conn_str = re.sub(r'(DATABASE|INITIAL CATALOG)\s*=\s*[^;]+', 'DATABASE=master', db_conn_str, flags=re.IGNORECASE)
        
        with pyodbc.connect(master_conn_str, autocommit=True) as conn:
            cursor = conn.cursor()
            print(f"Verificando se o banco de dados '{DB_NAME}' existe...")
            
            # Comando CREATE DATABASE não suporta parâmetros, por isso a formatação direta é segura aqui.
            create_db_sql = f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'{DB_NAME}') CREATE DATABASE [{DB_NAME}];"
            cursor.execute(create_db_sql)
            print(f"Banco de dados '{DB_NAME}' garantido.")

        # --- Passo 2: Conectar ao banco de dados 'AgroSpaceBR' e executar scripts ---
        print(f"Conectando ao banco de dados '{DB_NAME}'...")
        # Usa uma string de conexão que aponta diretamente para o banco do projeto
        db_specific_conn_str = re.sub(r'(DATABASE|INITIAL CATALOG)\s*=\s*[^;]+', f'DATABASE={DB_NAME}', db_conn_str, flags=re.IGNORECASE)
        if 'DATABASE=' not in db_specific_conn_str.upper() and 'INITIAL CATALOG=' not in db_specific_conn_str.upper():
            db_specific_conn_str = db_conn_str.rstrip(';') + f';DATABASE={DB_NAME};'

        with pyodbc.connect(db_specific_conn_str, autocommit=True) as conn:
            cursor = conn.cursor()

            # Executa o schema.sql
            models_dir = project_root / 'api' / 'models'
            schema_script = read_sql_script(models_dir / 'schema.sql')
            for statement in filter(None, schema_script.split('GO')):
                cursor.execute(statement)
            print("Script 'schema.sql' executado com sucesso.")

            # Executa o seed.sql
            seed_script = read_sql_script(models_dir / 'seed.sql')
            for statement in filter(None, seed_script.split('GO')):
                cursor.execute(statement)
            print("Script 'seed.sql' executado com sucesso.")

        print("\n✅ Bootstrap do banco de dados concluído com sucesso!")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"\nOcorreu um erro no banco de dados: {sqlstate} - {ex}", file=sys.stderr)
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()


