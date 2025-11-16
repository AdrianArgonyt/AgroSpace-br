import sys
import os
from functools import wraps
from flask import request, jsonify, g
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
# CORREÇÃO: Revertendo para importações absolutas
from api.config import get_config
from api.db import query_one

SECRET_KEY = get_config("SECRET_KEY", "fallback-insecure-secret-key-!CHANGE-ME!")

serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_auth_token(user_id, username):
    """Gera um token de autenticação seguro para um usuário."""
    return serializer.dumps({'user_id': user_id, 'username': username})

def verify_auth_token(token):
    """Verifica um token. Retorna os dados do usuário se for válido, senão None."""
    try:
        data = serializer.loads(token, max_age=86400) # Expira em 1 dia
    except (SignatureExpired, BadTimeSignature, Exception):
        return None
    return data

def token_required(f):
    """Decorador para proteger rotas que exigem autenticação."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
            
        if not token:
            return jsonify({"error": "Token de autenticação ausente."}), 401
            
        user_data = verify_auth_token(token)
        if user_data is None:
            return jsonify({"error": "Token inválido ou expirado."}), 401
            
        g.user = query_one("SELECT * FROM Users WHERE Id = ?", (user_data['user_id'],))
        
        if not g.user:
             return jsonify({"error": "Usuário do token não encontrado."}), 401

        return f(*args, **kwargs)
    return decorated_function

