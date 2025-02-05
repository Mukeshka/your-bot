from telethon import TelegramClient, events
import requests
from bs4 import BeautifulSoup
import sys  # For stopping the bot
import random  # For selecting best players


# 🔹 Replace with your actual credentials
API_ID = "25057606"
API_HASH = "bb37f3b7d70879d8e650f20d2beb09f6"
BOT_TOKEN = "7668887729:AAFn_5E6V24iIEpqlqTjlH7UZqT0_n36tP4"

# 🔹 Initialize Telegram Bot
bot = TelegramClient("fantasy_cricket_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 🔹 Store user data
user_state = {}

# 🔹 Start Command
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    user_state[event.sender_id] = {"step": 1}  # Start user flow
    await event.reply("🏏 **Welcome to Fantasy Cricket Bot!**\n\nEnter **Team 1 Name**:")

# 🔹 Handle User Input
@bot.on(events.NewMessage)
async def handle_input(event):
    user_id = event.sender_id
    if user_id not in user_state:
        return  # Ignore if user hasn't started the bot

    state = user_state[user_id]

    if state["step"] == 1:  # Team 1 Name
        state["team1"] = event.text.strip()
        state["step"] = 2
        await event.reply("✅ Team 1 saved! Now enter **Team 2 Name**:")

    elif state["step"] == 2:  # Team 2 Name
        state["team2"] = event.text.strip()
        state["step"] = 3
        await event.reply(f"✅ {state['team2']} saved! Now enter **Team 1 Players** (comma-separated):")

    elif state["step"] == 3:  # Team 1 Players
        state["team1_players"] = [player.strip() for player in event.text.split(",")]
        state["step"] = 4
        await event.reply(f"✅ Players for {state['team1']} saved! Now enter **Team 2 Players** (comma-separated):")

    elif state["step"] == 4:  # Team 2 Players
        state["team2_players"] = [player.strip() for player in event.text.split(",")]
        state["step"] = 5
        await event.reply("✅ Players saved! Fetching stats and building best teams...")

        # Fetch stats and generate teams
        all_players = state["team1_players"] + state["team2_players"]
        best_18, best_11, captain, vice_captain = await fetch_and_analyze_players(event, all_players)

        # Display final teams
        response_text = "**🏏 Best 18 Players:**\n" + "\n".join([f"🔹 {p}" for p in best_18])
        response_text += "\n\n**🏆 Mega GL Team (Best 11 Players):**\n" + "\n".join([f"⭐ {p}" for p in best_11])
        response_text += f"\n\n**👑 Captain:** {captain}\n**🛡 Vice-Captain:** {vice_captain}"

        await event.reply(response_text, link_preview=False)

        del user_state[user_id]  # Reset user state

# 🔹 Fetch & Analyze Player Stats
async def fetch_and_analyze_players(event, players):
    player_stats = []

    for player in players:
        formatted_name = player.replace(" ", "-").lower()
        url = f"https://crex.live/player-profile/{formatted_name}"
        stats = fetch_stats_from_crex(url)
        if stats:
            player_stats.append((player, stats))

    # Sort by Batting Avg, SR, Bowling Wickets, Econ
    sorted_players = sorted(player_stats, key=lambda x: (x[1]['bat_avg'], x[1]['bat_sr'], x[1]['bowl_wickets'], -x[1]['bowl_econ']), reverse=True)

    best_18 = [p[0] for p in sorted_players[:18]]  # Top 18 Players
    best_11 = best_18[:11]  # Best 11 for Mega GL
    captain = random.choice(best_11[:5])  # Choose a Captain from top 5 players
    vice_captain = random.choice([p for p in best_11 if p != captain])  # Choose VC from remaining

    return best_18, best_11, captain, vice_captain

# 🔹 Scrape Player Stats from Crex
def fetch_stats_from_crex(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        batting_section = soup.find("div", class_="player-career-batting")
        bowling_section = soup.find("div", class_="player-career-bowling")

        # Extract Batting Stats
        bat_stats = batting_section.find_all("tr")[-1].find_all("td")  # Last row has career stats
        bat_avg = float(bat_stats[3].text.strip())  # Batting Avg
        bat_sr = float(bat_stats[4].text.strip())  # Batting Strike Rate

        # Extract Bowling Stats
        bowl_stats = bowling_section.find_all("tr")[-1].find_all("td")
        bowl_wickets = int(bowl_stats[3].text.strip())  # Wickets
        bowl_econ = float(bowl_stats[4].text.strip())  # Economy

        return {
            "bat_avg": bat_avg,
            "bat_sr": bat_sr,
            "bowl_wickets": bowl_wickets,
            "bowl_econ": bowl_econ
        }

    except:
        return None

# 🔹 Stop Command
@bot.on(events.NewMessage(pattern="/stop"))
async def stop_bot(event):
    await event.reply("⚠ **Bot is stopping... Goodbye!** 👋")
    sys.exit()

# 🔹 Run the bot
print("Bot is running...")
bot.run_until_disconnected()
