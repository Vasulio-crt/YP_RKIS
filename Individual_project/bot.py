import requests, os, sqlite3, random
import telebot # pip install pyTelegramBotAPI
from telebot.types import Message

class DataBase:
    def __init__(self, db_name='bot_data.db'):
        self.con = sqlite3.connect(db_name)
        self.load_tables()

    def load_tables(self):
        cur = self.con.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS passwords(
                password_number INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS fake_person(
                person_number INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                birthday TEXT NOT NULL,
                gender TEXT NOT NULL);
            """)

    def add_person(self, data: tuple):
        cur = self.con.cursor()
        cur.execute("INSERT INTO fake_person VALUES(NULL, ?, ?, ?, ?, ?, ?)", data)
        self.con.commit()

    def add_password(self, password: str):
        cur = self.con.cursor()
        cur.execute("INSERT INTO passwords VALUES(NULL, ?)", (password,))
        self.con.commit()

    def __del__(self):
        self.con.close()


def fake_person_male():
    db = DataBase()
    base_url = 'https://api.randomdatatools.ru/'
    params = {
        'gender': 'man',
        'unescaped': 'false'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    db.add_person((data["FirstName"], data["LastName"], data["Email"],
        data["Phone"], data["DateOfBirth"], data["Gender"]))
    return data

def fake_person_female():
    db = DataBase()
    base_url = 'https://api.randomdatatools.ru/'
    params = {
        'gender': 'woman',
        'unescaped': 'false'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    db.add_person((data["FirstName"], data["LastName"], data["Email"],
        data["Phone"], data["DateOfBirth"], data["Gender"]))
    return data

def random_password(length = 16):
    db = DataBase()
    base_url = 'https://api.genratr.com/?uppercase&lowercase&numbers'
    response = requests.get(base_url, params={"length": length})
    data = response.json()
    db.add_password(data["password"])
    return data

def random_app_name(size = 3):
    base_url = 'https://random-data-api.com/api/app/random_app'
    response = requests.get(base_url, params={"size": size})
    data = response.json()
    return data


TOKEN = str(os.environ.get('TOKEN'))
bot = telebot.TeleBot(TOKEN)
print("\033[44mSTART BOT\033[0m")

@bot.message_handler(commands=['start'])
def start_command(message: Message):
    message_id = message.chat.id
    bot.send_message(message_id, "Приветствуем вас в нашем боте.")


@bot.message_handler(commands=['fake_male', 'fakeMale'])
def fake_male(message: Message):
    data = fake_person_male()
    message_id = message.chat.id
    text = f"Имя: {data["FirstName"]}\nФамилия: {data["LastName"]}\nemail: {data["Email"]}\n"
    text = text + f"Телефон: {data["Phone"]}\nДень рождения: {data["DateOfBirth"]}"
    bot.send_message(message_id, text)


@bot.message_handler(commands=['fake_female', 'fakeFemale'])
def fake_female(message: Message):
    data = fake_person_female()
    message_id = message.chat.id
    text = f"Имя: {data["FirstName"]}\nФамилия: {data["LastName"]}\nemail: {data["Email"]}\n"
    text = text + f"Телефон: {data["Phone"]}\nДень рождения: {data["DateOfBirth"]}"
    bot.send_message(message_id, text)
    

@bot.message_handler(commands=['generate_password', 'password', 'gen_pas'])
def generate_password(message: Message):
    data = random_password()
    message_id = message.chat.id
    bot.send_message(message_id, f"Пароль: {data["password"]}")


@bot.message_handler(commands=['app_name'])
def app_name(message: Message):
    message_id = message.chat.id
    data = random_app_name()
    text = f"Название приложения:\n1 - {data[0]["app_name"]}\n2 - {data[1]["app_name"]}\n3 - {data[2]["app_name"]}"
    bot.send_message(message_id, text)


@bot.message_handler(commands=['random', 'random_num'])
def random_number(message: Message):
    message_id = message.chat.id
    bot.send_message(message_id, "Случаеное число от 1 до X")
    bot.send_message(message_id, "Введите X")
    bot.register_next_step_handler(message, random_number_2)

def random_number_2(message: Message):
    try:
        x = message.text
        bot.send_message(message.chat.id, f"Выпало число: {random.randint(1, int(x))}")
    except:
        bot.send_message(message.chat.id, "X должен быть числом")

bot.infinity_polling(skip_pending=True)