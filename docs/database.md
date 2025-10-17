# The Database
## Where is it?
the database is stored in the named Docker volume '''postgres_data'''.
This volume persist across container restarts and prevents re-running init.sql

init.sql is mounted into the Docker volume on its first creation to create the database

To remove the volume (and delete the database) use '''docker-compose down -v'''

## how to create a new table
### Add it to init.sql
This will cause the table to be created when the container is built for the first time.
This will make it easier for people to build the database localy and work on this project.
However this will not update any existing databases. Only redefine how to initialize it.

### Adding it to built database
since init.sql is only ran when a container is created for the first time we will have 
to manual create new tables for existing databases

first we have to connect to the db
```docker-compose exec postgres psql -U botuser -d discord_bot```

Then we create the table manualy
```
CREATE TABLE IF NOT EXISTS game_request (
    id SERIAL PRIMARY KEY,
    username BIGINT NOT NULL,
    game VARCHAR(255) NOT NULL,
    platform VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending'
);
```