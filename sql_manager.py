import os
import psycopg2
from psycopg2 import OperationalError, pool
from psycopg2.extras import RealDictCursor
from typing import Optional, Tuple, Any, List
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()


class SQLManager:
    """Manages PostgreSQL connections using connection pooling"""

    def __init__(self, min_conn=2, max_conn=10):
        """Initialize connection pool"""
        self.config = {
            "user": os.getenv("SQL_USER"),
            "password": os.getenv("SQL_PASSWORD"),
            "host": os.getenv("SQL_HOST"),
            "port": os.getenv("SQL_PORT", 5432),
            "dbname": os.getenv("SQL_DATABASE"),
        }
        
        try:
            self.pool = psycopg2.pool.ThreadedConnectionPool(
                min_conn,
                max_conn,
                **self.config
            )
            print(f"PostgreSQL connection pool created ({min_conn}-{max_conn} connections)")
        except OperationalError as err:
            print(f"Failed to create connection pool: {err}")
            raise

    @contextmanager
    def get_connection(self):
        """Context manager for getting pooled connections"""
        conn = self.pool.getconn()
        try:
            yield conn
        finally:
            self.pool.putconn(conn)

    @contextmanager
    def get_cursor(self, conn):
        """Context manager for database cursors"""
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
        finally:
            cursor.close()

    def _execute_query(
        self, query: str, params: Optional[Tuple] = None, fetch: Optional[str] = None
    ) -> Any:
        """Execute a query using pooled connections"""
        with self.get_connection() as conn:
            with self.get_cursor(conn) as cursor:
                try:
                    cursor.execute(query, params or ())
                    
                    if fetch == "one":
                        result = cursor.fetchone()
                    elif fetch == "all":
                        result = cursor.fetchall()
                    else:
                        result = None
                    
                    conn.commit()
                    return result
                    
                except psycopg2.Error as err:
                    conn.rollback()
                    print(f"Query execution error: {err}")
                    raise

    def add_game_request(self, guild_id: int, user_id: int, game: str, platform: str) -> Tuple[bool, str]:
        """Add a new game request to the database"""
        try:
            query = """
                INSERT INTO game_request (guild_id, username, game, platform)
                VALUES (%s, %s, %s, %s);
            """
            self._execute_query(query, (guild_id, user_id, game.lower().strip(), platform))
            return (True, f"Game request added: {game} on {platform}")
        except Exception as e:
            return (False, f"Error adding game request: {str(e)}")

    def get_game_requests(self, guild_id: int) -> Tuple[bool, List]:
        """Retrieve all game requests"""
        try:
            query = """
                SELECT * FROM game_request 
                WHERE guild_id = %s 
                ORDER BY id DESC;
            """
            results = self._execute_query(query, (guild_id,), fetch="all")
            return (True, results or [])
        except Exception as e:
            return (False, str(e))

    def delete_game_request(self, guild_id: int, request_id: int) -> Tuple[bool, str]:
        """Delete a game request"""
        try:
            query = """
                DELETE FROM game_request 
                WHERE id = %s AND guild_id = %s;
            """
            self._execute_query(query, (request_id, guild_id))
            return (True, "Game request deleted")
        except Exception as e:
            return (False, f"Error deleting game request: {str(e)}")

    def get_guild_settings(self, guild_id: int) -> Tuple[bool, dict]:
        """Get settings"""
        try:
            query = """
                SELECT * FROM guild_settings 
                WHERE guild_id = %s;
            """
            result = self._execute_query(query, (guild_id,), fetch="one")
            if not result:
                self._create_default_guild_settings(guild_id)
                result = self._execute_query(query, (guild_id,), fetch="one")
            return (True, dict(result))
        except Exception as e:
            return (False, str(e))

    def _create_default_guild_settings(self, guild_id: int):
        """Create default settings for a new guild"""
        query = """
            INSERT INTO guild_settings (guild_id)
            VALUES (%s)
            ON CONFLICT (guild_id) DO NOTHING;
        """
        self._execute_query(query, (guild_id,))

    def test_connection(self) -> bool:
        """Simple connectivity test"""
        try:
            query = "SELECT 1;"
            self._execute_query(query)
            print("Database connection test passed")
            return True
        except Exception as e:
            print(f"Database connection test failed: {e}")
            return False

    def close_pool(self):
        """Close all connections in the pool"""
        if self.pool:
            self.pool.closeall()
            print("Connection pool closed")

    def __enter__(self):
        """Support context manager protocol"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup on exit"""
        self.close_pool()