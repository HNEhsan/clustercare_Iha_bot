import logging
from telebot import TeleBot
from Database.ORM.doctor import select_with_chat_id


def handle_type(message: str, user_states: dict, type: str) -> None:
    """_summary_

    Args:
        message (str): _description_
        user_states (dict): _description_
        type (str): _description_
    """
    user_id = message.chat.id
    user_states[user_id]["type"] = type


def handle_value(message, user_states: dict, state: str) -> None:
    """_summary_

    Args:
        message (_type_): _description_
        user_states (dict): _description_
        state (str): _description_
    """
    user_id = message.chat.id
    user_states[user_id][f"value_{state}"] = message.text


def update_state(user_id, user_states: dict, type: str, new_state: str) -> None:
    """
    Updates the state for a user in the user_states dictionary.

    Args:
        user_id (_type_): _description_
        user_states (dict): _description_
        type (str): _description_
        new_state (str): _description_
    """

    if user_id in user_states:
        user_states[user_id]['state'] = new_state
    else:
        user_states[user_id] = {'type': type,
                                'state': new_state, "value": None}


def init_patient(call, user_states: dict, bot: TeleBot) -> None:
    """_summary_

    Args:
        call (_type_): _description_
        user_states (dict): _description_
        bot (TeleBot): _description_
    """
    logging.info("init new patien")
    logging.info("update user state type to patient")
    if call.message.chat.id not in user_states:
        user_states[call.message.chat.id] = {'type': None, 'state': None}
    if user_states[call.message.chat.id]["type"] != "patient":
        handle_type(message=call.message,
                    user_states=user_states, type="patient")
        logging.info("update user state states to name")
        update_state(user_id=call.message.chat.id,
                     user_states=user_states,
                     new_state="name", type="patient")
        bot.send_message(call.message.chat.id,
                         "لطفا نام و نام خانوادگی بیمار را وارد کنید")
        return


def init_doctor(call, user_states: dict, bot: TeleBot):
    """_summary_

    Args:
        call (_type_): _description_
        user_states (dict): _description_
        bot (TeleBot): _description_
    """
    res = select_with_chat_id(chat_id=call.message.chat.id)
    if res:
        bot.send_message(
            call.message.chat.id, "شما در سیستم دارای حساب کاربری هستید.")
        return
    logging.info("init new patien")
    logging.info("update user state type to doctor")
    if not user_states[call.message.chat.id] or call.message.chat.id not in user_states:
        user_states[call.message.chat.id] = {'type': None, 'state': None}
    if user_states[call.message.chat.id]["type"] is None or user_states[call.message.chat.id]["type"] != "doctor":
        handle_type(message=call.message,
                    user_states=user_states, type="doctor")
        logging.info("update user state states to name")
        update_state(user_id=call.message.chat.id,
                     user_states=user_states,
                     new_state="name", type="doctor")
        bot.send_message(call.message.chat.id,
                         "نام و نام خانوادگی خود را وارد کنید")
        return
