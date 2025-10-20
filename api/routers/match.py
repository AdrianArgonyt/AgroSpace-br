from flask import Blueprint, jsonify, request
from api.db import query_one

bp = Blueprint('match', __name__, url_prefix='/api')

def calculate_score(crop, env):
    """
    Calcula o score de compatibilidade e os fatores com base em uma heurística.
    Retorna um dicionário com score, fatores limitantes e recomendações.
    """
    score = 100
    limiting_factors = []
    rationale = []

    # 1. Temperatura
    temp_overlap = 0
    if crop['TempMinC'] is not None and crop['TempMaxC'] is not None and env['TempMinC'] is not None and env['TempMaxC'] is not None:
        # Calcula a sobreposição entre a faixa da cultura e a faixa do ambiente
        overlap_min = max(crop['TempMinC'], env['TempMinC'])
        overlap_max = min(crop['TempMaxC'], env['TempMaxC'])
        overlap_range = max(0, overlap_max - overlap_min)
        crop_range = crop['TempMaxC'] - crop['TempMinC']
        
        if crop_range > 0:
            temp_overlap = (overlap_range / crop_range) * 100
        elif crop['TempMinC'] >= env['TempMinC'] and crop['TempMaxC'] <= env['TempMaxC']:
            temp_overlap = 100

    if temp_overlap < 20:
        score -= 30
        limiting_factors.append("Temperatura incompatível")
        rationale.append(f"Necessário controle de temperatura para manter a faixa de {crop['TempMinC']}°C a {crop['TempMaxC']}°C.")
    elif temp_overlap < 80:
        score -= (80 - temp_overlap) * 0.25 # Penalidade menor
        rationale.append(f"A faixa de temperatura do ambiente ({env['TempMinC']}°C a {env['TempMaxC']}°C) tem sobreposição parcial com a ideal para a cultura.")


    # 2. pH do Solo
    if crop['PhMin'] is not None and crop['PhMax'] is not None and env['SoilPh'] is not None:
        if not (crop['PhMin'] <= env['SoilPh'] <= crop['PhMax']):
            score -= 25
            limiting_factors.append("pH do solo inadequado")
            rationale.append(f"O pH do solo de {env['SoilPh']} está fora da faixa ideal ({crop['PhMin']}-{crop['PhMax']}). Será necessário ajustar o substrato.")
        else:
            rationale.append("O pH do solo é compatível.")
    else:
        score -= 5 # Incerteza
        limiting_factors.append("Dados de pH do solo insuficientes")

    # 3. Pressão Atmosférica
    if env['PressureKPa'] is not None:
        if env['PressureKPa'] < 1: # Quase vácuo
            score -= 30
            limiting_factors.append("Pressão atmosférica extremamente baixa (vácuo)")
            rationale.append("É mandatório o uso de estufas pressurizadas para o cultivo.")
        elif env['PressureKPa'] > 2000: # Pressão esmagadora
            score -= 40
            limiting_factors.append("Pressão atmosférica extremamente alta")
            rationale.append("Estruturas de contenção robustas são necessárias para suportar a pressão externa.")
    
    # 4. Água
    water_map = {'baixa': 1, 'media': 2, 'alta': 3}
    crop_water = water_map.get(crop.get('WaterNeed', '').lower())
    env_water = water_map.get(env.get('WaterAvailability', '').lower())
    
    if crop_water is not None and env_water is not None:
        if env_water < crop_water:
            score -= 20
            limiting_factors.append("Disponibilidade de água insuficiente")
            rationale.append(f"A cultura necessita de água '{crop['WaterNeed']}', mas a disponibilidade no ambiente é '{env['WaterAvailability']}'. Irrigação com água importada ou extraída localmente é essencial.")
        else:
            rationale.append("Disponibilidade de água compatível com a necessidade da cultura.")

    return {
        "score": max(0, int(score)),
        "limiting_factors": limiting_factors or ["Nenhum fator limitante principal identificado."],
        "rationale": rationale
    }


@bp.route('/match', methods=['POST'])
def match_crop_environment():
    """
    Recebe IDs de cultura e ambiente, calcula a compatibilidade e retorna o resultado.
    """
    data = request.get_json()
    crop_id = data.get('cropId')
    environment_id = data.get('environmentId')

    if not crop_id or not environment_id:
        return jsonify({"error": "Os campos 'cropId' e 'environmentId' são obrigatórios."}), 400

    crop = query_one("SELECT * FROM Crops WHERE Id = ?", (crop_id,))
    env = query_one("SELECT * FROM Environments WHERE Id = ?", (environment_id,))

    if not crop or not env:
        return jsonify({"error": "Cultura ou ambiente não encontrado."}), 404

    result = calculate_score(crop, env)
    
    return jsonify(result)

