from telethon import TelegramClient, events
import requests
from bs4 import BeautifulSoup
import time

# ✅ TELEGRAM API CREDENTIALS
api_id = "25057606"  # My.telegram.org se lo
api_hash = "bb37f3b7d70879d8e650f20d2beb09f6"  # My.telegram.org se lo
bot_token = "7545239035:AAF1BjXGjU43B8hcQbQ0KIucmpCN-DimziM"  # BotFather se lo

# ✅ TELEGRAM CLIENT SETUP
client = TelegramClient('aviator_bot', api_id, api_hash).start(bot_token=bot_token)

# ✅ 1Win Aviator Game URL
aviator_url = "https://1wyfui.life/casino/play/aviator?p=ftgc"

# ✅ Game History Data
previous_results = []

# ✅ Scraping Function
def get_aviator_results():
    try:
        response = requests.get(aviator_url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 📌 FIND RESULT VALUES (Modify selector based on actual site structure)
        crash_values = [float(div.text.replace("x", "")) for div in soup.find_all("div", class_="crash-result-class")]  # 👈 Update the class name!
        
        return crash_values[:5]  # Last 5 results return karega
    except Exception as e:
        print(f"Scraping Error: {e}")
        return []

# ✅ Pattern Detection Function
def detect_pattern(results):
    if len(results) < 3:
        return None  # Kam data hone par prediction na kare

    last_3 = results[:3]  # Latest 3 values
    pattern = None
    prediction = None

    # ✅ Pattern 1: (1 time 2x ke neeche, phir 2x ke upar)
    if last_3[1] < 2.0 and last_3[2] > 2.0:
        pattern = "Pattern 1"
        prediction = 2.0  # Next prediction

    # ✅ Pattern 2: (2 baar 2x se neeche crash)
    elif last_3[0] < 2.0 and last_3[1] < 2.0:
        pattern = "Pattern 2"
        prediction = 2.0  # Next prediction

    return pattern, prediction

# ✅ Telegram Message Sending Function
async def send_prediction(pattern, prediction):
    message = f"📢 **Aviator Signal Alert!** 🚀\n\n"
    message += f"🎯 **Pattern Detected:** {pattern}\n"
    message += f"🎲 **Next Prediction:** {prediction}x\n"
    message += f"💡 **Auto Cashout:** {prediction}.00x\n\n"
    message += f"🔗 [Play Now on 1Win]({aviator_url})"
    
    await client.send_message("@your_channel_username", message, link_preview=False)

# ✅ Main Bot Loop
async def main_loop():
    global previous_results
    while True:
        new_results = get_aviator_results()

        if new_results and new_results != previous_results:
            previous_results = new_results
            pattern, prediction = detect_pattern(new_results)

            if pattern and prediction:
                await send_prediction(pattern, prediction)

        time.sleep(10)  # ⏳ 10 sec delay

# ✅ Start the bot
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("👋 Welcome to **Aviator Prediction Bot**!\n\n🔔 This bot sends **Aviator game signals** based on patterns.\n\n⏳ Please wait for the next signal!")

print("✅ Bot is running...")
client.loop.run_until_complete(main_loop())
client.run_until_disconnected()
