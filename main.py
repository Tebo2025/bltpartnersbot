import telebot
from flask import Flask, request
import os
from telebot import types

API_TOKEN = 'YOUR_BOT_TOKEN'  # buraya öz tokenini yaz
ACCESS_PASSWORD = 'b2baccess2025'  # dəyişmək istəyirsənsə, buradan dəyiş

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Saxlanmış istifadəçilər (giriş etmiş B2B agentlər)
authorized_users = set()

# /start komandası ilə giriş istənir
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🔒 Welcome to Baku Life Partners Bot.\n\nPlease enter your access password to continue:")

# İstifadəçi şifrə daxil edir
@bot.message_handler(func=lambda m: m.text and m.text.startswith('/start') == False)
def handle_password_or_commands(message):
    user_id = message.chat.id

    if user_id not in authorized_users:
        if message.text.strip() == ACCESS_PASSWORD:
            authorized_users.add(user_id)
            show_main_menu(user_id)
        else:
            bot.send_message(user_id, "❌ Incorrect password. Try again.")
    else:
        # Authorized user: show menu
        show_main_menu(user_id)

# Ana menyunu göstərir
def show_main_menu(user_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    reg_btn = types.InlineKeyboardButton("🧾 Register Your Company", url="https://docs.google.com/forms/d/e/1FAIpQLSeOzobznkaYjU2TbQzeuX2uLmID_NBydRpS_rBSL-R8UdMvjw/viewform")
    markup.add(reg_btn)

    bot.send_message(user_id, """
✅ Access Granted!

Welcome to the Baku Life Partners Panel.  
Use the options below to register your agency and begin using B2B features.
    """, reply_markup=markup)

# Webhook bağlantıları
@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running.', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    bot.remove_webhook()
    bot.set_webhook(url=f"https://YOUR_RENDER_URL.onrender.com/{API_TOKEN}")
    app.run(host="0.0.0.0", port=port)
