# scaffold_agroespaco.py
from pathlib import Path

# Vai criar em: C:\Users\Administrator\Documents\AgroSpaceBR\AgroSpace-br
PROJECT = Path(r"C:\Users\Administrator\Documents\AgroSpaceBR") / "AgroSpace-br"

FILES = {
    # raiz
    "README.md": "# AgroEspaço BR\n\nEstrutura inicial do projeto.\n",
    ".gitignore": "__pycache__/\n*.pyc\n.venv/\n.env\n.vscode/\n.DS_Store\n",
    "LICENSE": "MIT License\n\n(c) 2025 Seu Nome\n",
    # docs
    "docs/objetivo_problema.md": "# Objetivo & Problema\n",
    "docs/requisitos.md": "# Requisitos\n",
    "docs/casos_de_uso.md": "# Casos de Uso\n",
    "docs/arquitetura.md": "# Arquitetura\n",
    # infra
    "infra/.env.example": "SQLSERVER_SERVER=localhost\\SQLEXPRESS\nSQLSERVER_DATABASE=AgroEspaco\nSQLSERVER_USERNAME=\nSQLSERVER_PASSWORD=\nSQLSERVER_TRUSTED=Yes\nAPP_ENV=dev\n",
    "infra/docker-compose.yml": "version: '3.9'\nservices:\n  mssql:\n    image: mcr.microsoft.com/mssql/server:2022-latest\n    environment:\n      - ACCEPT_EULA=Y\n      - SA_PASSWORD=SuaSenhaForte_123\n    ports:\n      - '1433:1433'\n    volumes:\n      - ./mssql_data:/var/opt/mssql\n",
    # api
    "api/__init__.py": "",
    "api/requirements.txt": "flask==3.0.3\npython-dotenv==1.0.1\npyodbc==5.1.0\n",
    "api/app.py": "# placeholder: app Flask vai aqui\n",
    "api/db.py": "# placeholder: conexão SQL Server vai aqui\n",
    "api/config.py": "# placeholder: leitura de variáveis de ambiente vai aqui\n",
    # routers
    "api/routers/health.py": "# placeholder: rota /health\n",
    "api/routers/crops.py": "# placeholder: rotas /crops\n",
    "api/routers/environments.py": "# placeholder: rotas /environments\n",
    "api/routers/match.py": "# placeholder: rota /match (simulador)\n",
    # models
    "api/models/schema.sql": "-- DDL aqui\n",
    "api/models/seed.sql": "-- seeds aqui\n",
}

def main():
    root = Path(PROJECT)
    for rel_path, content in FILES.items():
        file_path = root / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            file_path.write_text(content, encoding="utf-8")
    # diretórios vazios úteis
    for d in ["data", "infra/mssql_data"]:
        (root / d).mkdir(parents=True, exist_ok=True)
    # imprime a árvore criada
    print(f"\nCriado em: {root.resolve()}\n")
    for p in sorted(root.rglob("*")):
        print(p.relative_to(root))

if __name__ == "__main__":
    main()
