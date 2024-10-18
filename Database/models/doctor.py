''' Doctor Models '''
from jdatetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


engine = create_engine('sqlite:///./Database/bot.db')
Base = declarative_base()


class Doctor(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'tbl_doctor'
    id = Column(Integer, primary_key=True)
    chat_id = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    medical_system_number = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=False)
    created_at = Column(String, default=str(datetime.now().replace(
        microsecond=0)), nullable=False)

    def __str__(self):
        return f"name='{self.name}', phone='{self.phone}'"


def create_table():
    """
    create models
    """
    Base.metadata.create_all(engine)
