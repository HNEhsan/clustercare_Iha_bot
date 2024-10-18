''' Telegram App '''
import os
import logging
import telebot
from telebot import types
from dotenv import load_dotenv
from App.profile import view_profile
from App.report import report_doctor, report_patient, report_log
from App.register import (
    handle_type, init_doctor, init_patient, handle_value, update_state)
from Database.models.doctor import create_table as doctor_create_table
from Database.ORM.doctor import create_doctor, select_with_chat_id
from Database.models.patient import create_table as patient_create_table
from Database.ORM.patient import create_patient, select_with_phone

# load data from .env file
load_dotenv()

# init log
logging.basicConfig(filename='./Log/bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# init bot
bot = telebot.TeleBot(os.getenv('TOKEN'))

# save user state
user_states = {}


# callback handlers data
callback_handlers = {
    'init_patient': lambda call: init_patient(call, bot=bot, user_states=user_states),
    'init_doctor': lambda call: init_doctor(call, bot=bot, user_states=user_states),
    'report_doctor': lambda call: report_doctor(call, bot=bot),
    'report_patient': lambda call: report_patient(call, bot=bot),
    'report_log': lambda call: report_log(call, bot=bot),
    'view_profile': lambda call: view_profile(call, bot=bot),
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states[message.from_user.id] = {'type': None, 'state': None}
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(
        'ثبت بیمار', callback_data='init_patient')
    res = select_with_chat_id(chat_id=message.chat.id)
    if res is not None:
        btn2 = telebot.types.InlineKeyboardButton(
            'مشاهده پروفایل', callback_data='view_profile')
    else:
        btn2 = telebot.types.InlineKeyboardButton(
            'ثبت پزشک', callback_data='init_doctor')
    markup.add(btn1, btn2)
    bot.send_message(
        message.chat.id, "لطفا گزینه مورد نظر را انتخاب کنید:", reply_markup=markup)


@bot.message_handler(commands=['register_patient'])
def send_init_register_patient(message):
    logging.info("init new register_patient")
    logging.info("update user state type to patient")
    if message.chat.id not in user_states:
        user_states[message.chat.id] = {'type': None, 'state': None}
    if user_states[message.chat.id]["type"] is None or user_states[message.chat.id]["type"] != "patient":
        handle_type(message=message,
                    user_states=user_states, type="patient")
        logging.info("update user state states to name")
        update_state(user_id=message.chat.id,
                     user_states=user_states,
                     new_state="name", type="patient")
        bot.send_message(message.chat.id,
                         "لطفا نام و نام خانوادگی بیمار را وارد کنید")


@bot.message_handler(commands=['register_doctor'])
def send_init_register_doctor(message):
    res = select_with_chat_id(chat_id=message.chat.id)
    if res:
        bot.send_message(
            message.chat.id, "شما در سیستم دارای حساب کاربری هستید.")
        return
    logging.info("init new register_doctor")
    logging.info("update user state type to doctor")
    if message.chat.id not in user_states:
        user_states[message.chat.id] = {'type': None, 'state': None}
    if user_states[message.chat.id]["type"] is None or user_states[message.chat.id]["type"] != "doctor":
        handle_type(message=message,
                    user_states=user_states, type="doctor")
        logging.info("update user state states to name")
        update_state(user_id=message.chat.id,
                     user_states=user_states,
                     new_state="name", type="doctor")
        bot.send_message(message.chat.id,
                         "لطفا نام و نام خانوادگی خود را وارد کنید")


@bot.message_handler(commands=['admin'])
def handle_report(message):
    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(
            message, "اطلاعات ورودی صحیح نمی باشد.")
        return
    username, password = args[1], args[2]
    admin_username = os.getenv("PASSWORD")
    admin_password = os.getenv("PASSWORD")
    admin_password = hash(admin_password)
    password = hash(password)
    if not (admin_username == username) and (admin_password == password):
        bot.reply_to(
            message, "نام کاربری یا رمز عبور صحیح نمی باشد")
        return

    bot.reply_to(
        message, "به بخش ادمین خوش آمدید")
    logging.info("create report menu")
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        "مشاهده اطلاعات پزشکان", callback_data="report_doctor")
    btn2 = types.InlineKeyboardButton(
        "مشاهده اطلاعات بیماران", callback_data="report_patient")
    btn3 = types.InlineKeyboardButton(
        "مشاهده لاگ ربات", callback_data="report_log")
    markup.add(btn1, btn2, btn3)
    bot.send_message(
        message.chat.id, "لطفا گزینه مورد نظر را انتخاب کنید:", reply_markup=markup)


@bot.message_handler(commands=['profile'])
def handle_profile(message):
    res = select_with_chat_id(chat_id=message.chat.id)
    if res is not None:
        text = f"""
        نام و نام خا نوادگی : {res.name}
        شماره تلفن همراه : {res.phone}
        شماره نظام پزشکی : {res.medical_system_number}
        شهر : {res.city}
        """
        bot.send_message(
            message.chat.id, text)
    else:
        bot.send_message(
            message.chat.id, "شما پروفایل کاربری ندارید")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data in callback_handlers:
            callback_handlers[call.data](call)
        else:
            bot.answer_callback_query(call.id, 'گزینه نامعتبر.')
    except Exception as e:
        logging.error(f"Error processing callback: {str(e)}")
        bot.answer_callback_query(
            call.id, 'متاسفانه خطایی رخ داده است. لطفا مجددا تلاش کنید.')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id in user_states:
        type = user_states[user_id]['type']
        state = user_states[user_id]['state']
        if type == "doctor":
            res = select_with_chat_id(chat_id=message.chat.id)
            if res:
                bot.send_message(
                    message.chat.id, "شما در سیستم دارای حساب کاربری هستید.")
                return
            if state == 'name':
                handle_value(message=message,
                             user_states=user_states, state=state)
                update_state(user_id=message.chat.id, user_states=user_states,
                             new_state="phonenumber", type="doctor")
                bot.send_message(
                    message.chat.id, "لطفا شماره تلفن همراه خود را وارد نمایید")
            elif state == 'phonenumber':
                if len(message.text) != 11:
                    bot.send_message(
                        message.chat.id, "ورودی صحیح نمی باشد.")
                    bot.send_message(
                        message.chat.id, "لطفا شماره تلفن همراه خود را وارد نمایید")
                    return
                handle_value(message=message,
                             user_states=user_states, state=state)
                update_state(user_id=message.chat.id, user_states=user_states,
                             new_state="doctorid", type="doctor")
                bot.send_message(
                    message.chat.id, "لطفا شماره ی نظام پزشکی خود را وارد نمایید")
            elif state == 'doctorid':
                if not (4 <= len(message.text) <= 6):
                    bot.send_message(
                        message.chat.id, "ورودی صحیح نمی باشد.")
                    bot.send_message(
                        message.chat.id, "لطفا شماره ی نظام پزشکی خود را وارد نمایید")
                    return
                handle_value(message=message,
                             user_states=user_states, state=state)
                update_state(user_id=message.chat.id, user_states=user_states,
                             new_state="city", type="doctor")
                bot.send_message(
                    message.chat.id, "لطفا نام شهر خود را وارد نمایید")
            elif state == 'city':
                handle_value(message=message,
                             user_states=user_states, state=state)
                update_state(user_id=message.chat.id, user_states=user_states,
                             new_state="done", type="doctor")
                text = f""" 
آقا / خانم دکتر 
{user_states[message.chat.id]["value_name"]}
از همکاری شما صمیمانه سپاسگزاریم ،
همکاران ما در انجمن علمی سردرد ایران در اسرع وقت با بیمار شما ارتباط خواهند گرفت، 
ریاست انجمن سردرد ایران 
دکتر منصوره تقا
                        """
                bot.send_message(
                    message.chat.id, text)
                bot.send_message(
                    message.chat.id, "برای ثبت بیمار برروی لینک زیر کلیک نمایید. \n /register_patient")

                logging.info("register new doctor")
                doctor_info: dict = user_states[message.chat.id]
                create_doctor(chat_id=message.chat.id, city=doctor_info["value_city"],
                              medical_system_number=doctor_info["value_doctorid"],
                              name=doctor_info["value_name"], phone=doctor_info["value_phonenumber"])
        else:
            if state == 'name':
                handle_value(message=message,
                             user_states=user_states, state=state)
                update_state(user_id=message.chat.id, user_states=user_states,
                             new_state="phonenumber", type="patient")
                bot.send_message(
                    message.chat.id, "لطفا شماره تلفن همراه بیمار را وارد نمایید")
            elif state == 'phonenumber':
                if len(message.text) != 11:
                    bot.send_message(
                        message.chat.id, "ورودی صحیح نمی باشد.")
                    bot.send_message(
                        message.chat.id, "لطفا شماره تلفن همراه بیمار را وارد نمایید")
                    return
                handle_value(message=message,
                             user_states=user_states, state=state)
                update_state(user_id=message.chat.id, user_states=user_states,
                             new_state="done", type="patient")

                logging.info("check patien exist")
                res = select_with_phone(
                    phone=user_states[message.chat.id]['value_phonenumber'])
                if res and res is not None:
                    bot.send_message(
                        message.chat.id, "بیمار با این مشخصات قبلا در سیستم وارد شده است")
                    user_states[message.from_user.id] = {
                        'type': None, 'state': None}
                    return
                bot.send_message(
                    message.chat.id, "از همکاری شما سپاسگزاریم, \n همکاران ما در انجمن علمی سردرد در اسرع وقت با بیمار شما ارتباط خواهند گرفت.")
                logging.info("register new patient")
                patient_info = user_states[message.chat.id]
                res = select_with_chat_id(chat_id=message.chat.id)
                doctor_id = None
                if res:
                    doctor_id = res.id
                create_patient(name=patient_info['value_name'], chat_id=message.chat.id,
                               phone=patient_info['value_phonenumber'], doctor_id=doctor_id)
                user_states[message.from_user.id] = {
                    'type': None, 'state': None}
    else:
        # start new conversation
        user_states[message.from_user.id] = {'type': None, 'state': None}
        send_welcome(message)


# Run App
if __name__ == "__main__":
    logging.info("app is runnig ...")
    logging.info("create databse")
    patient_create_table()
    doctor_create_table()
    print("Bot is runnig ...")
    while True:
        try:
            bot.polling(True)
        except Exception as e:
            logging.error(f"Main App has error : {e}")
