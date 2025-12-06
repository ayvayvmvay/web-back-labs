from app import app
from lab8_db import db
# Импортируем модели ЯВНО, чтобы скрипт их увидел
from lab8_db.models import users, articles
import os

print("--- НАЧАЛО СОЗДАНИЯ ---")

with app.app_context():
    # 1. Создаем таблицы
    db.create_all()
    print("Команда create_all выполнена.")

    # 2. Проверяем, создался ли файл
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ivan_shevchenko_orm.db")
    
    if os.path.exists(db_path):
        print(f"Файл базы данных найден: {db_path}")
        size = os.path.getsize(db_path)
        print(f"Размер файла: {size} байт (если 0 — значит плохо, если больше — всё ок)")
    else:
        print("ОШИБКА: Файл базы данных не появился!")

print("--- ГОТОВО ---")


