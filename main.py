import discord
import os
from dotenv import load_dotenv
from discord_bot import DiscordBot
from logger import setup_logger

load_dotenv()
logger = setup_logger(__name__)


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    DISCORD_OBJECT = discord.Object(id=int(os.getenv('GUILD_ID')) if os.getenv('GUILD_ID') else None)
    
    try:
        bot = DiscordBot(discord_object=DISCORD_OBJECT)
        logger.info("Starting run process...")
        bot.run(TOKEN)
    finally:
        logger.info("Shutdown successfull.")