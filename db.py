import os
from psycopg2 import pool
from pgvector.psycopg2 import register_vector
from fastapi import HTTPException

DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_USERNAME=os.getenv('DB_USERNAME')
DB_NAME=os.getenv('DB_NAME')
DB_PASSWORD=os.getenv('DB_PASSWORD')

try: 
    dbPool = pool.SimpleConnectionPool(
        1, 
        10, 
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        port=DB_PORT
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
            cursor.execute('CREATE TABLE IF NOT EXISTS embeddings (id SERIAL PRIMARY KEY,user_id INT NOT NULL,embedding vector(768))')
        conn.commit()
    except Exception as e:
        print('Create Embeddings Table Error', e)
        raise HTTPException(status_code=500, detail=str(e))
    finally: 
        dbPool.putconn(conn)



