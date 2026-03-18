import telebot
import os
import google.generativeai as genai
import time
from datetime import datetime

# ===== TOKEN =====
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = "AIzaSyCiQbgCZqskSKJOUs5p1tTMBegtK9npVDc"

# Init bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Setup Gemini
genai.configure(api_key=GEMINI_KEY)

# Configuration untuk kreativiti tinggi
generation_config = {
    "temperature": 1.5,        # Tinggi supaya kreatif dan tak sama
    "top_p": 0.99,
    "top_k": 50,
    "max_output_tokens": 200,
}

model = genai.GenerativeModel(
    'gemini-pro',
    generation_config=generation_config
)

# Simpan history sembang untuk setiap user (biar AI ingat context)
chat_sessions = {}

# ===== FUNGSI AI CHAT (TANPA SKRIP) =====
def ai_chat(user_message, user_name, user_id):
    """AI akan reply berdasarkan perbualan sebenar"""
    try:
        # Start chat session baru kalau takde
        if user_id not in chat_sessions:
            chat_sessions[user_id] = model.start_chat(history=[])
        
        # Hantar message terus ke AI - TANPA SKRIP
        response = chat_sessions[user_id].send_message(user_message)
        return response.text
        
    except Exception as e:
        print(f"AI Error: {e}")
        # Kalau error, cuba sekali lagi tanpa session
        try:
            response = model.generate_content(user_message)
            return response.text
        except:
            return "..."

# ===== WELCOME =====
@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for member in message.new_chat_members:
        if member.id == bot.get_me().id:
            continue
        
        # Guna AI untuk tulis welcome message
        welcome_prompt = f"Tulis ucapan selamat datang pendek untuk {member.first_name} yang baru join group. Guna bahasa santai Malaysia."
        welcome_text = model.generate_content(welcome_prompt).text
        bot.send_message(message.chat.id, welcome_text)

# ===== GOODBYE =====
@bot.message_handler(content_types=['left_chat_member'])
def goodbye(message):
    left = message.left_chat_member
    if left.id == bot.get_me().id:
        return
    
    goodbye_prompt = f"Tulis ucapan selamat tinggal pendek untuk {left.first_name} yang keluar dari group. Guna bahasa santai."
    goodbye_text = model.generate_content(goodbye_prompt).text
    bot.send_message(message.chat.id, goodbye_text)

# ===== SEMUA MESEJ =====
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text.startswith('/'):
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Dapat response dari AI (tanpa skrip)
    response = ai_chat(message.text, message.from_user.first_name, message.from_user.id)
    
    # Hantar balik
    bot.reply_to(message, response)

# ===== COMMANDS =====
@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, "Hai. Saya AI. Sembang je apa-apa.")

@bot.message_handler(commands=['reset'])
def reset(message):
    """Reset chat history untuk user"""
    user_id = message.from_user.id
    if user_id in chat_sessions:
        del chat_sessions[user_id]
    bot.reply_to(message, "OK. Saya dah lupa sembang lepas.")

# ===== MAIN =====
if __name__ == "__main__":
    print("🤖 BOT AI - TANPA SKRIP")
    print("Mode: AI fikir sendiri")
    
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling()
