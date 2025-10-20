from flask import Blueprint, jsonify, request
from api.db import query_all, query_one, execute_non_query

bp = Blueprint('environments', __name__, url_prefix='/api')

@bp.route('/environments', methods=['GET'])
def get_environments():
    """Lista todos os ambientes, com suporte a filtro por nome."""
    search_query = request.args.get('q', '')
    
    if search_query:
        sql = "SELECT * FROM Environments WHERE Name LIKE ? ORDER BY Name"
        params = (f'%{search_query}%',)
    else:
        sql = "SELECT * FROM Environments ORDER BY Name"
        params = ()
        
    environments = query_all(sql, params)
    return jsonify(environments)

@bp.route('/environments', methods=['POST'])
def create_environment():
    """Cria um novo ambiente."""
    data = request.get_json()
    if not data or not data.get('Name') or not data.get('Type'):
        return jsonify({"error": "Os campos 'Name' e 'Type' são obrigatórios."}), 400

    sql = """
        INSERT INTO Environments (Name, Type, Description, ImagePath, TempMinC, TempMaxC, PressureKPa, GravityG, RadiationIndex, SoilPh, SoilType, WaterAvailability, PhotoperiodH, Atmosphere)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    params = (
        data.get('Name'),
        data.get('Type'),
        data.get('Description'),
        data.get('ImagePath'),
        data.get('TempMinC'),
        data.get('TempMaxC'),
        data.get('PressureKPa'),
        data.get('GravityG'),
        data.get('RadiationIndex'),
        data.get('SoilPh'),
        data.get('SoilType'),
        data.get('WaterAvailability'),
        data.get('PhotoperiodH'),
        data.get('Atmosphere')
    )
    
    execute_non_query(sql, params)
    
    last_env = query_one("SELECT TOP 1 * FROM Environments ORDER BY Id DESC")
    return jsonify(last_env), 201

