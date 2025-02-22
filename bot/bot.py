import telebot
import psycopg2
import logging
from config import TOKEN, DB_URL

bot = telebot.TeleBot(TOKEN)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def connect_db():
    return psycopg2.connect(DB_URL)

# Команды /start и /map
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Отправь геопозицию, чтобы добавить точку.")

@bot.message_handler(commands=['map'])
def send_map(message):
    bot.send_message(message.chat.id, "🌍 Открыть карту: https://ТВОЙ_САЙТ.com")

# Обработка геопозиции
@bot.message_handler(content_types=['location'])
def location_handler(message):
    user_id = message.chat.id
    latitude = message.location.latitude
    longitude = message.location.longitude

    msg = bot.send_message(user_id, "Какая рыба здесь водится?")
    bot.register_next_step_handler(msg, lambda m: ask_bait(m, user_id, latitude, longitude))

def ask_bait(message, user_id, latitude, longitude):
    fish_type = message.text
    msg = bot.send_message(user_id, "На что клюёт?")
    bot.register_next_step_handler(msg, lambda m: save_spot(m, user_id, latitude, longitude, fish_type))

def save_spot(message, user_id, latitude, longitude, fish_type):
    bait = message.text
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO fishing_spots (user_id, latitude, longitude, fish_type, bait) VALUES (%s, %s, %s, %s, %s)",
        (user_id, latitude, longitude, fish_type, bait)
    )
    conn.commit()
    conn.close()
    bot.send_message(user_id, "Точка добавлена!")

bot.polling()
