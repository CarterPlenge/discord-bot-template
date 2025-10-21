import os
from dotenv import load_dotenv
from discord_bot import DiscordBot

load_dotenv()

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = int(os.getenv('GUILD_ID')) if os.getenv('GUILD_ID') else None

    bot = DiscordBot(guild_id=GUILD_ID)
    bot.run(TOKEN)
