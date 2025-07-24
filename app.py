from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verifica_conexao', methods=['GET'])
def verifica_conexao():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='softcom_linker',
            user='softcom',
            password='qaz123'
        )
        if conn.is_connected():
            return jsonify({'success': True, 'message': 'Conexão OK!'})
    except Error as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get('usuario')
    senha = data.get('senha')

    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='softcom_linker',
            user='softcom',
            password='qaz123'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND senha = %s", (usuario, senha))
        user = cursor.fetchone()

        if user:
            return jsonify({'success': True, 'usuario': user['usuario']})
        else:
            return jsonify({'success': False, 'message': 'Usuário ou senha inválidos.'})

    except Error as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
