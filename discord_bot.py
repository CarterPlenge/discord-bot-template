import discord
from discord import app_commands
from dotenv import load_dotenv
from commands import register_all
from logger import setup_logger

load_dotenv()
logger = setup_logger(__name__)

class DiscordBot:
    def __init__(self, database, guild_id: int | None = None):
        """Initalize the Discord bot"""
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.tree = app_commands.CommandTree(self.client)
        self.database = database
        self.guild_id = guild_id    # guild id == server id; leave as None to omit this
                                    # recommend only using guild_id for dev purpouses. 
                                    # leave as none for global deployment. This could take 
                                    # a few hours for slash commands to propagate.      
        self._setup_events()

    def _setup_events(self):
        """Sets up event handlers"""

        @self.client.event
        async def on_ready():
            logger.info(f"Logged in as {self.client.user}.")
            
            self.tree.clear_commands(guild=None)
            self.tree.clear_commands(guild=discord.Object(id=self.guild_id))
            
            logger.info("Registering commands, database, and guild id...")
            register_all(self.tree, self.database, self.guild_id)

            if self.guild_id is not None:
                logger.info(f"Guild id found. Syncing commands for server {self.guild_id}.")
                await self.tree.sync(guild=discord.Object(id=self.guild_id))
                logger.info(f"Sucessfully synced commands to server {self.guild_id}.")
            else:
                logger.info(f"No Guild id found. Syncing commands globaly.")
                logger.info(f"NOTE: it can take Discord a few hours to propogate global commands.")
                await self.tree.sync()
        
        @self.client.event
        async def on_guild_join(guild):
            """Called when bot joins a new server"""
            logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")
            self.database.get_guild_settings(guild.id)
            logger.info(f"Created guild settings for guild: {guild.id} in database.")
    
    # This code block is used to perform a task when a message is sent. 
    # --- Start of Code Block ---
    
        # @self.client.event 
        # async def on_message(message):
        #     """Called when a message is sent"""
        #     await self.handle_message(message)
            
    # async def handle_message(self, message):
    #     """
    #     Put functionality here if you want to do
    #     something on basic messages.
    #     """
    #     return
    
    # --- End of code block ---
    
    # for more events, check out here
    # https://discordpy.readthedocs.io/en/stable/api.html#event-reference
    
    def run(self, token):
        self.client.run(token)

if __name__ == "__main__":
    import os
    from sql_manager import SQLManager
    db = SQLManager(min_conn=2, max_conn=10)
    
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = int(os.getenv('GUILD_ID')) if os.getenv('GUILD_ID') else None
    
    bot = DiscordBot(db, GUILD_ID)
    bot.run(TOKEN)
            
