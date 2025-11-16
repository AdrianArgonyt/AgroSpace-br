from flask import Blueprint, request, jsonify
# CORREÇÃO: Revertendo para importação absoluta
from api.db import query_one
import re
import sys
import traceback

bp = Blueprint('match', __name__, url_prefix='/api')

def calculate_score(crop, env):
    """
    Calcula o score de compatibilidade heurístico entre uma cultura e um ambiente.
    Retorna o score (0-100), fatores limitantes e uma rationale.
    """
    score = 100
    limiting_factors = []
    rationale = []

    crop_temp_min = crop.get('TempMinC')
    crop_temp_max = crop.get('TempMaxC')
    env_temp_min = env.get('TempMinC')
    env_temp_max = env.get('TempMaxC')
    crop_ph_min = crop.get('PhMin')
    crop_ph_max = crop.get('PhMax')
    env_soil_ph = env.get('SoilPh')
    env_pressure = env.get('PressureKPa')
    crop_photoperiod_min = crop.get('PhotoperiodMinH')
    crop_photoperiod_max = crop.get('PhotoperiodMaxH')
    env_photoperiod = env.get('PhotoperiodH')
    env_radiation = env.get('RadiationIndex')

    # 1. Temperatura
    if all(v is not None for v in [crop_temp_min, crop_temp_max, env_temp_min, env_temp_max]):
        temp_overlap = max(0, min(crop_temp_max, env_temp_max) - max(crop_temp_min, env_temp_min))
        temp_range_crop = crop_temp_max - crop_temp_min
        
        if temp_range_crop > 0 and temp_overlap > 0:
            score_penalty = (1 - (temp_overlap / temp_range_crop)) * 25
            score -= score_penalty
            rationale.append(f"Faixa de temperatura ideal ({crop_temp_min}-{crop_temp_max}°C) é compatível com o ambiente ({env_temp_min}-{env_temp_max}°C).")
        elif temp_overlap <= 0:
            score -= 40
            if env_temp_max < crop_temp_min:
                limiting_factors.append(f"Temperatura muito baixa ({env_temp_max}°C). Requerido: {crop_temp_min}-{crop_temp_max}°C.")
            else:
                limiting_factors.append(f"Temperatura muito alta ({env_temp_min}°C). Requerido: {crop_temp_min}-{crop_temp_max}°C.")
            rationale.append("Será necessário controle de temperatura rigoroso.")
    else:
        rationale.append("Dados de temperatura incompletos para uma análise precisa.")
    
    # 2. pH do Solo
    if env_soil_ph is not None and all(v is not None for v in [crop_ph_min, crop_ph_max]):
        if crop_ph_min <= env_soil_ph <= crop_ph_max:
            rationale.append(f"pH do solo ({env_soil_ph}) está dentro da faixa ideal ({crop_ph_min}-{crop_ph_max}).")
        else:
            score -= 20
            if env_soil_ph < crop_ph_min:
                limiting_factors.append(f"Solo muito ácido ({env_soil_ph}). Requerido: {crop_ph_min}-{crop_ph_max}.")
            else:
                limiting_factors.append(f"Solo muito alcalino ({env_soil_ph}). Requerido: {crop_ph_min}-{crop_ph_max}.")
            rationale.append(f"Será necessário ajustar o pH do substrato para a faixa de {crop_ph_min}-{crop_ph_max}.")
    else:
        rationale.append("Ambiente sem solo natural ou pH não aplicável; cultura hidropônica ou substrato artificial será necessário.")

    # 3. Pressão Atmosférica
    MIN_PRESSURE_KPA = 10.0
    if env_pressure is not None:
        if env_pressure < MIN_PRESSURE_KPA:
            score -= 30
            limiting_factors.append(f"Pressão atmosférica ({env_pressure} kPa) muito baixa.")
            rationale.append(f"Será necessária uma estrutura pressurizada mantendo pelo menos {MIN_PRESSURE_KPA} kPa.")
        else:
            rationale.append(f"Pressão atmosférica ({env_pressure} kPa) é suficiente para água líquida.")
    else:
        limiting_factors.append("Dados de pressão atmosférica do ambiente indisponíveis.")

    # 4. Água
    water_map = {'baixa': 1, 'media': 2, 'alta': 3}
    crop_water = water_map.get(crop.get('WaterNeed', 'media'), 2)
    env_water = water_map.get(env.get('WaterAvailability', 'media'), 2)

    if env_water < crop_water:
        score -= (crop_water - env_water) * 10
        limiting_factors.append(f"Baixa disponibilidade de água. Cultura requer '{crop.get('WaterNeed', 'media')}', ambiente oferece '{env.get('WaterAvailability', 'media')}'.")
        rationale.append("Sistema de reciclagem de água e/ou exploração de gelo (se houver) será crítico.")
    else:
        rationale.append("Disponibilidade de água no ambiente é compatível com a necessidade da cultura.")

    # 5. Fotoperíodo
    if env_photoperiod is not None and all(v is not None for v in [crop_photoperiod_min, crop_photoperiod_max]):
        if not (crop_photoperiod_min <= env_photoperiod <= crop_photoperiod_max):
            score -= 15
            if env_photoperiod < crop_photoperiod_min:
                 limiting_factors.append(f"Fotoperíodo insuficiente ({env_photoperiod}h). Requerido: {crop_photoperiod_min}-{crop_photoperiod_max}h.")
            else:
                 limiting_factors.append(f"Fotoperíodo excessivo ({env_photoperiod}h). Requerido: {crop_photoperiod_min}-{crop_photoperiod_max}h.")
            rationale.append("Será necessário controle de iluminação artificial (luzes LED) para simular o ciclo dia/noite correto.")
    else:
        rationale.append("Fotoperíodo do ambiente não aplicável ou dados da cultura incompletos.")
    
    # 6. Radiação
    if env_radiation is not None and env_radiation > 5.0:
        score -= 10
        limiting_factors.append("Nível de radiação elevado.")
        rationale.append("Será necessária blindagem contra radiação (ex: enterrar estufa ou usar regolito).")

    final_score = max(0, int(score))
    limiting_factors = list(dict.fromkeys(limiting_factors))
    rationale = list(dict.fromkeys(rationale))

    return final_score, limiting_factors, rationale


@bp.route('/match', methods=['POST'])
def get_match():
    """Calcula a compatibilidade entre uma cultura e um ambiente."""
    data = request.get_json()
    
    if not data or 'cropId' not in data or 'environmentId' not in data:
        return jsonify({"error": "Os campos 'cropId' e 'environmentId' são obrigatórios."}), 400
        
    try:
        crop_id = data['cropId']
        env_id = data['environmentId']
        
        crop = query_one("SELECT * FROM Crops WHERE Id = ?", (crop_id,))
        env = query_one("SELECT * FROM Environments WHERE Id = ?", (env_id,))
        
        if not crop or not env:
            return jsonify({"error": "Cultura ou Ambiente não encontrado."}), 404
            
        score, factors, rationale = calculate_score(crop, env)
        
        response = {
            "score": score,
            "limiting_factors": factors,
            "rationale": rationale
        }
        
        return jsonify(response), 200

    except Exception as e:
        print(f"Erro detalhado ao calcular match: {e}\n{traceback.format_exc()}", file=sys.stderr)
        return jsonify({"error": "Ocorreu um erro inesperado no servidor."}), 500

