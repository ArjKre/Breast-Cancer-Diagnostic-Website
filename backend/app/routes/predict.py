from pathlib import Path

from fastapi import APIRouter, File, UploadFile

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    filepath = UPLOAD_DIR / file.filename

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "prediction": "Malignant",
        "confidence": 0.91,
        "risk_level": "High",
        "filename": file.filename,
    }
