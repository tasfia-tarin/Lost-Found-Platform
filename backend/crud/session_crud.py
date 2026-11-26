from datetime import datetime, timezone

from crud.user_crud import get_database_connection


def create_refresh_session(
    user_id: int,
    token_hash: str,
    expires_at: datetime,
    user_agent: str | None = None,
    ip_address: str | None = None,
):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO refresh_sessions
                (user_id, token_hash, expires_at, user_agent, ip_address)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    user_id,
                    token_hash,
                    expires_at,
                    user_agent,
                    ip_address,
                ),
            )

            return cursor.fetchone()[0]

def get_active_refresh_session(token_hash: str):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, user_id, token_hash, expires_at,
                       revoked_at, user_agent, ip_address
                FROM refresh_sessions
                WHERE token_hash = %s
                  AND revoked_at IS NULL
                  AND expires_at > %s
                """,
                (token_hash, datetime.now(timezone.utc)),
            )

            return cursor.fetchone()

def revoke_refresh_session(session_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE refresh_sessions
                SET revoked_at = %s
                WHERE id = %s
                  AND revoked_at IS NULL
                """,
                (datetime.now(timezone.utc), session_id),
            )

            return cursor.rowcount > 0


def revoke_all_user_sessions(user_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE refresh_sessions
                SET revoked_at = %s
                WHERE user_id = %s
                  AND revoked_at IS NULL
                """,
                (datetime.now(timezone.utc), user_id),
            )

            return cursor.rowcount


def get_user_active_sessions(user_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, created_at, expires_at, user_agent, ip_address
                FROM refresh_sessions
                WHERE user_id = %s
                  AND revoked_at IS NULL
                  AND expires_at > %s
                ORDER BY created_at DESC
                """,
                (user_id, datetime.now(timezone.utc)),
            )

            return cursor.fetchall()


def rotate_refresh_session(
    old_token_hash: str,
    new_token_hash: str,
    expires_at: datetime,
    user_agent: str | None = None,
    ip_address: str | None = None,
):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:

            # Find and lock the active old session
            cursor.execute(
                """
                SELECT id, user_id
                FROM refresh_sessions
                WHERE token_hash = %s
                  AND revoked_at IS NULL
                  AND expires_at > NOW()
                FOR UPDATE
                """,
                (old_token_hash,),
            )

            old_session = cursor.fetchone()

            if not old_session:
                return None

            old_session_id, user_id = old_session

            # Create the new refresh session
            cursor.execute(
                """
                INSERT INTO refresh_sessions
                (user_id, token_hash, expires_at, user_agent, ip_address)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    user_id,
                    new_token_hash,
                    expires_at,
                    user_agent,
                    ip_address,
                ),
            )

            new_session_id = cursor.fetchone()[0]

            # Revoke the old session and link the replacement
            cursor.execute(
                """
                UPDATE refresh_sessions
                SET revoked_at = NOW(),
                    replaced_by = %s
                WHERE id = %s
                """,
                (new_session_id, old_session_id),
            )

            return user_id