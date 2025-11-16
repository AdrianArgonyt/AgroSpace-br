import sys
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
# CORREÇÃO: Revertendo para importações absolutas
from api.db import query_one, execute_non_query
from api.auth_utils import generate_auth_token
import re

bp = Blueprint('auth', __name__, url_prefix='/api')

@bp.route('/register', methods=['POST'])
def register_user():
    """Regista um novo usuário."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Usuário e senha são obrigatórios."}), 400
        
    if not re.match(r"^[a-zA-Z0-9_.-]+$", username):
         return jsonify({"error": "Nome de usuário contém caracteres inválidos."}), 400
         
    if len(password) < 6:
        return jsonify({"error": "A senha deve ter pelo menos 6 caracteres."}), 400

    try:
        existing_user = query_one("SELECT Id FROM Users WHERE Username = ?", (username,))
        if existing_user:
            return jsonify({"error": "Este nome de usuário já está em uso."}), 409

        password_hash = generate_password_hash(password)
        execute_non_query("INSERT INTO Users (Username, PasswordHash) VALUES (?, ?)", (username, password_hash))
        
        return jsonify({"message": "Usuário registrado com sucesso."}), 201

    except Exception as e:
        print(f"Erro detalhado ao registrar: {e}\n", file=sys.stderr)
        return jsonify({"error": "Ocorreu um erro inesperado no servidor."}), 500


@bp.route('/login', methods=['POST'])
def login_user():
    """Autentica um usuário e retorna um token."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Usuário e senha são obrigatórios."}), 400

    try:
        user = query_one("SELECT * FROM Users WHERE Username = ?", (username,))
        
        if not user:
            return jsonify({"error": "Credenciais inválidas."}), 401
            
        if not check_password_hash(user['PasswordHash'], password):
            return jsonify({"error": "Credenciais inválidas."}), 401

        token = generate_auth_token(user['Id'], user['Username'])
        
        return jsonify({
            "message": "Login bem-sucedido.",
            "token": token,
            "user": {
                "username": user['Username'],
                "isAdmin": user['IsAdmin']
            }
        }), 200

    except Exception as e:
        print(f"Erro detalhado ao fazer login: {e}\n", file=sys.stderr)
        return jsonify({"error": "Ocorreu um erro inesperado no servidor."}), 500

