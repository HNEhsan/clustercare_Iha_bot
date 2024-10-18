from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.models.patient import Patient


def create_patient(name: str, phone: str, chat_id: str, doctor_id: int = None) -> None:
    """
    Register New Patient

    Args:
        name (str): _description_
        phone (str): _description_
        chat_id (str): _description_
        doctor_id (int, optional): _description_. Defaults to None.
    """
    engine = create_engine('sqlite:///./Database/bot.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    new_patient = Patient(name=name, phone=phone,
                          chat_id=chat_id, doctor_id=doctor_id)
    session.add(new_patient)
    session.commit()
    session.close()


def select_with_phone(phone: str) -> Patient:
    """
    _summary_

    Args:
        phone (str): _description_

    Returns:
        bool: _description_
    """
    engine = create_engine('sqlite:///./Database/bot.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(Patient).filter_by(phone=phone).first()
    session.close()
    return result


def select_all() -> Union[list, None]:
    engine = create_engine('sqlite:///./Database/bot.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Patient).all()
    session.close()
    return result
