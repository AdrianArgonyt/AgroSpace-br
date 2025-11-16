import sys
import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from pathlib import Path

# --- INÍCIO DA CORREÇÃO DE IMPORTAÇÃO ---
# Adiciona a pasta raiz (AgroSpace-br) ao sys.path
# Isso garante que o Python encontre o pacote 'api'
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))
# --- FIM DA CORREÇÃO DE IMPORTAÇÃO ---

# CORREÇÃO: Revertendo para importações absolutas
from api.routers import health, crops, environments, match, auth
from api.config import get_config

def create_app():
    """Cria e configura a aplicação Flask."""
    
    # Define o caminho para a pasta 'web'
    web_folder = (ROOT_DIR / 'web').resolve()
    
    app = Flask(__name__, static_folder=str(web_folder), static_url_path='/')
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registra os blueprints
    app.register_blueprint(health.bp)
    app.register_blueprint(crops.bp)
    app.register_blueprint(environments.bp)
    app.register_blueprint(match.bp)
    app.register_blueprint(auth.bp)

    @app.route('/')
    def serve_index():
        """Serve o ficheiro principal da interface, o index.html."""
        return send_from_directory(app.static_folder, 'index.html')
        
    @app.route('/<path:path>')
    def serve_static(path):
        """Serve qualquer outro ficheiro estático solicitado (js, css, imagens)."""
        return send_from_directory(app.static_folder, path)

    return app

# Ponto de entrada para servidores WSGI
app = create_app()

if __name__ == '__main__':
    # Executa a aplicação em modo de depuração
    port = int(get_config('FLASK_PORT', 8114))
    app.run(debug=True, port=port)

