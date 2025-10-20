from flask import Blueprint, jsonify
from api.db import get_conn
import time

# Cria um Blueprint. Um Blueprint é um conjunto de rotas que podem ser registradas em uma aplicação.
# 'health' é o nome do blueprint.
# __name__ ajuda o Flask a localizar recursos.
# url_prefix adiciona '/api' antes de todas as rotas neste blueprint.
bp = Blueprint('health', __name__, url_prefix='/api')

@bp.route('/health', methods=['GET'])
def health_check():
    """
    Verifica a saúde da aplicação e a conexão com o banco de dados.
    Retorna status 'ok' ou 'degraded'.
    """
    db_info = {"status": "ok"}
    http_code = 200
    try:
        t0 = time.time()
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
        db_info["latencyMs"] = int((time.time() - t0) * 1000)
    except Exception:
        http_code = 503
        db_info = {"status": "degraded"}

    return jsonify({
        "status": "ok" if http_code == 200 else "degraded",
        "db": db_info
    }), http_code

