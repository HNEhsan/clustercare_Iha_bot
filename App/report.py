''' Remport Module '''
import logging
import pandas as pd
from telebot import TeleBot
from Database.ORM.patient import select_all as select_all_patients
from Database.ORM.doctor import select_all as select_all_doctors


def report_log(call, bot: TeleBot) -> None:
    """_summary_

    Args:
        call (_type_): _description_
        bot (TeleBot): _description_
    """
    try:
        with open("./Log/bot.log", "r", encoding="utf-8") as file:
            bot.send_document(call.message.chat.id, file)
    except Exception as e:
        logging.error(f"Error sending file: {str(e)}")
        bot.answer_callback_query(
            call.id, "خطایی در ارسال فایل لاگ رخ داده است.")


def report_doctor(call, bot: TeleBot) -> None:
    """_summary_

    Args:
        call (_type_): _description_
        bot (TeleBot): _description_
    """
    try:
        all_docotors = select_all_doctors()
        if not all_docotors:
            bot.answer_callback_query(
                call.id, "لیستی از بیماران برای نمایش وجود ندارد.")
            return
        data = []
        for doctors in all_docotors:
            temp = {
                'id': doctors.id,
                'chat_id': doctors.chat_id,
                'name': doctors.name,
                'phone': doctors.phone,
                'medical_system_number': doctors.phone,
                'city': doctors.phone,
                'created_at': doctors.created_at,
            }
            data.append(temp)

        df = pd.DataFrame(data)
        df.to_excel('./Report/docotors.xlsx', index=False)
        with open("./Report/docotors.xlsx", "rb") as file:
            bot.send_document(call.message.chat.id, file)
    except Exception as e:
        logging.error(f"in section report_doctors has error :  {e}")
        bot.send_message(
            call.id, "متاسفانه در تهیه لیست بیماران مشکلی پیش آمده است.")
    finally:
        if 'file' in locals():
            file.close()


def report_patient(call, bot: TeleBot) -> None:
    """_summary_

    Args:
        call (_type_): _description_
        bot (TeleBot): _description_
    """
    try:
        all_patients = select_all_patients()
        if not all_patients:
            bot.answer_callback_query(
                call.id, "لیستی از بیماران برای نمایش وجود ندارد.")
            return
        data = []
        for patient in all_patients:
            temp = {
                'id': patient.id,
                'chat_id': patient.chat_id,
                'name': patient.name,
                'phone': patient.phone,
                'created_at': patient.created_at,
            }
            data.append(temp)

        df = pd.DataFrame(data)
        df.to_excel('./Report/patients.xlsx', index=False)
        with open("./Report/patients.xlsx", "rb") as file:
            bot.send_document(call.message.chat.id, file)
    except Exception as e:
        logging.error(f"in section report_patient has error :  {e}")
        bot.send_message(
            call.id, "متاسفانه در تهیه لیست بیماران مشکلی پیش آمده است.")
    finally:
        if 'file' in locals():
            file.close()
