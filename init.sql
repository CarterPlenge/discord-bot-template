
-- this is an example table setup for the example code.
CREATE TABLE IF NOT EXISTS game_request (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT NOT NULL,
    username BIGINT NOT NULL,
    game VARCHAR(255) NOT NULL,
    platform VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending'
);

CREATE INDEX IF NOT EXISTS idx_game_request_username ON game_request(username);
CREATE INDEX IF NOT EXISTS idx_game_request_status ON game_request(status);
CREATE INDEX IF NOT EXISTS idx_game_request_created_at ON game_request(created_at DESC);

CREATE TABLE IF NOT EXISTS guild_settings (
    guild_id BIGINT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS guild_roles (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT NOT NULL,
    role_name VARCHAR(100) NOT NULL,
    role_id BIGINT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_guild_roles
        FOREIGN KEY(guild_id) 
        REFERENCES guild_settings(guild_id)
        ON DELETE CASCADE,
    UNIQUE(guild_id, role_name)
);

CREATE INDEX IF NOT EXISTS idx_guild_roles_guild_id ON guild_roles(guild_id);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_guild_settings_updated_at
    BEFORE UPDATE ON guild_settings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();