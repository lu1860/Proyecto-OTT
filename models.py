import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS watch_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    show_id INTEGER,
    show_name TEXT,
    video_url TEXT,
    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        subscription_type TEXT NOT NULL
    )
    """)


    conn.commit()
    conn.close()
    
def user_exists(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    return cursor.fetchone() is not None
    
def create_user(username, password, subscription_type="FREE"):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password, subscription_type) VALUES (?, ?, ?)",
            (username, password, subscription_type)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print(" Usuario creado correctamente")
    finally:
        conn.close()
        
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, subscription_type FROM users")
    users = cursor.fetchall()

    conn.close()
    return users

def get_user(username,password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, subscription_type FROM users WHERE username = ? AND password = ?", 
        (username, password)
    )
    user = cursor.fetchone()

    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, subscription_type FROM users WHERE id = ?", 
        (user_id,)
    )
    user = cursor.fetchone()

    conn.close()
    return user

def update_subscription_type(user_id, new_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET subscription_type = ? WHERE id = ?", 
        (new_type, user_id)
    )
    
    conn.commit()
    conn.close()
    

