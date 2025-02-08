import asyncio
from telethon import TelegramClient, events

# 🔹 अपने टेलीग्राम क्रेडेंशियल्स डालें
API_ID = "25057606"
API_HASH = "bb37f3b7d70879d8e650f20d2beb09f6"
BOT_TOKEN = "7668887729:AAFn_5E6V24iIEpqlqTjlH7UZqT0_n36tP4"

# 🔹 बॉट को इनिशियलाइज़ करें
bot = TelegramClient("reply_forward_bot", API_ID, API_HASH)

async def main():
    await bot.start(bot_token=BOT_TOKEN)  # बॉट को स्टार्ट करें
    print("Bot is running 24/7...")
    await bot.run_until_disconnected()

# 🔹 टेलीग्राम यूज़रनेम जहाँ मैसेज फॉरवर्ड होंगे (आपका अकाउंट)
ADMIN_USERNAME = "@KevinfantasyteamKft"
user_messages = {}

@bot.on(events.NewMessage)
async def handle_message(event):
    if event.is_channel:
        return
    
    sender = await event.get_sender()
    user_id = sender.id
    
    if user_id != ADMIN_USERNAME:
        user_messages[user_id] = event
        await event.forward_to(ADMIN_USERNAME)
        print(f"Message received from {user_id} and forwarded to {ADMIN_USERNAME}")

@bot.on(events.NewMessage(from_users=ADMIN_USERNAME))
async def reply_to_user(event):
    if event.reply_to and event.reply_to.reply_markup is None:
        original_msg = await event.get_reply_message()
        sender_id = None

        for user_id, user_msg in user_messages.items():
            if user_msg.id == original_msg.id:
                sender_id = user_id
                break

        if sender_id:
            await bot.send_message(sender_id, event.text)
            print(f"Replied to {sender_id}: {event.text}")

# 🔹 बॉट शुरू करें
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
