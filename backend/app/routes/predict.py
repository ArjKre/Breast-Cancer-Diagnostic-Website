from pathlib import Path

from app.services.predictor import predict as run_prediction
from fastapi import APIRouter, File, UploadFile

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    filepath = UPLOAD_DIR / file.filename

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    result = run_prediction(filepath)

    return {"filename": file.filename, **result}
