from flask import Blueprint
import time
import sys
import traceback
# CORREÇÃO: Revertendo para importação absoluta
from api.db import get_conn

bp = Blueprint('health', __name__, url_prefix='/api')

@bp.route('/health', methods=['GET'])
def get_health():
    """Verifica a saúde da aplicação e a conexão com o banco de dados."""
    db_status = "ok"
    start_time = time.time()
    
    try:
        with get_conn():
            pass 
        latency_ms = (time.time() - start_time) * 1000
    except Exception as e:
        print(f"Erro no health check do banco: {e}\n{traceback.format_exc()}", file=sys.stderr)
        db_status = "degraded"
        latency_ms = -1

    if db_status == "ok":
        return jsonify({
            "status": "ok",
            "db": {"status": "ok", "latency_ms": f"{latency_ms:.2f}ms"}
        }), 200
    else:
        return jsonify({
            "status": "degraded",
            "db": {"status": "degraded"}
        }), 503

