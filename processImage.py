import requests
import os
from fastapi import HTTPException
from transformers import ViTImageProcessor, ViTModel
from PIL import Image
from dbInsert import insertEmbedding

processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224-in21k')
model = ViTModel.from_pretrained('google/vit-base-patch16-224-in21k')
    
def generateEmbeddings(image): 
    try: 
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state
        embedding_array = embeddings.mean(dim=1).squeeze().detach().numpy()
        return embedding_array
    except Exception as e: 
        print('Generate embeddings error', e)
        raise HTTPException(status_code=500, detail=str(e))

def processImage(imagePath, userId, postIdRef):
    try: 
        image = Image.open(imagePath)
        embedding_array = generateEmbeddings(image)
        insertEmbedding(userId, postIdRef, embedding_array)
        if os.path.exists(imagePath):
            os.remove(imagePath)
        else:
            print("The file does not exist")
    except Exception as e: 
        print('Open Image error', e)
        raise HTTPException(status_code=500, detail=str(e))

def fetchImage(url, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response:
                    f.write(chunk)
        else:
            raise Exception("The file does not exist")
    except Exception as e:
        print('Fetch Image failed', e)
        raise HTTPException(status_code=500, detail=str(e))
    