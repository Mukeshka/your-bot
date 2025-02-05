import asyncio
from telethon import TelegramClient, events
import requests
from bs4 import BeautifulSoup


# 🔹 Replace with your actual credentials
API_ID = "25057606"
API_HASH = "bb37f3b7d70879d8e650f20d2beb09f6"
BOT_TOKEN = "7668887729:AAFn_5E6V24iIEpqlqTjlH7UZqT0_n36tP4"

client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ✅ प्लेयर डेटा स्क्रैपिंग फ़ंक्शन (Crex.live से)
def scrape_player_data(player_name):
    search_url = f"https://crex.live/search?query={player_name.replace(' ', '%20')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    player_stats = {}  # डेटा स्टोर करने के लिए

    # 🔹 स्क्रैपिंग लॉजिक (क्रेक्स वेबसाइट के स्ट्रक्चर पर डिपेंड करता है)
    try:
        player_stats["name"] = player_name
        player_stats["matches"] = soup.find("td", text="Mat").find_next_sibling("td").text
        player_stats["runs"] = soup.find("td", text="R").find_next_sibling("td").text
        player_stats["wickets"] = soup.find("td", text="W").find_next_sibling("td").text
        player_stats["average"] = soup.find("td", text="Avg").find_next_sibling("td").text
    except AttributeError:
        return None  # अगर प्लेयर डेटा न मिले

    return player_stats

# ✅ AI-Based प्लेयर एनालिसिस (Simple Scoring System)
def analyze_players(players):
    player_scores = {}

    for player in players:
        data = scrape_player_data(player)
        if data:
            # 🔹 स्कोरिंग सिस्टम (रन्स + विकेट्स + एवरेज के आधार पर)
            score = int(data["runs"]) * 0.5 + int(data["wickets"]) * 10 + float(data["average"]) * 1.5
            player_scores[player] = score

    # 🔹 टॉप 18 और टॉप 11 प्लेयर्स निकालना
    sorted_players = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
    best_18 = [p[0] for p in sorted_players[:18]]
    best_11 = [p[0] for p in sorted_players[:11]]

    return best_18, best_11

# ✅ /start कमांड (यूज़र से इनपुट लेने के लिए)
@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond("👋 Welcome! कृपया दो टीमों के नाम और उनके प्लेयर्स भेजें।\n\n✍ *Format:* \n`Team1: Player1, Player2, Player3...`\n`Team2: Player1, Player2, Player3...`")
    await asyncio.sleep(2)

# ✅ प्लेयर डेटा प्रोसेसिंग
@client.on(events.NewMessage)
async def process_teams(event):
    msg = event.message.text
    if "Team1:" in msg and "Team2:" in msg:
        try:
            teams = msg.split("\n")
            team1_players = teams[0].split(":")[1].strip().split(", ")
            team2_players = teams[1].split(":")[1].strip().split(", ")

            all_players = team1_players + team2_players
            await event.respond("🔍 प्लेयर डेटा प्रोसेस किया जा रहा है... कृपया प्रतीक्षा करें।")
            
            best_18, best_11 = analyze_players(all_players)

            # ✅ परिणाम भेजें
            await event.respond(f"🏏 **Best 18 Players:**\n{', '.join(best_18)}")
            await event.respond(f"🔥 **Mega GL Best 11 Players:**\n{', '.join(best_11)}")
        except Exception as e:
            await event.respond("❌ Error: कृपया सही फॉर्मेट में जानकारी दें।")

# ✅ बॉट को रन करें
print("🤖 Bot is running...")
client.run_until_disconnected()
