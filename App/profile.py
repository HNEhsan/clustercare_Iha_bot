
import logging
from telebot import TeleBot
from Database.ORM.doctor import select_with_chat_id


def view_profile(call, bot: TeleBot) -> None:
    logging.info("see profile")
    res = select_with_chat_id(chat_id=call.message.chat.id)
    if res is not None:
        text = f"""
    نام و نام خا نوادگی : {res.name}
    شماره تلفن همراه : {res.phone}
    شماره نظام پزشکی : {res.medical_system_number}
    شهر : {res.city}
        """
        bot.send_message(
            call.message.chat.id, text)
    else:
        bot.send_message(
            call.message.chat.id, "شما پروفایل کاربری ندارید")
