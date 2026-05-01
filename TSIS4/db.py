import psycopg2
from config import DB_CONFIG


# Подключается к PostgreSQL через данные из config.py
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# Создаёт таблицы из schema.sql, если их ещё нет
def setup_database():
    conn = get_connection()
    cur = conn.cursor()

    with open("schema.sql", "r", encoding="utf-8") as file:
        cur.execute(file.read())

    conn.commit()
    cur.close()
    conn.close()


# Находит игрока по имени или создаёт нового
def get_or_create_player(username):
    conn = get_connection()
    cur = conn.cursor()

    # Добавляет игрока, если такого имени ещё нет
    cur.execute(
        """
        INSERT INTO players (username)
        VALUES (%s)
        ON CONFLICT (username) DO NOTHING
        """,
        (username,)
    )

    # Получает id игрока из таблицы players
    cur.execute(
        "SELECT id FROM players WHERE username = %s",
        (username,)
    )

    player_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return player_id


# Сохраняет результат игры в таблицу game_sessions
def save_result(username, score, level):
    player_id = get_or_create_player(username)

    conn = get_connection()
    cur = conn.cursor()

    # Добавляет новую игровую сессию игрока
    cur.execute(
        """
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
        """,
        (player_id, score, level)
    )

    conn.commit()
    cur.close()
    conn.close()


# Получает топ-10 лучших результатов
def get_top_10():
    conn = get_connection()
    cur = conn.cursor()

    # JOIN связывает результат игры с именем игрока
    cur.execute(
        """
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        ORDER BY g.score DESC
        LIMIT 10
        """
    )

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data


# Получает лучший личный результат конкретного игрока
def get_personal_best(username):
    conn = get_connection()
    cur = conn.cursor()

    # MAX берёт самый большой score этого игрока
    cur.execute(
        """
        SELECT MAX(g.score)
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        WHERE p.username = %s
        """,
        (username,)
    )

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    if result is None:
        return 0

    return result