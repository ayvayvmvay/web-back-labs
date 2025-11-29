import os
import sqlite3
from werkzeug.security import generate_password_hash
from os import path
import random

# Путь к базе данных (как в вашем коде)
dir_path = path.dirname(path.realpath(__file__))
db_path = path.join(dir_path, "database.db")

# Подключаемся
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Создаём таблицу, если её нет (на всякий случай)
cur.execute("""
CREATE TABLE IF NOT EXISTS users_rgz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT,
    age INTEGER,
    gender TEXT,
    looking_for TEXT,
    about TEXT,
    photo TEXT,
    is_hidden INTEGER DEFAULT 0
)
""")

# Хеш пароля (один для всех)
password_hash = generate_password_hash("password123")

# Список имён для разнообразия
names = [
    "Alex", "Maria", "Dmitry", "Anna", "Ivan", "Olga", "Sergey", "Elena", "Andrey", "Natalia",
    "Mikhail", "Irina", "Vladimir", "Tatiana", "Nikolai", "Svetlana", "Pavel", "Yulia", "Roman", "Galina",
    "Kirill", "Polina", "Artem", "Daria", "Oleg", "Victoria", "Boris", "Alina", "Viktor", "Ksenia"
]

# Генерация 30 пользователей
for i in range(1, 31):
    login = f"user{i}"
    name = names[i - 1] if i <= len(names) else f"User{i}"
    
    # 10 пользователей — 20 лет, остальные — случайный возраст от 18 до 35
    if i <= 10:
        age = 20
    else:
        age = random.randint(18, 35)
    
    # Чередуем пол: m, f, m, f...
    gender = "m" if i % 2 == 1 else "f"
    looking_for = "f" if gender == "m" else "m"
    
    about = f"Привет! Меня зовут {name}. Мне {age} лет. Ищу общения."
    is_hidden = 0  # все видимые
    
    # photo остаётся NULL (не заполняем)
    photo = None
    
    try:
        cur.execute("""
            INSERT INTO users_rgz 
            (login, password, name, age, gender, looking_for, about, photo, is_hidden)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (login, password_hash, name, age, gender, looking_for, about, photo, is_hidden))
        print(f"Добавлен: {login}, возраст: {age}, пол: {gender}")
    except sqlite3.IntegrityError:
        print(f"Пользователь {login} уже существует — пропускаем.")

# Сохраняем и закрываем
conn.commit()
conn.close()

print("\n✅ База данных успешно заполнена 30 пользователями.")