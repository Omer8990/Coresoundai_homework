from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PIL import Image as PILImage
import os
import random
from db.image import Image

# Initialize Celery
celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/images")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@celery_app.task(bind=True, max_retries=3)
def process_image(self, image_id: str):
    db = SessionLocal()
    try:
        # Get image record from database
        image_record = db.query(Image).filter(Image.id == image_id).first()
        if not image_record:
            raise ValueError(f"Image record {image_id} not found")

        # Update status to processing
        image_record.status = 'processing'
        db.commit()

        # Open and process image
        with PILImage.open(image_record.original_image_path) as img:
            # Get image dimensions
            width, height = img.size

            # Generate random crop dimensions
            crop_width = random.randint(width // 4, width // 2)
            crop_height = random.randint(height // 4, height // 2)

            # Calculate random position
            crop_x = random.randint(0, width - crop_width)
            crop_y = random.randint(0, height - crop_height)

            # Perform crop
            cropped_img = img.crop((crop_x, crop_y,
                                    crop_x + crop_width,
                                    crop_y + crop_height))

            # Save processed image
            processed_path = f"/processed/{image_id}_cropped.jpg"
            cropped_img.save(processed_path)

            # Update database record
            image_record.processed_image_path = processed_path
            image_record.crop_x = crop_x
            image_record.crop_y = crop_y
            image_record.crop_width = crop_width
            image_record.crop_height = crop_height
            image_record.status = 'completed'
            db.commit()

    except Exception as exc:
        # Update status to failed
        if image_record:
            image_record.status = 'failed'
            db.commit()

        # Retry the task
        raise self.retry(exc=exc, countdown=60)

    finally:
        db.close()
