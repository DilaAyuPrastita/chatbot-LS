import pymysql

# Konfigurasi database
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "chatbot",
    "connect_timeout": 5
}

def get_db_connection():
    return pymysql.connect(**db_config)

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Buat tabel users jika belum ada
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(50) UNIQUE,
        name VARCHAR(100),
        phone VARCHAR(20) NULL
    )
    """)

    # Buat tabel chat_history jika belum ada
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(50),
        message TEXT,
        response TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """)

    # Buat tabel user_activity jika belum ada
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_activity (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(50),
        activity TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# Panggil fungsi ini hanya jika file ini dijalankan langsung
if __name__ == "__main__":
    try:
        create_tables()
        print("Tabel berhasil dibuat.")
    except Exception as e:
        print("Gagal membuat tabel:", e)
