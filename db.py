import os
from psycopg2 import pool
from pgvector.psycopg2 import register_vector
from fastapi import HTTPException

SERVER_ENV=os.getenv('SERVER_ENV')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_USERNAME=os.getenv('DB_USERNAME')
DB_NAME=os.getenv('DB_NAME')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_KEY_NAME=os.getenv('DB_KEY_NAME')

try: 
    conn_params = {
        "host": DB_HOST,
        "database": DB_NAME,
        "user": DB_USERNAME,
        "password": DB_PASSWORD,
        "port": DB_PORT
    }
    if SERVER_ENV == 'prod':
        conn_params.update({
            "sslmode": "require",
            "sslrootcert": DB_KEY_NAME
        })
    dbPool = pool.SimpleConnectionPool(
        1, 
        10, 
        **conn_params
    )
    print('Connection pool created successfully.')
except Exception as e:
    print('Error while connecting to the database:', e)

def registerVector(conn):
    try: 
        with conn.cursor() as cursor:
            cursor.execute('CREATE EXTENSION IF NOT EXISTS vector')
        register_vector(conn)
    except Exception as e: 
        print('Register Vector Error', e)
    

def createEmbeddingsTable(): 
    conn = dbPool.getconn()
    try: 
        registerVector(conn)
        with conn.cursor() as cursor:
            cursor.execute('CREATE TABLE IF NOT EXISTS embeddings (id SERIAL PRIMARY KEY,user_id INT NOT NULL UNIQUE,embedding vector(768),created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), deleted_at TIMESTAMPTZ DEFAULT NULL,FOREIGN KEY(user_id) REFERENCES setting(user_id))')
        conn.commit()
    except Exception as e:
        print('Create Embeddings Table Error', e)
        raise HTTPException(status_code=500, detail=str(e))
    finally: 
        dbPool.putconn(conn)



