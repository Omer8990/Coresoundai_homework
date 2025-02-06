from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Image

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 6),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'image_processing',
    default_args=default_args,
    description='Process pending images',
    schedule_interval=timedelta(minutes=5),
    catchup=False
)


def get_pending_images():
    engine = create_engine('postgresql://user:password@postgres:5432/images')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        pending_images = session.query(Image).filter(Image.status == 'pending').all()
        return [str(image.id) for image in pending_images]
    finally:
        session.close()


def submit_batch(ti):
    pending_image_ids = ti.xcom_pull(task_ids='get_pending_images')
    if not pending_image_ids:
        return "No pending images found"

    response = requests.post(
        'http://api:8000/submit_batch',
        json={'image_ids': pending_image_ids}
    )
    response.raise_for_status()
    return "Batch submitted successfully"


def monitor_completion(ti):
    pending_image_ids = ti.xcom_pull(task_ids='get_pending_images')
    if not pending_image_ids:
        return "No images to monitor"

    engine = create_engine('postgresql://user:password@postgres:5432/images')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for image_id in pending_image_ids:
            image = session.query(Image).filter(Image.id == image_id).first()
            if image and image.status not in ['completed', 'failed']:
                raise Exception(f"Image {image_id} processing incomplete")
    finally:
        session.close()

    return "All images processed"


with dag:
    get_pending_task = PythonOperator(
        task_id='get_pending_images',
        python_callable=get_pending_images,
    )

    submit_batch_task = PythonOperator(
        task_id='submit_batch',
        python_callable=submit_batch,
    )

    monitor_task = PythonOperator(
        task_id='monitor_completion',
        python_callable=monitor_completion,
    )

    get_pending_task >> submit_batch_task >> monitor_task
