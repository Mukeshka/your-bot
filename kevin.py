from telethon import TelegramClient, events
import json

# 🔹 Replace with your actual credentials
API_ID = "25057606" 
API_HASH = "bb37f3b7d70879d8e650f20d2beb09f6"  
BOT_TOKEN = "7545239035:AAGsFcyO_CUcaWfjGEQSxOI5oipNmDGx6g4"

# 🔹 Initialize Telegram Bot
bot = TelegramClient("join_channel_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 🔹 Store users who have received the message
USER_DATA_FILE = "users.json"

# 🔹 Load user data
try:
    with open(USER_DATA_FILE, "r") as f:
        sent_users = json.load(f)
except FileNotFoundError:
    sent_users = {}

# 🔹 Start Command (Send Message Only Once)
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    user_id = str(event.sender_id)  # Convert to string for JSON storage
    
    if user_id not in sent_users:
        message = """
🎯 **Join Our Fantasy Cricket Community!** 🏏  

🔥 **Mega GL Predictions & Expert Teams**  
🔗 **Join Telegram:** [Kevin Fantasy Teams](https://t.me/kevinfantasyteams)  
📺 **Subscribe on YouTube:** [Kevin Fantasy Teams](https://www.youtube.com/@Kevinfantasyteams)  

🚀 Get daily match predictions,best fantasy teams booikng ke liye massage kare : 
@KevinfantasyteamKft, and expert analysis! Don't miss out!  
        """
        await event.reply(message, link_preview=True)
        
        # Save the user as "sent"
        sent_users[user_id] = True
        with open(USER_DATA_FILE, "w") as f:
            json.dump(sent_users, f)
    else:
        await event.reply("✅ You have already received the message. Stay tuned for updates!")

# 🔹 Run the bot
print("Bot is running...")
bot.run_until_disconnected()
