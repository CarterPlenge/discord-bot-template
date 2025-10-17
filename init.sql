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

GRANT CONNECT ON DATABASE discord_bot TO botuser;
GRANT USAGE ON SCHEMA public TO botuser;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO botuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO botuser;