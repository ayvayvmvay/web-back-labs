from flask import Blueprint, render_template, request, redirect, session, current_app, flash, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from os import path
import sqlite3
import re
import os
import random 

rgz = Blueprint('rgz', __name__)

def db_connect():
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
    
    # Проверка существования пользователя
    cur.execute("SELECT login FROM users_rgz WHERE login=?;", (login,))
        
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('rgz/register.html', error="Пользователь с таким логином уже существует")
        
    password_hash = generate_password_hash(password)
    
    # Регистрация
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
            SET name=?, age=?, gender=?, looking_for=?, about=?, is_hidden=?
        """
        params = [name, age, gender, looking_for, about, is_hidden]

        if filename:
            query_update += ", photo=?"
            params.append(filename)
        
        query_update += " WHERE login=?"
        params.append(login)

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
        cur.execute("SELECT gender, looking_for FROM users_rgz WHERE login=?", (login,))
        
        me = cur.fetchone()
        if not me or not me['gender']:
            db_close(conn, cur)
            return jsonify({'result': []}) # Профиль не заполнен

        my_gender = me['gender']
        target_gender = me['looking_for']

        # 2. Поиск с фильтрами
        query_parts = ["gender = ?", "looking_for = ?", "is_hidden = 0", "login != ?"]
        args = [target_gender, my_gender, login]

        if search_name:
            query_parts.append("name LIKE ?")
            args.append(f"%{search_name}%")

        if search_age:
            query_parts.append("age = ?")
            args.append(search_age)

        where_clause = " AND ".join(query_parts)
        
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