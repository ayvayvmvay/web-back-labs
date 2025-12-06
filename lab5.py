from flask import Blueprint, render_template, request, redirect, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

# Пытаемся импортировать psycopg2, но если его нет - не падаем, так как используем SQLite
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None
    RealDictCursor = None

lab5 = Blueprint('lab5', __name__)

def db_connect():

    if current_app.config['DB_TYPE'] == 'postgres':
        if psycopg2 is None:
            raise ImportError("Для работы с Postgres нужен модуль psycopg2")
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='ivan_shevchenko_knowledge_base',
            user='ivan_shevchenko_knowledge_base',
            password='1'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        # SQLite подключение
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    """Сохранение изменений и закрытие соединения"""
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    # Проверка существования пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Такой пользователь уже существует")

    # Создание пользователя
    password_hash = generate_password_hash(password)
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
        
    user = cur.fetchone()

    # Если пользователь не найден
    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    # Проверка пароля
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()

    if not title or not article_text:
        return render_template(
            'lab5/create_article.html', 
            error='Заполните поля',
            title=title, 
            article_text=article_text
        )

    conn, cur = db_connect()

    # Получаем ID пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login') # Если юзер в сессии есть, а в БД нет (странная ситуация, но бывает)

    # Создаем статью
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles(user_id, title, article_text) VALUES (%s, %s, %s);",
                    (user['id'], title, article_text))
    else:
        cur.execute("INSERT INTO articles(user_id, title, article_text) VALUES (?, ?, ?);",
                    (user['id'], title, article_text))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Получаем ID пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')

    # Получаем статьи
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY id DESC;", (user['id'],))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id=? ORDER BY id DESC;", (user['id'],))

    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    # Проверяем, принадлежит ли статья пользователю
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user['id']))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user['id']))

    article = cur.fetchone()
    if not article:
        db_close(conn, cur)
        return redirect('/lab5/list')

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()

    if not title or not article_text:
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article, error='Нельзя сохранить пустую статью')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", (title, article_text, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    # Удаляем только если статья принадлежит юзеру
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s;", (article_id, user['id']))
    else:
        cur.execute("DELETE FROM articles WHERE id=? AND user_id=?;", (article_id, user['id']))
    
    db_close(conn, cur)
    return redirect('/lab5/list')




@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Получаем данные пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user)

    # Обработка POST запроса (обновление данных)
    name = request.form.get('name')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')

    if password: 
        # Если пользователь хочет сменить пароль
        if password != password_confirm:
             db_close(conn, cur)
             return render_template('lab5/profile.html', user=user, error="Пароли не совпадают")
        
        password_hash = generate_password_hash(password)
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET name=%s, password=%s WHERE login=%s;", (name, password_hash, login))
        else:
            cur.execute("UPDATE users SET name=?, password=? WHERE login=?;", (name, password_hash, login))
    else:
        # Если меняем только имя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET name=%s WHERE login=%s;", (name, login))
        else:
            cur.execute("UPDATE users SET name=? WHERE login=?;", (name, login))

    db_close(conn, cur)
    return redirect('/lab5/profile')

@lab5.route('/lab5/users')
def users_list():
    conn, cur = db_connect()
    
    cur.execute("SELECT login, name FROM users;")
    users = cur.fetchall()
    
    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)