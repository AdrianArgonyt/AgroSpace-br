import os
from dotenv import load_dotenv
from pathlib import Path

# Carrega o .env da pasta raiz do projeto
# Path(__file__).resolve().parent.parent aponta para 'AgroSpace-br'
env_path = Path(__file__).resolve().parent.parent / '.env'

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print(f"Aviso: Arquivo .env não encontrado em {env_path}", file=os.sys.stderr)

def get_config(key, default=None):
    """Busca uma variável de configuração do ambiente."""
    return os.getenv(key, default)

