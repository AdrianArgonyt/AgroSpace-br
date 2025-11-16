from flask import Blueprint, request, jsonify
# CORREÇÃO: Revertendo para importações absolutas
from api.db import query_all, query_one, execute_non_query
from api.auth_utils import token_required
import sys
import traceback

bp = Blueprint('crops', __name__, url_prefix='/api')

@bp.route('/crops', methods=['GET'])
def get_crops():
    """Busca a lista de todas as culturas."""
    try:
        query = "SELECT * FROM Crops"
        q_param = request.args.get('q')
        if q_param:
            query += f" WHERE CommonName LIKE ?"
            params = (f'%{q_param}%',)
            crops = query_all(query, params)
        else:
            crops = query_all(query)
            
        return jsonify(crops), 200
    except Exception as e:
        print(f"Erro ao buscar culturas: {e}\n{traceback.format_exc()}", file=sys.stderr)
        return jsonify({"error": "Ocorreu um erro inesperado no servidor."}), 500

@bp.route('/crops', methods=['POST'])
@token_required
def create_crop():
    """Cria uma nova cultura (Rota protegida)."""
    data = request.get_json()
    
    if not data or 'CommonName' not in data:
        return jsonify({"error": "O campo 'CommonName' é obrigatório."}), 400

    try:
        allowed_columns = [
            'CommonName', 'ScientificName', 'Category', 'TempMinC', 'TempMaxC',
            'PhMin', 'PhMax', 'PhotoperiodMinH', 'PhotoperiodMaxH', 'WaterNeed',
            'EvidenceLevel', 'Sources', 'ImagePath'
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

        sql = f"INSERT INTO Crops ({', '.join(columns)}) VALUES ({', '.join(values)})"
        
        new_id = execute_non_query(sql, tuple(params))
        
        new_crop = query_one("SELECT * FROM Crops WHERE Id = ?", (new_id,))
        
        return jsonify(new_crop), 201
        
    except Exception as e:
        print(f"Erro detalhado ao criar cultura: {e}\n{traceback.format_exc()}", file=sys.stderr)
        return jsonify({"error": "Ocorreu um erro inesperado no servidor."}), 500

