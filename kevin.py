from telethon import TelegramClient, events
import requests
from bs4 import BeautifulSoup
import sys  # For stopping the bot
import random  # For selecting best players


# 🔹 Replace with your actual credentials
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

# 🔹 Initialize Telegram Bot
bot = TelegramClient("cricket_stats_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 🔹 Store user data
user_state = {}

# 🔹 Start Command
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    user_state[event.sender_id] = {"step": 1}  # Start user flow
    await event.reply("🏏 **Welcome to Cricket Player Stats Bot!**\n\nEnter **Player Names** (comma-separated):")

# 🔹 Handle Player Name Input
@bot.on(events.NewMessage)
async def handle_input(event):
    user_id = event.sender_id
    if user_id not in user_state:
        return  # Ignore if user hasn't started the bot

    state = user_state[user_id]

    if state["step"] == 1:  # Player Names
        players = [player.strip() for player in event.text.split(",")]
        await event.reply(f"✅ Players received! Fetching stats...")

        best_players = await fetch_and_analyze_players(event, players)

        # Display final results
        response_text = "**🏏 Best Performing Players:**\n" + "\n".join([f"🔹 {p}" for p in best_players])
        response_text += "\n\n✅ **Detailed Stats Sent Below**..."
        await event.reply(response_text, link_preview=False)

        # Fetch & send detailed stats for each player
        for player in players:
            player_stats = fetch_stats_from_crex(player)
            if player_stats:
                await event.reply(player_stats, link_preview=False)

        del user_state[user_id]  # Reset user state

# 🔹 Fetch & Analyze Player Stats
async def fetch_and_analyze_players(event, players):
    player_stats = []

    for player in players:
        formatted_name = player.replace(" ", "-").lower()
        stats = fetch_stats_from_crex(player)
        if stats:
            player_stats.append((player, stats))

    # Sort by Batting Avg, SR, Bowling Wickets, Econ
    sorted_players = sorted(
        player_stats, key=lambda x: (
            x[1]['bat_avg'], x[1]['bat_sr'], x[1]['bowl_wickets'], -x[1]['bowl_econ']
        ), reverse=True
    )

    best_players = [p[0] for p in sorted_players[:5]]  # Top 5 Players

    return best_players

# 🔹 Scrape Player Stats from Crex
def fetch_stats_from_crex(player_name):
    formatted_name = player_name.replace(" ", "-").lower()
    url = f"https://crex.live/player-profile/{formatted_name}"

    response = requests.get(url)
    if response.status_code != 200:
        return f"❌ **Could not fetch data for {player_name}**"

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        # Extract Basic Information
        player_info = soup.find("h2", class_="formTitle").text.strip()
        birth_date = soup.find("td", class_="key", text="Birth").find_next_sibling("td").text.strip()
        nationality = soup.find("td", class_="key", text="Nationality").find_next_sibling("td").text.strip()
        teams = ", ".join([team.text.strip() for team in soup.find_all("span", class_="flexCenter")])

        # Extract Social Media Links
        instagram = soup.find("a", href=True, text="Instagram")
        twitter = soup.find("a", href=True, text="Twitter")
        instagram_link = instagram["href"] if instagram else "Not Available"
        twitter_link = twitter["href"] if twitter else "Not Available"

        # Extract Recent Batting & Bowling Form
        recent_batting = soup.find("tbody", id="recentId Batting")
        recent_bowling = soup.find("tbody", id="recentId Bowling")

        recent_bat_scores = [row.find_all("td")[1].text.strip() for row in recent_batting.find_all("tr")[:5]]
        recent_bowl_scores = [row.find_all("td")[1].text.strip() for row in recent_bowling.find_all("tr")[:5]]

        # Extract Career Stats
        career_batting = soup.find("div", class_="player-career-batting")
        career_bowling = soup.find("div", class_="player-career-bowling")

        # Extract Career Batting Stats
        bat_stats = career_batting.find_all("tr")[-1].find_all("td")
        bat_avg = float(bat_stats[8].text.strip())  # Batting Avg
        bat_sr = float(bat_stats[7].text.strip())  # Batting Strike Rate

        # Extract Career Bowling Stats
        bowl_stats = career_bowling.find_all("tr")[-1].find_all("td")
        bowl_wickets = int(bowl_stats[3].text.strip())  # Wickets
        bowl_econ = float(bowl_stats[4].text.strip())  # Economy

        stats_text = f"""
🏏 **{player_info} - Player Stats**  
🎂 **Birth Date:** {birth_date}  
🌍 **Nationality:** {nationality}  
🔹 **Teams Played For:** {teams}  

📌 **Recent Batting Form:** {', '.join(recent_bat_scores)}  
🎯 **Recent Bowling Form:** {', '.join(recent_bowl_scores)}  

🏆 **Career Batting Stats:**  
🔹 Average: {bat_avg}  
🔹 Strike Rate: {bat_sr}  

🎯 **Career Bowling Stats:**  
🔹 Wickets: {bowl_wickets}  
🔹 Economy: {bowl_econ}  

📲 **Social Media:**  
📸 [Instagram]({instagram_link}) | 🐦 [Twitter]({twitter_link})
        """
        return stats_text

    except:
        return f"❌ **Error extracting stats for {player_name}**"

# 🔹 Stop Command
@bot.on(events.NewMessage(pattern="/stop"))
async def stop_bot(event):
    await event.reply("⚠ **Bot is stopping... Goodbye!** 👋")
    sys.exit()

# 🔹 Run the bot
print("Bot is running...")
bot.run_until_disconnected()
