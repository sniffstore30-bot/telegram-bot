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

# ===== SYSTEM PROMPT UNTUK GAYA BAHASA MELAYU SLANG =====
MALAY_SLANG_SYSTEM_PROMPT = """Kamu adalah bot AI yang sangat gaul dan casual, macam teman2 di group chat. 
Respond dalam gaya bahasa Melayu yang santai dengan banyak slang seperti:
- "lah", "lor", "leh", "meh" di akhir ayat
- Gunakan "bro", "saudara", "kawan", "budak" dalam percakapan
- Mix Malay-English (Rojak) macam orang Malaysia/Singapore biasa cakap
- Gunakan emoji dan sarkasm
- Keep it short dan natural, bukan formal atau template
- Jangan respond panjang2, 1-2 line je ok
- Jangan sebut "sebagai AI" atau "saya AI"
- Reply macam teman baik kamu saja

Contoh style:
- "ish kena gilak lah" 
- "haha gila betul bro"
- "saya pun rasa la"
- "wey tu lagi" 
- "alamak bro haha"

Respond casual, fun, dan natural je."""

# Configuration untuk kreativiti tinggi
generation_config = {
    "temperature": 1.3,
    "top_p": 0.95,
    "top_k": 50,
    "max_output_tokens": 150,
}

model = genai.GenerativeModel(
    'gemini-pro',
    generation_config=generation_config,
    system_instruction=MALAY_SLANG_SYSTEM_PROMPT
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
            return "Alamak bro, error la haha 😅"

# ===== WELCOME =====
@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for member in message.new_chat_members:
        if member.id == bot.get_me().id:
            continue
        bot.send_message(message.chat.id, f"Yo {member.first_name}! Welcome to the gang bro! 🎉")

# ===== GOODBYE =====
@bot.message_handler(content_types=['left_chat_member'])
def goodbye(message):
    left = message.left_chat_member
    if left.id == bot.get_me().id:
        return
    bot.send_message(message.chat.id, f"Dah la {left.first_name}, jangan lupa kami la 😢")

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
    bot.reply_to(message, "Yo wey! I'm here to sembang la. Just type anything bro 😎")

@bot.message_handler(commands=['reset'])
def reset(message):
    user_id = message.from_user.id
    if user_id in chat_sessions:
        del chat_sessions[user_id]
    bot.reply_to(message, "Reset la bro! Fresh start hehe 🔄")

# ===== MAIN DENGAN HANDLER YANG BETUL =====
if __name__ == "__main__":
    print("🤖 BOT AI - READY & GAUL!")
    
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