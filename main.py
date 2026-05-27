import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from flask import Flask
from threading import Thread

# თქვენი Telegram ბოტის ტოკენი
TOKEN = "8869842105:AAFtoMm9E0wB2To3PfQfCR8t4eVd0WvJnEo"
bot = telebot.TeleBot(TOKEN)

# 2D გრაფიკული თამაშის ბმული
GAME_URL = "https://github.io"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # ვქმნით სპეციალურ WebApp ღილაკს გრაფიკული თამაშის გასახსნელად
    markup = InlineKeyboardMarkup()
    web_app = WebAppInfo(url=GAME_URL)
    game_button = InlineKeyboardButton(text="🎮 ითამაშე თამაში", web_app=web_app)
    markup.add(game_button)
    
    # მისალმების ტექსტი მოთამაშისთვის
    welcome_text = (
        f"გამარჯობა, {message.from_user.first_name}! 👋\n\n"
        "2D გრაფიკული თამაშის დასაწყებად დააჭირე ქვედა ლურჯ ღილაკს👇"
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "თამაშის დასაწყებად გთხოვთ გამოიყენოთ ბრძანება /start")

# Flask ვებ-სერვერი, რომელიც სჭირდება Render-ს მუდმივი მუშაობისთვის
app = Flask('')

@app.route('/')
def home():
    return "ბოტი წარმატებით მუშაობს სერვერზე!"

def run():
    # Render ავტომატურად იყენებს პორტს 8080
    app.run(host='0.0.0.0', port=8080)

# ბოტის გაშვება ფონურ რეჟიმში (ცალკე ნაკადში)
def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":

    keep_alive()
    bot.infinity_polling()
