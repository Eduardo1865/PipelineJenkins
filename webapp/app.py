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
