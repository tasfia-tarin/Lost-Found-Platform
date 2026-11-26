import os
import psycopg


def get_database_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("Database URL not found")

    return psycopg.connect(
        database_url,
        sslmode="require"
    )


def row_to_user(row):
    if row is None:
        return None

    return {
        "id": row[0],
        "email": row[1],
        "password_hash": row[2],
        "role": row[3],
        "is_banned": row[4],
        "failed_login_attempts": row[5],
        "locked_until": row[6],
        "created_at": row[7],
        "updated_at": row[8],
        "password_changed_at": row[9]
    }


def create_user(email: str, password_hash: str):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.users (email, password_hash)
                VALUES (%s, %s)
                RETURNING id, email, password_hash, role,
                          is_banned, failed_login_attempts,
                          locked_until, created_at, updated_at,
                          password_changed_at
                """,
                (email.lower().strip(), password_hash)
            )

            row = cursor.fetchone()

    return row_to_user(row)


def get_user_by_email(email: str):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, password_hash, role,
                       is_banned, failed_login_attempts,
                       locked_until, created_at, updated_at,
                       password_changed_at
                FROM public.users
                WHERE LOWER(email) = LOWER(%s)
                """,
                (email.strip(),)
            )

            row = cursor.fetchone()

    return row_to_user(row)


def get_user_by_id(user_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, password_hash, role,
                       is_banned, failed_login_attempts,
                       locked_until, created_at, updated_at,
                       password_changed_at
                FROM public.users
                WHERE id = %s
                """,
                (user_id,)
            )

            row = cursor.fetchone()

    return row_to_user(row)


def reset_failed_login_attempts(user_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.users
                SET failed_login_attempts = 0,
                    locked_until = NULL,
                    updated_at = NOW()
                WHERE id = %s
                """,
                (user_id,)
            )


def increment_failed_login_attempts(user_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.users
                SET failed_login_attempts = failed_login_attempts + 1,
                    locked_until = CASE
                        WHEN failed_login_attempts + 1 >= 5
                        THEN NOW() + INTERVAL '15 minutes'
                        ELSE locked_until
                    END,
                    updated_at = NOW()
                WHERE id = %s
                """,
                (user_id,)
            )


def update_user_email(user_id: int, email: str):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.users
                SET email = %s,
                    updated_at = NOW()
                WHERE id = %s
                RETURNING id, email, role, is_banned
                """,
                (email.lower().strip(), user_id)
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "email": row[1],
        "role": row[2],
        "is_banned": row[3]
    }


def update_user_password(user_id: int, password_hash: str):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.users
                SET password_hash = %s,
                    password_changed_at = NOW(),
                    updated_at = NOW()
                WHERE id = %s
                """,
                (password_hash, user_id)
            )

            return cursor.rowcount > 0



def get_all_users(search: str = "", limit: int = 20, offset: int = 0):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, role, is_banned,
                       failed_login_attempts, locked_until,
                       created_at, updated_at
                FROM public.users
                WHERE email ILIKE %s
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                (f"%{search.strip()}%", limit, offset),
            )

            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "email": row[1],
            "role": row[2],
            "is_banned": row[3],
            "failed_login_attempts": row[4],
            "locked_until": row[5],
            "created_at": row[6],
            "updated_at": row[7],
        }
        for row in rows
    ]


def count_users(search: str = ""):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM public.users
                WHERE email ILIKE %s
                """,
                (f"%{search.strip()}%",),
            )

            return cursor.fetchone()[0]


def get_user_statistics():
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COUNT(*),
                    COUNT(*) FILTER (WHERE role = 'admin'),
                    COUNT(*) FILTER (WHERE role = 'user'),
                    COUNT(*) FILTER (WHERE is_banned = TRUE)
                FROM public.users
                """
            )

            row = cursor.fetchone()

    return {
        "total_users": row[0],
        "total_admins": row[1],
        "total_regular_users": row[2],
        "banned_users": row[3],
    }

def ban_user(user_id: int, reason: str):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.users
                SET is_banned = TRUE,
                    ban_reason = %s,
                    updated_at = NOW()
                WHERE id = %s
                  AND role = 'user'
                RETURNING id, email, role, is_banned, ban_reason
                """,
                (reason.strip(), user_id),
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "email": row[1],
        "role": row[2],
        "is_banned": row[3],
        "ban_reason": row[4],
    }


def unban_user(user_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.users
                SET is_banned = FALSE,
                    ban_reason = NULL,
                    updated_at = NOW()
                WHERE id = %s
                  AND role = 'user'
                RETURNING id, email, role, is_banned, ban_reason
                """,
                (user_id,),
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "email": row[1],
        "role": row[2],
        "is_banned": row[3],
        "ban_reason": row[4],
    }
def update_user_role(user_id: int, new_role: str):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.users
                SET role = %s,
                    updated_at = NOW()
                WHERE id = %s
                  AND role = 'user'
                RETURNING id, email, role
                """,
                (new_role, user_id),
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "email": row[1],
        "role": row[2],
    }