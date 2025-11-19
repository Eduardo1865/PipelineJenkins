from flask import Flask, jsonify, request
import psycopg2
import redis
import os
from datetime import datetime

app = Flask(__name__)

# Configurações
DATABASE_URL = os.getenv('DATABASE_URL')
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379')

# Conecta ao Redis
r = redis.from_url(REDIS_URL, decode_responses=True)

def get_db_connection():
    """Cria conexão com PostgreSQL"""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    """Inicializa o banco de dados"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS visitantes (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            data_visita TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def home():
    """Página inicial"""
    # Incrementa contador no Redis
    visitas = r.incr('total_visitas')
    
    return jsonify({
        'mensagem': 'Bem-vindo à aplicação web!',
        'total_visitas': visitas,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/visitantes', methods=['GET'])
def listar_visitantes():
    """Lista todos os visitantes do banco"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, nome, data_visita FROM visitantes ORDER BY data_visita DESC')
    visitantes = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify({
        'visitantes': [
            {'id': v[0], 'nome': v[1], 'data': v[2].isoformat()}
            for v in visitantes
        ]
    })

@app.route('/visitantes', methods=['POST'])
def adicionar_visitante():
    """Adiciona um visitante no banco"""
    nome = request.json.get('nome')
    
    if not nome:
        return jsonify({'erro': 'Nome é obrigatório'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO visitantes (nome) VALUES (%s) RETURNING id', (nome,))
    visitante_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({
        'mensagem': 'Visitante adicionado!',
        'id': visitante_id,
        'nome': nome
    }), 201

@app.route('/health')
def health():
    """Verifica saúde da aplicação"""
    try:
        # Testa PostgreSQL
        conn = get_db_connection()
        conn.close()
        postgres_ok = True
    except:
        postgres_ok = False
    
    try:
        # Testa Redis
        r.ping()
        redis_ok = True
    except:
        redis_ok = False
    
    status = 'ok' if (postgres_ok and redis_ok) else 'error'
    
    return jsonify({
        'status': status,
        'postgres': 'ok' if postgres_ok else 'error',
        'redis': 'ok' if redis_ok else 'error'
    })

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
