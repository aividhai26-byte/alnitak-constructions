"""
JobApplication model for career applications from the careers page
"""

from datetime import datetime
from app.models import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime


class JobApplication(Base):
    """JobApplication model for storing career form submissions with resume files"""

    __tablename__ = 'job_applications'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(30), nullable=False)
    role = Column(String(100))
    cover_letter = Column(Text)
    resume_filename = Column(String(255))   # original filename shown to admin
    resume_path = Column(String(500))       # path relative to static folder
    is_reviewed = Column(Boolean, default=False, index=True)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<JobApplication {self.first_name} {self.last_name} - {self.role}>'

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'cover_letter': self.cover_letter,
            'resume_filename': self.resume_filename,
            'is_reviewed': self.is_reviewed,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None
        }
