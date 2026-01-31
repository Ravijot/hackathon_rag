import os
from src.pipeline import Pipeline
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

# Allowed file extensions
ALLOWED_EXTENSIONS = {".html", ".md", ".pdf"}

pipeline = Pipeline()

def is_allowed_file(filename: str) -> bool:
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        if not is_allowed_file(file.filename):
            raise HTTPException(status_code=400, detail="File type not supported")

        file_location = os.path.join(DATA_FOLDER, file.filename)
        file_type = file.filename.split('.')[-1]
        
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

        response = pipeline.process_document(file_location, file_type)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@app.post("/query/")
async def query_api(query: str):
    try:
        response = pipeline.query(query)
        return {"response": response}
    except Exception as e:
        print(f"Error in Queries API : {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
