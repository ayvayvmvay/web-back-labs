from flask import Blueprint, render_template, request, redirect, session, current_app, flash, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from os import path
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
import re
import os
import random # Для генерации 30 пользователей

rgz = Blueprint('rgz', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='ivan_shevchenko_knowledge_base',
            user='ivan_shevchenko_knowledge_base',
            password='1'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

# --- Вспомогательная функция валидации ---
def validate_credentials(login, password):
    pattern = r"^[a-zA-Z0-9_!@#$%^&*()-+=]+$"
    if not login or not password:
        return "Логин и пароль не могут быть пустыми."
    if not re.match(pattern, login):
        return "Логин должен содержать только латинские буквы, цифры и знаки: _!@#$%^&*()-+="
    if not re.match(pattern, password):
        return "Пароль должен содержать только латинские буквы, цифры и знаки: _!@#$%^&*()-+="
    return None

@rgz.route('/rgz/')
def index():
    return render_template('rgz/index.html')

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    error = validate_credentials(login, password)
    if error:
        return render_template('rgz/register.html', error=error)
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users_rgz WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users_rgz WHERE login=?;", (login,))
        
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('rgz/register.html', error="Пользователь с таким логином уже существует")
        
    password_hash = generate_password_hash(password)
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users_rgz (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users_rgz (login, password) VALUES (?, ?);", (login, password_hash))
        
    db_close(conn, cur)
    return render_template('rgz/success_register.html')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
        
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not login or not password:
        return render_template('rgz/login.html', error="Введите логин и пароль")

    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users_rgz WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users_rgz WHERE login=?;", (login,))
        
    user = cur.fetchone()
    db_close(conn, cur)
    
    if user and check_password_hash(user['password'], password):
        session['rgz_login'] = user['login']
        session['rgz_id'] = user['id']
        return redirect('/rgz/')
    else:
        return render_template('rgz/login.html', error="Неверный логин или пароль")

@rgz.route('/rgz/logout')
def logout():
    session.pop('rgz_login', None)
    session.pop('rgz_id', None)
    return redirect('/rgz/')

@rgz.route('/rgz/delete_account', methods=['POST'])
def delete_account():
    login = session.get('rgz_login')
    if not login:
        return redirect('/rgz/login')
        
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM users_rgz WHERE login=%s;", (login,))
    else:
        cur.execute("DELETE FROM users_rgz WHERE login=?;", (login,))
    db_close(conn, cur)
    
    session.pop('rgz_login', None)
    session.pop('rgz_id', None)
    return redirect('/rgz/')

@rgz.route('/rgz/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('rgz_login')
    if not login:
        return redirect('/rgz/login')

    conn, cur = db_connect()

    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users_rgz WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT * FROM users_rgz WHERE login=?;", (login,))
        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('rgz/profile.html', user=user)

    try:
        name = request.form.get('name')
        age_raw = request.form.get('age')
        age = int(age_raw) if age_raw else None
        gender = request.form.get('gender')
        about = request.form.get('about')
        is_hidden = request.form.get('is_hidden') == 'on'
        
        # Пол для поиска (автоматически противоположный)
        looking_for = 'f' if gender == 'm' else 'm'

        file = request.files.get('photo')
        filename = None
        
        if file and file.filename:
            filename = secure_filename(file.filename)
            filename = f"{login}_{filename}"
            save_dir = os.path.join(current_app.root_path, 'static', 'rgz')
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            save_path = os.path.join(save_dir, filename)
            file.save(save_path)

        query_update = """
            UPDATE users_rgz 
            SET name=%s, age=%s, gender=%s, looking_for=%s, about=%s, is_hidden=%s
        """
        params = [name, age, gender, looking_for, about, is_hidden]

        if filename:
            query_update += ", photo=%s"
            params.append(filename)
        
        query_update += " WHERE login=%s"
        params.append(login)

        if current_app.config['DB_TYPE'] != 'postgres':
            query_update = query_update.replace('%s', '?')

        cur.execute(query_update, tuple(params))
        db_close(conn, cur)
        return redirect('/rgz/profile')
        
    except Exception as e:
        print(f"ОШИБКА: {e}")
        db_close(conn, cur)
        return f"Ошибка: {e}", 500

@rgz.route('/rgz/search')
def search_page():
    return render_template('rgz/search.html')

@rgz.route('/rgz/api', methods=['POST'])
def api():
    login = session.get('rgz_login')
    if not login:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    method = data.get('method')
    params = data.get('params', {})
    req_id = data.get('id')

    if method == 'search':
        page = params.get('page', 1)
        search_name = params.get('name', '')
        search_age = params.get('age', '')
        
        limit = 3
        offset = (page - 1) * limit

        conn, cur = db_connect()

        # 1. Узнаем мой пол и кого я ищу
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT gender, looking_for FROM users_rgz WHERE login=%s", (login,))
        else:
            cur.execute("SELECT gender, looking_for FROM users_rgz WHERE login=?", (login,))
        
        me = cur.fetchone()
        if not me or not me['gender']:
            db_close(conn, cur)
            return jsonify({'result': []}) # Профиль не заполнен

        my_gender = me['gender']
        target_gender = me['looking_for']

        # 2. ЛОГИКА ПОИСКА ИЗ ЗАДАНИЯ:
        # Ищем тех, у кого:
        # (gender == target_gender) AND (looking_for == my_gender)
        # То есть: если я парень ищу девушек, мне нужны Девушки, которые ищут Парней.
        
        query_parts = ["gender = %s", "looking_for = %s", "is_hidden = FALSE", "login != %s"]
        args = [target_gender, my_gender, login]

        if search_name:
            query_parts.append("name LIKE %s")
            args.append(f"%{search_name}%")

        if search_age:
            query_parts.append("age = %s")
            args.append(search_age)

        where_clause = " AND ".join(query_parts)
        
        if current_app.config['DB_TYPE'] != 'postgres':
            where_clause = where_clause.replace("%s", "?")

        sql = f"SELECT login, name, age, about, photo FROM users_rgz WHERE {where_clause} ORDER BY id LIMIT {limit} OFFSET {offset}"
        
        cur.execute(sql, args)
        users = [dict(row) for row in cur.fetchall()]
        db_close(conn, cur)

        return jsonify({
            'jsonrpc': '2.0',
            'result': users,
            'id': req_id
        })

    return jsonify({'jsonrpc': '2.0', 'error': 'Method not found', 'id': req_id})

# --- СЕКРЕТНЫЙ РОУТ ДЛЯ ГЕНЕРАЦИИ 30 ПОЛЬЗОВАТЕЛЕЙ ---
# Запустить один раз: открыть в браузере /rgz/init_db
# @rgz.route('/rgz/init_db')
# @rgz.route('/rgz/init_db')
# def init_db_data():
#     conn, cur = db_connect()
    
#     # Разный SQL для Postgres и SQLite
#     if current_app.config['DB_TYPE'] == 'postgres':
#         cur.execute("""
#             CREATE TABLE IF NOT EXISTS users_rgz (
#                 id SERIAL PRIMARY KEY,
#                 login VARCHAR(255) NOT NULL UNIQUE,
#                 password VARCHAR(255) NOT NULL,
#                 name VARCHAR(255),
#                 age INTEGER,
#                 gender VARCHAR(10),
#                 looking_for VARCHAR(10),
#                 about TEXT,
#                 photo VARCHAR(255),
#                 is_hidden BOOLEAN DEFAULT FALSE
#             );
#         """)
#     else:
#         # Для SQLite
#         cur.execute("""
#             CREATE TABLE IF NOT EXISTS users_rgz (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 login TEXT NOT NULL UNIQUE,
#                 password TEXT NOT NULL,
#                 name TEXT,
#                 age INTEGER,
#                 gender TEXT,
#                 looking_for TEXT,
#                 about TEXT,
#                 photo TEXT,
#                 is_hidden BOOLEAN DEFAULT 0
#             );
#         """)
    
#     conn.commit()

#     # Генерация данных
#     names_m = ['Ivan', 'Alex', 'Dmitry', 'Sergey', 'Andrey', 'Maxim', 'Pavel', 'Oleg', 'Egor', 'Vlad']
#     names_f = ['Maria', 'Anna', 'Elena', 'Olga', 'Tatiana', 'Natalia', 'Irina', 'Svetlana', 'Yulia', 'Daria']
    
#     default_pass = generate_password_hash('123') 

#     for i in range(30):
#         gender = 'm' if i % 2 == 0 else 'f'
#         name = random.choice(names_m) if gender == 'm' else random.choice(names_f)
#         login = f"user_{i}_{name.lower()}"
#         age = random.randint(18, 40)
#         looking_for = 'f' if gender == 'm' else 'm'
#         about = f"Привет, я {name}, мне {age}. Ищу пару!"
        
#         try:
#             # Postgres использует %s, SQLite использует ?
#             placeholder = "%s" if current_app.config['DB_TYPE'] == 'postgres' else "?"
            
#             # Формируем запрос с 7 плейсхолдерами
#             query = f"""
#                 INSERT INTO users_rgz (login, password, name, age, gender, looking_for, about)
#                 VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
#             """
            
#             cur.execute(query, (login, default_pass, name, age, gender, looking_for, about))
#         except Exception as e:
#             conn.rollback() # Откат, если ошибка (например, такой логин уже есть)
#             print(f"Ошибка вставки: {e}")

    # db_close(conn, cur)
    # return "База данных успешно создана и наполнена! (PostgreSQL/SQLite совместимость)"
