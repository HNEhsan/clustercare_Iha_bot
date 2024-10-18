''' Patient Models '''
from jdatetime import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from Database.models.doctor import Doctor

engine = create_engine('sqlite:///./Database/bot.db')
Base = declarative_base()


class Patient(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'tbl_patient'
    id = Column(Integer, primary_key=True)
    chat_id = Column(String, unique=False, nullable=False)
    name = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    created_at = Column(String, default=str(datetime.now().replace(
        microsecond=0)), nullable=False)
    doctor_id = Column(Integer, ForeignKey(Doctor.id), nullable=True)
    doctor = relationship(Doctor)

    def __str__(self):
        return f"name='{self.name}', phone='{self.phone}'"


def create_table():
    """
    create models
    """
    Base.metadata.create_all(engine)
