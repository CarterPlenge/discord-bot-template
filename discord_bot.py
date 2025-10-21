import discord
from discord import app_commands
from dotenv import load_dotenv
from commands import register_all

load_dotenv()

class DiscordBot:
    def __init__(self, guild_id: int | None = None):
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.tree = app_commands.CommandTree(self.client)
        self.guild_id = guild_id    # guild id == server id; leave as None to omit this
                                    # recommend only using guild_id for dev purpouses. 
        self._setup_events()

    def _setup_events(self):
        """Sets up event handlers"""

        @self.client.event
        async def on_ready():
            print(f"Logged in as {self.client.user}")
            
            self.tree.clear_commands(guild=None)
            self.tree.clear_commands(guild=discord.Object(id=self.guild_id))
            
            register_all(self.tree, self.guild_id)

            if self.guild_id is not None:
                await self.tree.sync(guild=discord.Object(id=self.guild_id))
                print(f"Synced commands to guild {self.guild_id}")
            else:
                await self.tree.sync()
                print("Synced commands globally")
        
        @self.client.event
        async def on_guild_join(guild):
            """Called when bot joins a new server"""
            print(f"Joined new guild: {guild.name} (ID: {guild.id})")
    
        # @self.client.event 
        # async def on_message(message):
        #     await self.handle_message(message)
            
    # async def handle_message(self, message):
    #     """
    #     Put functionality here if you want to do
    #     somthing on basic messages.
    #     """
    #     return
    
    # for more events check out here
    # https://discordpy.readthedocs.io/en/stable/api.html#event-reference
    
    def run(self, token):
        self.client.run(token)

if __name__ == "__main__":
    import os
    
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = int(os.getenv('GUILD_ID')) if os.getenv('GUILD_ID') else None
    
    bot = DiscordBot(GUILD_ID)
    bot.run(TOKEN)