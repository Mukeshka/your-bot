from telethon import TelegramClient, events
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Bot credentials (Replace with your actual credentials)
API_ID = "25057606"
API_HASH = "bb37f3b7d70879d8e650f20d2beb09f6"
BOT_TOKEN = "7668887729:AAFn_5E6V24iIEpqlqTjlH7UZqT0_n36tP4"

# Create bot client
bot = TelegramClient('cricket_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Store team and player details
teams = {}

# Function to fetch player stats from a cricket website
def fetch_player_stats(player_name):
    try:
        url = f"https://www.espncricinfo.com/search/results?q={player_name}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Example: Fetch first player's link
        player_link = soup.find("a", class_="result-link")
        if player_link:
            player_url = "https://www.espncricinfo.com" + player_link["href"]
            player_response = requests.get(player_url, headers=headers)
            player_soup = BeautifulSoup(player_response.text, "html.parser")

            # Extracting stats
            stats = player_soup.find_all("span", class_="stat")
            if stats:
                return f"🔹 {player_name} Stats: {stats[0].text} Runs, {stats[1].text} Wickets"
            else:
                return f"⚠ No stats found for {player_name}."
        else:
            return f"⚠ Player {player_name} not found on ESPN Cricinfo."
    
    except Exception as e:
        return f"❌ Error fetching data: {str(e)}"

# Start command
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond("👋 Welcome! Please enter Team 1 and Team 2 names in this format:\n\n`/teams Team1 vs Team2`")

# Handle team input
@bot.on(events.NewMessage(pattern="/teams (.+) vs (.+)"))
async def set_teams(event):
    team1, team2 = event.pattern_match.group(1), event.pattern_match.group(2)
    teams["team1"] = team1
    teams["team2"] = team2
    teams["players"] = []
    
    await event.respond(f"✅ Teams set: **{team1}** vs **{team2}**\n\nNow enter Playing XI using:\n`/playingxi Player1, Player2, ...`")

# Handle Playing XI input
@bot.on(events.NewMessage(pattern="/playingxi (.+)"))
async def set_playing_xi(event):
    players = event.pattern_match.group(1).split(", ")
    teams["players"] = players

    await event.respond("✅ Playing XI added!\nFetching stats and predictions...")

    # Fetch stats for each player
    analysis = []
    for player in players:
        stats = fetch_player_stats(player)
        analysis.append(stats)
    
    result = "\n".join(analysis)
    await event.respond(f"📊 **Player Stats & Analysis:**\n\n{result}\n\n📢 Use `/bestteam` to get Best 18 & Best 11.")

# Handle Best 18 & Best 11 selection
@bot.on(events.NewMessage(pattern="/bestteam"))
async def best_team(event):
    if "players" not in teams or not teams["players"]:
        await event.respond("❌ Please enter Playing XI first using `/playingxi`")
        return

    # Simple logic: Pick top 18 & top 11 players randomly (Can be improved with AI-based selection)
    best_18 = teams["players"][:18]
    best_11 = teams["players"][:11]

    response = f"🏏 **Best 18 Players:**\n" + ", ".join(best_18) + "\n\n"
    response += f"🔥 **Best 11 Players:**\n" + ", ".join(best_11)

    await event.respond(response)

# Run the bot
bot.run_until_disconnected()
