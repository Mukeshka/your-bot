from telethon import TelegramClient, events
import json

# 🔹 Replace with your actual credentials
API_ID = "25057606" 
API_HASH = "bb37f3b7d70879d8e650f20d2beb09f6"  
BOT_TOKEN = "7668887729:AAFn_5E6V24iIEpqlqTjlH7UZqT0_n36tP4"

# 🔹 Initialize Telegram Bot
bot = TelegramClient("join_channel_bot", API_ID, API_HASH)

# 🔹 Start Command (Send Message Every Time)
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    message = """
🎯 **Join Our Fantasy Cricket Community!** 🏏  

🔥 **Mega GL Predictions & Expert Teams**  
🔗 **Join Telegram:** [Kevin Fantasy Teams](https://t.me/kevinfantasyteams)  
📺 **Subscribe on YouTube:** [Kevin Fantasy Teams](https://www.youtube.com/@Kevinfantasyteams)  

🚀 Get daily match predictions, best fantasy teams booking ke liye massage kare @KevinfantasyteamKft , and expert analysis! Don't miss out!  
    """
    await event.reply(message, link_preview=True)

# 🔹 Your Telegram username (where messages will be forwarded)
YOUR_USERNAME = "@KevinfantasyteamKft"

# 🔹 Initialize Telegram Bot
bot = TelegramClient("forward_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 🔹 Forward all messages to your username
@bot.on(events.NewMessage)
async def forward_message(event):
    try:
        # Forward the message to your username
        await event.forward_to(YOUR_USERNAME)
        print(f"Message forwarded to {YOUR_USERNAME}")
    except Exception as e:
        print(f"Error forwarding message: {e}")
# 🔹 Run the bot
async def main():
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot is running...")
    await bot.run_until_disconnected()

# 🔹 Run the bot
print("Bot is running...")
bot.run_until_disconnected()
