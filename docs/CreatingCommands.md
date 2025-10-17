# Creating Commands
```
commands/
├── user/           # commands in here should be callable for all users
│   ├── gameRequest.py
│   ├── about.py
│   └── __init__.py
├── board/           # commands in here should be callable for boad members
│   ├── healthCheck.py
│   ├── setStatus.py
│   └── __init__.py 
├── admin/           # commands in here should be callable for select few
│   ├── shutdown.py
│   └── __init__.py 
```
This project is structured to read in commands from individual python files.

the **__init__.py** files are used to load in all the commands.
This means to create a new command we just need to create a new python file where we want it.

Note: there is no logic built into locking commands based on their directory. You must specify 
who is allowed to call the command in the command file. Please put your command in the appropriate
directory for organization purpouses. 

## Writing a command walkthough
```
#
# To start we need to bring in the packages we will be using
#
from discord import app_commands, Object, Interaction
from permissions import require_any_role
from datetime import datetime

#
# Next we need to define a register function for the __init__.py 
# to add the command to the bots command tree. 
# We convert the guild_id (an int) into a discord.Object 
#

def register(tree, database, guild_id):
    guild = Object(id=guild_id) if guild_id else None

    #
    # Here we will create our command using decorators
    #

    # This defines the command name and description
    # IMPORTANT: DO NOT USE CAPITAL LETTERS. discord commands cant have caps
    @tree.command(name="add", description="adds two numbers together", guild=guild)

    # This will lock the command to only work if someone has a specific role
    # ommiting this will result in it being callable by anyone. (like the about command)
    @require_any_role("Esports Staff", "President", "Trusted bot contributor")

    # Here we will describe parameters and give them a discription
    # omiting this will result in a command with no params (like the about command)
    @app_commands.describe(
        num1="first number",
        num2="second number"
    )

    # We can lock parameters to use only set values using this
    # check out admin/status.py and gameRequest.py for more examples.
    # here i will only lock param num2 to set choices
    @app_commands.choices(
        num2=[
            app_commands.Choice(name="one", value=1),
            app_commands.Choice(name="two", value=2),
            app_commands.Choice(name="three", value=3)
        ]
    )

    #
    # Here is where we will define our command functionality
    #

    # function name doesnt technicly matter but try to match command name
    async def command_add(interaction: Interaction, num1: str, num2: app_commands.Choice[str]):
        
        # trade Choice name for choice value
        real_num2 = num2.value

        num1 = int(num1)

        total = num1 + real_num2

        # return a response
        await interaction.response.send_message(
            f"{num1} + {real_num2} = {total}", 
            ephemeral=True # this makes it only show to the person who called the command
        )
```