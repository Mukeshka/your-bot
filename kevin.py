
from telethon import TelegramClient, events
import requests
from bs4 import BeautifulSoup
import openai

# ✅ Replace with your actual credentials
API_ID = "25057606"
API_HASH = "bb37f3b7d70879d8e650f20d2beb09f6"
BOT_TOKEN = "7668887729:AAFn_5E6V24iIEpqlqTjlH7UZqT0_n36tP4"
OPENAI_API_KEY = "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"  # ⚠️ Replace with your OpenAI API Key

# ✅ Initialize Telegram Bot
bot = TelegramClient('cricket_ai_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
teams = {}

# ✅ Fetch Player Stats from Crex.live
def fetch_player_stats(player_name):
    try:
        url = f"https://www.crex.live/search?q={player_name.replace(' ', '%20')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Example: Find first player's link
        player_link = soup.find("a", class_="player-link")
        if player_link:
            player_url = "https://www.crex.live" + player_link["href"]
            player_response = requests.get(player_url, headers=headers)
            player_soup = BeautifulSoup(player_response.text, "html.parser")

            # Extract recent match stats
            stats = player_soup.find_all("span", class_="stat")
            if stats:
                return f"🔹 {player_name} Stats: {stats[0].text} Runs, {stats[1].text} Wickets"
            else:
                return f"⚠ No stats found for {player_name}."
        else:
            return f"⚠ Player {player_name} not found on Crex.live."
    except Exception as e:
        return f"❌ Error fetching data: {str(e)}"

# ✅ AI-Based Player Analysis using OpenAI
def ai_analyze_team(players):
    try:
        openai.api_key = OPENAI_API_KEY
        prompt = f"Select best 18 and best 11 players for mega GL team based on recent performance:\n\n{players}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠ AI Analysis Error: {str(e)}"

# ✅ Start Command
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("👋 Welcome! Enter teams using:\n\n`/teams Team1 vs Team2`")

# ✅ Handle Team Names Input
@bot.on(events.NewMessage(pattern=r"/teams (.+) vs (.+)"))
async def set_teams(event):
    team1, team2 = event.pattern_match.group(1), event.pattern_match.group(2)
    teams["team1"] = team1
    teams["team2"] = team2
    teams["players"] = []
    await event.respond(f"✅ Teams set: **{team1}** vs **{team2}**\n\nNow enter Playing XI:\n`/playingxi Player1, Player2, ...`")

# ✅ Handle Playing XI Input
@bot.on(events.NewMessage(pattern=r"/playingxi (.+)"))
async def set_playing_xi(event):
    players = event.pattern_match.group(1).split(", ")
    teams["players"] = players

    # Fetch stats for each player
    analysis = []
    for player in players:
        stats = fetch_player_stats(player)
        analysis.append(stats)
    
    result = "\n".join(analysis)
    await event.respond(f"📊 **Player Stats & Analysis:**\n\n{result}\n\n📢 Use `/bestteam` for AI-based best team.")

# ✅ Handle AI-Based Best 18 & Best 11 Selection
@bot.on(events.NewMessage(pattern="/bestteam"))
async def best_team(event):
    if "players" not in teams or not teams["players"]:
        await event.respond("❌ Please enter Playing XI first using `/playingxi`")
        return

    # AI Analysis
    ai_result = ai_analyze_team(teams["players"])
    await event.respond(f"🤖 **AI-Based Best Team Analysis:**\n\n{ai_result}")

# ✅ Run the bot
print("✅ Bot is running...")
bot.run_until_disconnected()
