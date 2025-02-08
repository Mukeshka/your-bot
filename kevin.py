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
ADMIN_ID = 123456789  # 👈 अपना Telegram ID डालें (Replace with your Telegram ID)
user_messages = {}

# 🔹 जब कोई यूज़र मैसेज करे, तो उसे सेव करें और एडमिन को फॉरवर्ड करें
@bot.on(events.NewMessage)
async def handle_message(event):
    if event.is_channel:  # चैनल से आने वाले मैसेज को ब्लॉक करें
        return
    
    sender = await event.get_sender()
    user_id = sender.id

    if user_id != ADMIN_ID:  # अगर मैसेज एडमिन से नहीं आया है
        user_messages[event.id] = user_id  # यूज़र का मैसेज सेव करें
        await event.forward_to(ADMIN_ID)  # एडमिन को फॉरवर्ड करें
        print(f"Message received from {user_id} and forwarded to Admin.")

# 🔹 जब ADMIN किसी मैसेज का रिप्लाई करे, तो वही रिप्लाई उसी यूज़र को भेजें
@bot.on(events.NewMessage(from_users=ADMIN_ID))
async def reply_to_user(event):
    if event.reply_to:  # अगर एडमिन ने किसी मैसेज को रिप्लाई किया है
        original_msg = await event.get_reply_message()
        
        if original_msg.id in user_messages:  # अगर मैसेज यूज़र का था
            sender_id = user_messages[original_msg.id]  # उस यूज़र का ID निकालें
            
            await bot.send_message(sender_id, event.text)  # रिप्लाई भेजें
            print(f"Replied to {sender_id}: {event.text}")

# 🔹 बॉट शुरू करें
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
