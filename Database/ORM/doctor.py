from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.models.patient import Doctor

engine = create_engine('sqlite:///./Database/bot.db')
Session = sessionmaker(bind=engine)
session = Session()


def create_doctor(chat_id: str, name: str, phone: str, medical_system_number: str, city: str):
    """
    Register New Doctor

    Args:
        chat_id (str): _description_
        name (str): _description_
        phone (str): _description_
        medical_system_number (str): _description_
        city (str): _description_
    """
    engine = create_engine('sqlite:///./Database/bot.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    new_doctor = Doctor(name=name, phone=phone, chat_id=chat_id,
                        medical_system_number=medical_system_number, city=city)
    session.add(new_doctor)
    session.commit()
    session.close()


def select_with_chat_id(chat_id: str) -> Doctor:
    """
    _summary_

    Args:
        chat_id (str): _description_

    Returns:
        bool: _description_
    """
    engine = create_engine('sqlite:///./Database/bot.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Doctor).filter_by(chat_id=chat_id).first()
    session.close()
    return result


def select_all() -> Union[list, None]:
    engine = create_engine('sqlite:///./Database/bot.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Doctor).all()
    session.close()
    return result
