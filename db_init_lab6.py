import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Создаем таблицу offices
cur.execute('''
CREATE TABLE IF NOT EXISTS offices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER NOT NULL,
    tenant VARCHAR(30) DEFAULT '',
    price INTEGER NOT NULL
);
''')

# Очищаем таблицу перед заполнением (чтобы не дублировать при повторном запуске)
cur.execute("DELETE FROM offices;")

# Заполняем 10 офисов (Task 6 и 8)
for i in range(1, 11):
    # Логика цены: например, базовые 900 + немного вариации
    price = 900 + (i % 3) * 100 
    cur.execute("INSERT INTO offices (number, tenant, price) VALUES (?, ?, ?);", (i, '', price))

conn.commit()
conn.close()

print("Таблица offices успешно создана и заполнена 10 кабинетами!")