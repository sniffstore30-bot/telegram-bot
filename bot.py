import telebot
import os
import google.generativeai as genai
import time
import threading

# ===== TOKEN =====
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = "AIzaSyCiQbgCZqskSKJOUs5p1tTMBegtK9npVDc"

# Init bot dengan setting timeout yang betul
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Setup Gemini
genai.configure(api_key=GEMINI_KEY)

# Configuration untuk kreativiti tinggi
generation_config = {
    "temperature": 1.5,
    "top_p": 0.99,
    "top_k": 50,
    "max_output_tokens": 200,
}

model = genai.GenerativeModel(
    'gemini-pro',
    generation_config=generation_config
)

# Simpan chat history
chat_sessions = {}

# ===== FUNGSI AI CHAT =====
def ai_chat(user_message, user_name, user_id):
    try:
        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])
        
        response = chat_sessions[user_id].send_message(user_message)
        return response.text
        
    except Exception as e:
        print(f"AI Error: {e}")
        try:
            response = model.generate_content(user_message)
            return response.text
        except:
            return "Ha ah..."

# ===== WELCOME =====
@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for member in message.new_chat_members:
        if member.id == bot.get_me().id:
            continue
        bot.send_message(message.chat.id, f"Welcome {member.first_name}!")

# ===== GOODBYE =====
@bot.message_handler(content_types=['left_chat_member'])
def goodbye(message):
    left = message.left_chat_member
    if left.id == bot.get_me().id:
        return
    bot.send_message(message.chat.id, f"Bye {left.first_name}!")

# ===== SEMUA MESEJ =====
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text.startswith('/'):
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    
    response = ai_chat(message.text, message.from_user.first_name, message.from_user.id)
    bot.reply_to(message, response)

# ===== COMMANDS =====
@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, "Hai. Saya AI. Sembang je.")

@bot.message_handler(commands=['reset'])
def reset(message):
    user_id = message.from_user.id
    if user_id in chat_sessions:
        del chat_sessions[user_id]
    bot.reply_to(message, "OK. Reset.")

# ===== MAIN DENGAN HANDLER YANG BETUL =====
if __name__ == "__main__":
    print("🤖 BOT AI - READY")
    
    # Remove webhook dulu
    try:
        bot.remove_webhook()
        time.sleep(1)
    except:
        pass
    
    # Start bot dengan setting yang sesuai untuk Railway
    print("Connecting to Telegram...")
    
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as e:
            print(f"Error: {e}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)
