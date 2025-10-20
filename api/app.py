import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from pathlib import Path

# Importa os blueprints das rotas
from api.routers import health, crops, environments, match
from api.config import get_config

def create_app():
    """Cria e configura a aplicação Flask."""
    
    # Define o caminho para a pasta 'web' que contém os ficheiros estáticos (index.html, js, imagens)
    # '../web' significa "subir um nível a partir da pasta 'api' e depois entrar na 'web'"
    web_folder = (Path(__file__).resolve().parent.parent / 'web').resolve()
    
    # Cria a instância da aplicação Flask, informando onde estão os ficheiros estáticos
    app = Flask(__name__, static_folder=str(web_folder), static_url_path='/')
    
    # Habilita o CORS para permitir que o frontend comunique com a API
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registra os blueprints (conjuntos de rotas) na aplicação
    app.register_blueprint(health.bp)
    app.register_blueprint(crops.bp)
    app.register_blueprint(environments.bp)
    app.register_blueprint(match.bp)

    @app.route('/')
    def serve_index():
        """Serve o ficheiro principal da interface, o index.html."""
        return send_from_directory(app.static_folder, 'index.html')
        
    @app.route('/<path:path>')
    def serve_static(path):
        """Serve qualquer outro ficheiro estático solicitado (js, css, imagens)."""
        return send_from_directory(app.static_folder, path)

    return app

# Ponto de entrada para servidores WSGI como Gunicorn ou Waitress
app = create_app()

if __name__ == '__main__':
    # Executa a aplicação em modo de depuração se o script for chamado diretamente
    port = int(get_config('FLASK_PORT', 8114))
    app.run(debug=True, port=port)

