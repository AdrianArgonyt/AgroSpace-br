from flask import Blueprint, request, jsonify
# CORREÇÃO: Revertendo para importações absolutas
from api.db import query_all, query_one, execute_non_query
from api.auth_utils import token_required
import sys
import traceback

bp = Blueprint('environments', __name__, url_prefix='/api')

@bp.route('/environments', methods=['GET'])
def get_environments():
    """Busca a lista de todos os ambientes."""
    try:
        query = "SELECT * FROM Environments"
        q_param = request.args.get('q')
        if q_param:
            query += f" WHERE Name LIKE ?"
            params = (f'%{q_param}%',)
            environments = query_all(query, params)
        else:
            environments = query_all(query)
            
        return jsonify(environments), 200
    except Exception as e:
        print(f"Erro ao buscar ambientes: {e}\n{traceback.format_exc()}", file=sys.stderr)
        return jsonify({"error": "Ocorreu um erro inesperado no servidor."}), 500

@bp.route('/environments', methods=['POST'])
@token_required
def create_environment():
    """Cria um novo ambiente (Rota protegida)."""
    data = request.get_json()
    
    if not data or 'Name' not in data or 'Type' not in data:
        return jsonify({"error": "Os campos 'Name' e 'Type' são obrigatórios."}), 400

    try:
        allowed_columns = [
            'Name', 'Type', 'TempMinC', 'TempMaxC', 'PressureKPa', 'GravityG',
            'RadiationIndex', 'SoilPh', 'SoilType', 'WaterAvailability',
            'PhotoperiodH', 'Atmosphere', 'EvidenceLevel', 'Notes', 'Sources', 'ImagePath'
        ]
        
        columns = []
        values = []
        params = []
        
        for col in allowed_columns:
            if col in data and data[col] is not None:
                columns.append(col)
                values.append('?')
                params.append(data[col])
        
        if not columns:
             return jsonify({"error": "Nenhum dado válido fornecido."}), 400

        sql = f"INSERT INTO Environments ({', '.join(columns)}) VALUES ({', '.join(values)})"
        
        new_id = execute_non_query(sql, tuple(params))
        
        new_env = query_one("SELECT * FROM Environments WHERE Id = ?", (new_id,))
        
        return jsonify(new_env), 201
        
    except Exception as e:
        print(f"Erro detalhado ao criar ambiente: {e}\n{traceback.format_exc()}", file=sys.stderr)
        return jsonify({"error": "Ocorreu um erro inesperado no servidor."}), 500

