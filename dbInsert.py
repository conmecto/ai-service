from db import dbPool
from fastapi import HTTPException

def insertEmbedding(userId, embedding):
    if (dbPool.closed):
        print('Pool connection closed')
        return
    conn = dbPool.getconn()
    try: 
        cursor = conn.cursor()
        cursor.execute('INSERT INTO embeddings (user_id, embedding) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET embedding = EXCLUDED.embedding', (userId, embedding))
        conn.commit()
    except Exception as e: 
        print('Insert embedding error', e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        dbPool.putconn(conn)