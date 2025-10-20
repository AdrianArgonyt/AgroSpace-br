from flask import Blueprint, jsonify, request
from api.db import query_all, query_one, execute_non_query

bp = Blueprint('crops', __name__, url_prefix='/api')

@bp.route('/crops', methods=['GET'])
def get_crops():
    """Lista todas as culturas, com suporte a filtro por nome."""
    search_query = request.args.get('q', '')
    
    if search_query:
        sql = "SELECT * FROM Crops WHERE CommonName LIKE ? ORDER BY CommonName"
        params = (f'%{search_query}%',)
    else:
        sql = "SELECT * FROM Crops ORDER BY CommonName"
        params = ()
        
    crops = query_all(sql, params)
    return jsonify(crops)

@bp.route('/crops', methods=['POST'])
def create_crop():
    """Cria uma nova cultura."""
    data = request.get_json()
    if not data or not data.get('CommonName'):
        return jsonify({"error": "O campo 'CommonName' é obrigatório."}), 400

    sql = """
        INSERT INTO Crops (CommonName, ScientificName, Family, ImagePath, TempMinC, TempMaxC, PhMin, PhMax, PhotoperiodMinH, PhotoperiodMaxH, WaterNeed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    params = (
        data.get('CommonName'),
        data.get('ScientificName'),
        data.get('Family'),
        data.get('ImagePath'),
        data.get('TempMinC'),
        data.get('TempMaxC'),
        data.get('PhMin'),
        data.get('PhMax'),
        data.get('PhotoperiodMinH'),
        data.get('PhotoperiodMaxH'),
        data.get('WaterNeed')
    )
    
    execute_non_query(sql, params)
    
    # Retorna o item recém-criado
    last_crop = query_one("SELECT TOP 1 * FROM Crops ORDER BY Id DESC")
    return jsonify(last_crop), 201

