# Discord bot templete
This is a templete for creating a discord bot with a database. This is based on a refactor i made for my [college's discord bot](https://github.com/GameMagma/NWMSU-Bot/pull/1). 

check other branches for differnt templetes
 - no-database        // doesnt have a database

## Getting started
### Getting the project locally
software needed:
 - docker           to run the bot and db
 - git              to clone from github
software recommended:
 - python           if you want to run code outside of docker
 - preferred IDE    if you dont want to edit everything in a text editor

Step 1: Clone the repo
remember to cd to your desired directory 
```
git clone 
cd 
```

Optional Step: creating a virtual enviroment
```
# if you want to run code localy i would recommend using a venv
python -m venv env
pip install -r requirements.txt

# if psycopg2-binary==2.9.11 fails
# run "pip install psycopg2" instead
```

Step 2: setting up .env
use .envExample to create your .env
command to do so
```cp .envExample .env```

```
# you will need to [create a discord bot](https://discord.com/developers/applications) and put its token here
DISCORD_TOKEN= # put your discord bots token here
GUILD_ID=   # put the guild_id of the test server here, other wise remove it for global deployment


SQL_USER= testing        # create whatever username you want
SQL_PASSWORD= 1234       # create whatever password you want

SQL_HOST= postgres       # leave as is, match docker
SQL_PORT= 5432           # the port you want it to run on (5432 by default)
SQL_DATABASE= dbtest     # name it whatever you want          
```

Step 3: Starting containers
```
# make sure you have docker running

# build the services
docker compose build

# start the containers
docker compose up -d # -d runs it detached 
```
use ```docker compose down``` to stop containers

You should have a working local clone of the project now

## What needs reconfigured?
This templete comes with examples included in it. 
Check branches for templetes without examples

This is a full list of things you should change to match your use case
 - init.sql         // change to match your database

 - sql_manager.py   // define new functions to match your database

 - commands/*       // update commands for your use case 
                    // Note: leave the __init__.py files they are not commands
                    // game_request, database_query, and about.py
                    // should almost always be changed as there examples



## Project arcitectuer
basic overview of the project arcitecture
```
commands/            # holds all commands
├── gameRequest.py  # example database write command
├── about.py
├── health_check.py
├── say.py
├── database_query.py   # example database read command
├── status.py
└── __init__.py 

docs/               # holds additional documentation

.dockerignore       # tells docker what to ignore (not copy)
.envEXAMPLE         # .env creation reference
.gitignore          # tells git what to ignore
requirements.txt    # keeps all required external libraries needed to run this project

# I would recommend using discords built in way of locking slash commands
# but if you want control with code you can use these
channel.py          # holds additional logic for locking commands to channels
permissions.py      # holds additional logic for locking commands to roles

SQLManager          # holds logic for database operations
discordBot.py       # defines class discordBot which interacts with discord

docker-compose.yml  # tells docker how to build the project
Dockerfile          # tells docker how to build a container
init.sql            # inital templet for database initialization

main.py
```
