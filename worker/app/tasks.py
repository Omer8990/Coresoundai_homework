from celery import Celery
from PIL import Image as PILImage
import random
import os
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Image

# Initialize Celery
celery_app = Celery('tasks')
celery_app.conf.broker_url = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
celery_app.conf.result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

PROCESSED_DIR = "/app/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)


@celery_app.task(bind=True, max_retries=3)
def process_image(self, image_id: str):
    db = SessionLocal()
    try:
        # Get image record
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise ValueError(f"Image {image_id} not found")

        # Update status to processing
        image.status = 'processing'
        db.commit()

        # Open and process image
        with PILImage.open(image.original_image_path) as img:
            # Get image dimensions
            width, height = img.size

            # Generate random crop dimensions
            crop_width = random.randint(width // 4, width // 2)
            crop_height = random.randint(height // 4, height // 2)

            # Calculate random position
            crop_x = random.randint(0, width - crop_width)
            crop_y = random.randint(0, height - crop_height)

            # Perform crop
            cropped_img = img.crop((crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))

            # Save processed image
            processed_filename = f"processed_{image_id}.png"
            processed_path = os.path.join(PROCESSED_DIR, processed_filename)
            cropped_img.save(processed_path)

            # Update database
            image.processed_image_path = processed_path
            image.crop_x = crop_x
            image.crop_y = crop_y
            image.crop_width = crop_width
            image.crop_height = crop_height
            image.status = 'completed'
            db.commit()

    except Exception as exc:
        # Update status to failed and retry
        image.status = 'failed'
        db.commit()
        raise self.retry(exc=exc)

    finally:
        db.close()
