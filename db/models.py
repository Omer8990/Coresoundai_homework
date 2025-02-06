import uuid
from sqlalchemy import Column, String, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Image(Base):
    __tablename__ = 'images'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_image_path = Column(String, nullable=False)
    processed_image_path = Column(String, nullable=True)
    crop_x = Column(Integer, nullable=True)
    crop_y = Column(Integer, nullable=True)
    crop_width = Column(Integer, nullable=True)
    crop_height = Column(Integer, nullable=True)
    status = Column(
        SQLEnum('pending', 'processing', 'completed', 'failed', name='status_enum'),
        nullable=False,
        default='pending'
    )
