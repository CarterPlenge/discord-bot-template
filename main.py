import discord
import os
from dotenv import load_dotenv
from discord_bot import DiscordBot
from sql_manager import SQLManager
from logger import setup_logger

load_dotenv()
logger = setup_logger(__name__)

db = SQLManager(min_conn=2, max_conn=10)

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    DISCORD_OBJECT = discord.Object(id=int(os.getenv('GUILD_ID')) if os.getenv('GUILD_ID') else None)

    if not db.test_connection():
        logger.error("Failed to connect to database. Exiting...")
        exit(1)
    
    try:
        bot = DiscordBot(database=db, discord_object=DISCORD_OBJECT)
        logger.info("Starting run process...")
        bot.run(TOKEN)
    finally:
        logger.info("Closing database pool...")
        db.close_pool()
        logger.info("Shutdown successfull.")