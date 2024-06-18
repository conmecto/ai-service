from db import dbPool
from fastapi import HTTPException

def insertEmbedding(userId, postIdRef, embedding):
    if (dbPool.closed):
        print('Pool connection closed')
        return
    conn = dbPool.getconn()
    try: 
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO embeddings (user_id, post_id_ref, embedding) VALUES (%s, %s, %s)', 
            (userId, postIdRef, embedding)
        )
        conn.commit()
    except Exception as e: 
        print('Insert embedding error', e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        dbPool.putconn(conn)