from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import os
from typing import List
from db.database import get_db
from db.models import Image
from worker.app.tasks import process_image

app = FastAPI(title="Image Processing API")

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/submit_batch")
async def submit_batch(
        files: List[UploadFile] = File(...),
        db: Session = Depends(get_db)
):
    results = []

    for file in files:
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Create database entry
        db_image = Image(
            original_image_path=file_path,
            status='pending'
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        # Queue processing task
        process_image.delay(str(db_image.id))

        results.append({
            "id": str(db_image.id),
            "status": "queued",
            "original_path": file_path
        })

    return {"message": "Batch submitted successfully", "tasks": results}


@app.get("/status/{image_id}")
def get_status(image_id: uuid.UUID, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return {
        "id": str(image.id),
        "status": image.status,
        "original_path": image.original_image_path,
        "processed_path": image.processed_image_path,
        "crop_coordinates": {
            "x": image.crop_x,
            "y": image.crop_y,
            "width": image.crop_width,
            "height": image.crop_height
        } if image.crop_x is not None else None
    }
