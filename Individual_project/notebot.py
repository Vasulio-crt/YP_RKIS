import telebot, json, threading, datetime, os
from json import JSONDecodeError
from telebot.types import Message

TOKEN = str(os.environ.get('TOKEN'))

bot = telebot.TeleBot(TOKEN)

FILE_PATH_id_save = os.path.dirname(__file__) + "/id_save.json"
print(FILE_PATH_id_save)

def overwriting_file(new_save: dict, mes_id: str):
    with open(FILE_PATH_id_save, "r", encoding="UTF-8") as file:
        data_user = json.load(file)
    data_user[mes_id] = new_save
    with open(FILE_PATH_id_save, "w", encoding="UTF-8") as file:
        json.dump(data_user, file, indent=2, ensure_ascii=False)

def view_notes(user_dict: dict, message_id, text: str):
    s = str()
    for i, (k, v) in enumerate(user_dict.items()):
        s += f"Заметка> {k} < == {v if len(v) < 30 else v[:30]+"..."}\n"#18 + 45
        if (i + 1) % 35 == 0:
            bot.send_message(message_id, "Список заметок\n" + s)
            s = ""
    if s:
        bot.send_message(message_id, f"{text}\n" + s)


@bot.message_handler(commands=['start'])
def start_command(message: Message):
    try:
        with open(FILE_PATH_id_save, "r", encoding="UTF-8") as file:
            data_user = json.load(file)
    except JSONDecodeError:
        data_user = dict()
    message_id = str(message.chat.id)
    if message_id not in data_user:
        data_user[message_id] = {}
        bot.send_message(message_id, "Приветствуем вас в нашем боте для заметок и памяток")
        with open(FILE_PATH_id_save, "w", encoding="UTF-8") as file:
            json.dump(data_user, file, indent=2, ensure_ascii=False)
    else:
        bot.send_message(message_id, "Вы уже водили эту команду!")



@bot.message_handler(commands=['help'])
def help_or_reference(message: Message):
    warning = "ВАЖНО ЕСЛИ БОТ ПЕРЕЗАПУСТИТСЯ ТО ВСЕ ВАШИ НАПОМИНАНИЯ СБРОСИТСЯ!!!"
    s0 = "Справка о командах:\n"
    s1 = "/create_note, /createNote, /cn - Создать заметку\n"
    s2 = "/show_note, /showNote, /sn - Просмотреть заметки\n"
    s3 = "/delete_note, /deleteNote, /dn - Удалить заметку\n"
    s4 = "/editing_note, /editingNote, /en - Изменить заметку\n"
    s5 = "/exit - Завершает действие (работает в запушенных командах)\n"
    s6 = "/name_editing_note, /nameEditingNote, /nen - Редактирование имени заметки\n"
    s_end = f"/reminder - Сделать напоминание({warning})\n"
    s_end_2 = "/clear_note, /clearNote - Удаление всех заметок"
    bot.send_message(message.chat.id, s0 + s1 + s2 + s3 + s4 + s6 + s5 + s_end +s_end_2)


@bot.message_handler(commands=["create_note", "createNote", "cn"])
def create_note(message: Message):
    bot.delete_message(message.chat.id, message.id)
    bot.send_message(message.chat.id, "Напишете название заметки формата:\nназвание_заметки - Описание_заметки")
    bot.register_next_step_handler(message, create_note_new)

def create_note_new(message: Message):
    if message.text == "/exit":
        return
    message_id = str(message.chat.id)
    message_proces = message.text.split(" - ", maxsplit=1)
    if len(message_proces) == 2:
        if len(message_proces[0]) <= 60 and len(message_proces[1]) <= 340:
            with open(FILE_PATH_id_save, "r", encoding="UTF-8") as file:
                data_user = json.load(file)
                if message_proces[0] in data_user[message_id]:
                    bot.send_message(message_id, "Название уже существует. Попробуй ещё раз!")
                    bot.register_next_step_handler(message, create_note_new)
                    return

            message_note = data_user[message_id]
            message_note[message_proces[0]] = message_proces[1]
            data_user[message_id] = message_note

            with open(FILE_PATH_id_save, "w", encoding="UTF-8") as file:
                json.dump(data_user, file, indent=2, ensure_ascii=False)
            bot.send_message(message_id, "Заметка успешно создана!")
        else:
            bot.send_message(message_id, "Превышен лимит на кол-во символов.\nНазвание 60 символов "
                                         "или описание 340 символов. Попробуй ещё раз!")
            bot.register_next_step_handler(message, create_note_new)
    else:
        bot.send_message(message_id, "Неправильный формат ввода. Попробуй ещё раз!")
        bot.register_next_step_handler(message, create_note_new)


@bot.message_handler(commands=["show_note", "showNote", "sn"])
def show_note(message: Message):
    bot.delete_message(message.chat.id, message.id)
    message_id = str(message.chat.id)
    with open(FILE_PATH_id_save, "r", encoding="UTF-8") as file:
        data_user = json.load(file)
    if len(data_user[message_id]) != 0:
        s = str()#9*400(3600)+189+99+15
        user_dict: dict = data_user[message_id]
        for i, (k, v) in enumerate(user_dict.items()):
            s += "=" * 19 + "=\n" + f"Заметка {k}:\n{v}\n"
            if (i + 1) % 9 == 0:
                bot.send_message(message_id, "Список заметок\n" + s)
                s = ""

        if s:
            bot.send_message(message_id, "Список заметок\n" + s)

    else:
        bot.send_message(message_id, "У вас нет заметок! Создать заметку /createNote")


@bot.message_handler(commands=["delete_note", "deleteNote", "dn"])
def delete_note(message: Message):
    bot.delete_message(message.chat.id, message.id)
    message_id = str(message.chat.id)
    with open(FILE_PATH_id_save, "r", encoding="UTF-8") as file:
        data_user = json.load(file)
    if len(data_user[message_id]) != 0:
        view_notes(data_user[message_id], message_id, "Чтобы удалить заметку напишите её название:")
        bot.register_next_step_handler(message, del_note, data_user[message_id])
    else:
        bot.send_message(message_id, "У вас нет заметок! Создать заметку /createNote")


def del_note(message: Message, user_dict: dict):
    if message.text == "/exit":
        return
    try:
        user_dict.pop(message.text)
        overwriting_file(user_dict, str(message.chat.id))
        bot.send_message(message.chat.id, "Заметка удалена успешно!")
    except KeyError:
        bot.send_message(message.chat.id, "Нет такого названия. Попробуй ещё раз!")
        bot.register_next_step_handler(message, del_note, user_dict)


@bot.message_handler(commands=["name_editing_note", "nameEditingNote", "nen"])
def name_editing_note(message: Message):
    bot.delete_message(message.chat.id, message.id)
    message_id = str(message.chat.id)
    with open(FILE_PATH_id_save, "r", encoding="UTF-8") as file:
        data_user = json.load(file)
    if len(data_user[message_id]) != 0:
        view_notes(data_user[message_id], message_id, "Чтобы изменить имя заметки напишите её название:")
        bot.register_next_step_handler(message, pre_n_edit_note, data_user[message_id])
    else:
        bot.send_message(message_id, "У вас нет заметок! Создать заметку /createNote")

def pre_n_edit_note(message: Message, user_dict: dict):
    if message.text == "/exit":
        return
    mes_text = message.text
    if mes_text in user_dict:
        bot.send_message(message.chat.id, "Введите новое название заметки.")
        bot.register_next_step_handler(message, n_edit_note, user_dict, mes_text)
    else:
        bot.send_message(message.chat.id, "Нет такого названия. Попробуй ещё раз!")
        bot.register_next_step_handler(message, pre_n_edit_note, user_dict)

def n_edit_note(message: Message, user_dict: dict, mes_text):
    if message.text == "/exit":
        return
    if message.text in user_dict:
        bot.send_message(message.chat.id, "Название уже существует. Попробуй ещё раз!")
        bot.register_next_step_handler(message, n_edit_note, user_dict, mes_text)
        return
    if len(message.text) <= 60:
        user_dict[message.text] = user_dict.pop(mes_text)
        overwriting_file(user_dict, str(message.chat.id))
        bot.send_message(message.chat.id, "Заметка изменена успешно!")
    else:
        bot.send_message(message.chat.id, "Название превышает лимит в 60 символов!\nПопробуй ещё раз!")
        bot.register_next_step_handler(message, pre_n_edit_note, user_dict)


@bot.message_handler(commands=["editing_note", "editingNote", "en"])
def editing_note(message: Message):
    bot.delete_message(message.chat.id, message.id)
    message_id = str(message.chat.id)
    with open(FILE_PATH_id_save, "r", encoding="UTF-8") as file:
        data_user = json.load(file)
    if len(data_user[message_id]) != 0:
        view_notes(data_user[message_id], message_id, "Чтобы изменить заметку напишите её название:")
        bot.register_next_step_handler(message, pre_edit_note, data_user[message_id])
    else:
        bot.send_message(message_id, "У вас нет заметок! Создать заметку /createNote")

def pre_edit_note(message: Message, user_dict: dict):
    if message.text == "/exit":
        return
    mes_text = message.text
    if mes_text in user_dict:
        bot.send_message(message.chat.id, "Введите новое описание заметки.")
        bot.register_next_step_handler(message, edit_note, user_dict, mes_text)
    else:
        bot.send_message(message.chat.id, "Нет такого названия. Попробуй ещё раз!")
        bot.register_next_step_handler(message, pre_edit_note, user_dict)

def edit_note(message: Message, user_dict: dict, mes_text):
    if message.text == "/exit":
        return
    if len(message.text) <= 340:
        user_dict[mes_text] = message.text
        overwriting_file(user_dict, str(message.chat.id))
        bot.send_message(message.chat.id, "Заметка изменена успешно!")
    else:
        bot.send_message(message.chat.id, "Описание превышает лимит в 340 символов!\nПопробуй ещё раз!")
        bot.register_next_step_handler(message, pre_edit_note, user_dict)


@bot.message_handler(commands=["clear_note", "clearNote"])
def clear_note(message: Message):
    mes_id, mes_txt = str(message.chat.id), message.text.lower()
    if mes_txt in ["/clear_note", "/clearnote"]:
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, "Вы точно хотите удалить все ваши заметки. Если да, то напишите да")
    if mes_txt == "да":
        with open(FILE_PATH_id_save, "r", encoding="UTF-8") as file:
            data_user = json.load(file)
        data_user[mes_id] = {}
        with open(FILE_PATH_id_save, "w", encoding="UTF-8") as file:
            json.dump(data_user, file, indent=2, ensure_ascii=False)
        bot.send_message(mes_id, "Ваши заметки полностью удаленны!")
        return
    bot.register_next_step_handler(message, clear_note)


@bot.message_handler(commands=['reminder'])
def reminder_message(message: Message):
    bot.delete_message(message.chat.id, message.id)
    with open(FILE_PATH_id_save, "r", encoding="UTF-8") as file:
        data_user = json.load(file)
    view_notes(data_user[str(message.chat.id)], message.chat.id, "Введите название заметки, который нужно поставить напоминание:")
    bot.register_next_step_handler(message, set_reminder_name, data_user[str(message.chat.id)])

def set_reminder_name(message, user_data: dict):
    if message.text == "/exit":
        return
    mes_text = message.text
    if mes_text in user_data:
        bot.send_message(message.chat.id, 'Введите дату и время, когда вы хотите '
                                          'получить напоминание в формате ГГГГ-ММ-ДД чч:мм.')
        user_data = (mes_text, user_data[mes_text])
        bot.register_next_step_handler(message, reminder_set, user_data)
    else:
        bot.send_message(message.chat.id, "Нет такого названия. Попробуй ещё раз!")
        bot.register_next_step_handler(message, set_reminder_name, user_data)

def reminder_set(message, user_data: tuple):
    if message.text == "/exit":
        return
    try:
        reminder_time = datetime.datetime.strptime(message.text, '%Y-%m-%d %H:%M')
        now = datetime.datetime.now()
        delta = reminder_time - now
        if delta.total_seconds() <= 0:
            bot.send_message(message.chat.id, 'Вы ввели прошедшую дату, попробуйте еще раз.')
        else:
            bot.send_message(message.chat.id, f"Напоминание установлено на {reminder_time.strftime("%Y-%m-%d %H:%M")}")
            reminder_timer = threading.Timer(delta.total_seconds(), send_reminder, [message.chat.id, user_data])
            reminder_timer.start()
            return
    except ValueError:
        bot.send_message(message.chat.id, 'Вы ввели неверный формат даты и времени, попробуйте еще раз.')
    bot.register_next_step_handler(message, reminder_set, user_data)

def send_reminder(chat_id, user_data: tuple):
    bot.send_message(chat_id, f"Время получить вашу заметку {user_data[0]} на установленное вами время!"
                              f"\nЕго наполнение:\n{user_data[1]}")

bot.infinity_polling(skip_pending=True)
