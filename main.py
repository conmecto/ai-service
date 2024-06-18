from fastapi import FastAPI
from db import createEmbeddingsTable
from processImage import fetchImage, processImage, generateEmbeddings
from dbInsert import insertEmbedding
from pydantic import BaseModel

createEmbeddingsTable()

class File(BaseModel):
    userId: int
    fileName: str
    url: str
    postIdRef: int

app = FastAPI()

@app.post("/v1/images/generate-embeddings")
def generateEmbeddings(file: File):
    fileObj = file.model_dump()
    url = fileObj['url']
    fileName = fileObj['fileName']
    userId  = fileObj['userId']
    postIdRef = fileObj['postIdRef']
    imagePath = 'temp/' + fileName
    fetchImage(url, imagePath)
    processImage(imagePath, userId, postIdRef)
    return { "message": "Image added successfully" }
    
            