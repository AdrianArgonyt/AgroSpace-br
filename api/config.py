import os
from dotenv import load_dotenv
from pathlib import Path

def find_dotenv():
    """Busca o arquivo .env subindo a árvore de diretórios a partir deste script."""
    # O diretório atual do script (ex: .../AgroSpace-br/api)
    current_dir = Path(__file__).resolve().parent
    # O diretório raiz do projeto (ex: .../AgroSpace-br)
    project_root = current_dir.parent
    
    env_path = project_root / '.env'
    
    return env_path if env_path.exists() else None

# Carrega as variáveis de ambiente do arquivo .env encontrado
ENV_PATH = find_dotenv()
if ENV_PATH:
    print(f"Procurando arquivo .env em: {ENV_PATH}")
    load_dotenv(dotenv_path=ENV_PATH)
    print("Arquivo .env carregado com sucesso.")
else:
    print("AVISO: Arquivo .env não encontrado.")

def get_config(key, default=None):
    """
    Busca uma variável de ambiente de forma segura.
    Renomeado de 'config' para 'get_config' para evitar conflito com o objeto de config do Flask.
    """
    return os.getenv(key, default)

