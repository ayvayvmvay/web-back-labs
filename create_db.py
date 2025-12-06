import sqlite3

# Подключаемся (файл создастся сам)
conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Создаем таблицу пользователей
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login VARCHAR(30) UNIQUE NOT NULL,
    password VARCHAR(162) NOT NULL
);
''')

# Создаем таблицу статей
cur.execute('''
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(50),
    article_text TEXT,
    is_favorite BOOLEAN DEFAULT 0,
    is_public BOOLEAN DEFAULT 0,
    likes INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
''')

conn.commit()
conn.close()

print("База данных database.db успешно создана! Таблицы готовы.")
