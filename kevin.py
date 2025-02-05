from telethon import TelegramClient, events

# 🔹 Replace with your actual credentials
API_ID = "25057606" 
API_HASH = "bb37f3b7d70879d8e650f20d2beb09f6"  
BOT_TOKEN = "7545239035:AAGsFcyO_CUcaWfjGEQSxOI5oipNmDGx6g4"

# 🔹 Initialize Telegram Bot
bot = TelegramClient("join_channel_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 🔹 Start Command
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    message = """
🎯 **Join Our Fantasy Cricket Community!** 🏏  

🔥 **Mega GL Predictions & Expert Teams**  
🔗 **Join Telegram:** [Kevin Fantasy Teams](https://t.me/kevinfantasyteams)  
📺 **Subscribe on YouTube:** [Kevin Fantasy Teams](https://www.youtube.com/@Kevinfantasyteams)  

🚀 Get daily match predictions, best fantasy teams booikng ke liye massage kare : 
@KevinfantasyteamKft , and expert analysis! Don't miss out!  
    """
    await event.reply(message, link_preview=True)

# 🔹 Run the bot
print("Bot is running...")
bot.run_until_disconnected()

