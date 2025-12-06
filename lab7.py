from flask import Blueprint, render_template, request, abort, jsonify
import sqlite3
from os import path
import datetime

lab7 = Blueprint('lab7', __name__)

DB_NAME = 'lab7.db'

def db_connect():
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, DB_NAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def init_db():
    conn, cur = db_connect()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            title_ru TEXT NOT NULL,
            year INTEGER,
            description TEXT
        );
    """)
    
    db_close(conn, cur)

init_db()

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films")
    films = [dict(row) for row in cur.fetchall()]
    db_close(conn, cur)
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    
    if film is None:
        abort(404)
        
    return jsonify(dict(film))

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM films WHERE id = ?", (id,))
    db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def update_film(id):
    film = request.get_json()
    errors = {}
    
    if not film.get('title_ru'):
        errors['title_ru'] = 'Русское название не может быть пустым'

    if not film.get('title'):
        if film.get('title_ru'):
            film['title'] = film['title_ru']
        else:
             errors['title'] = 'Укажите оригинальное или русское название'

    current_year = datetime.datetime.now().year
    year = film.get('year')
    if not year:
        errors['year'] = 'Укажите год'
    elif not (1895 <= int(year) <= current_year):
        errors['year'] = f'Год должен быть от 1895 до {current_year}'

    description = film.get('description')
    if not description:
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    if errors:
        return errors, 400

    conn, cur = db_connect()
    
    cur.execute("SELECT id FROM films WHERE id = ?", (id,))
    if cur.fetchone() is None:
        db_close(conn, cur)
        abort(404)

    cur.execute('''
        UPDATE films 
        SET title = ?, title_ru = ?, year = ?, description = ?
        WHERE id = ?
    ''', (film['title'], film['title_ru'], film['year'], film['description'], id))
    
    db_close(conn, cur)
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    errors = {}
    
    if not film.get('title_ru'):
        errors['title_ru'] = 'Русское название не может быть пустым'

    if not film.get('title'):
        if film.get('title_ru'):
            film['title'] = film['title_ru']
        else:
             errors['title'] = 'Укажите оригинальное или русское название'

    current_year = datetime.datetime.now().year
    year = film.get('year')
    if not year:
        errors['year'] = 'Укажите год'
    elif not (1895 <= int(year) <= current_year):
        errors['year'] = f'Год должен быть от 1895 до {current_year}'

    description = film.get('description')
    if not description:
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    if errors:
        return errors, 400

    conn, cur = db_connect()
    cur.execute('''
        INSERT INTO films (title, title_ru, year, description)
        VALUES (?, ?, ?, ?)
    ''', (film['title'], film['title_ru'], film['year'], film['description']))
    
    new_id = cur.lastrowid
    db_close(conn, cur)
    
    film['id'] = new_id
    return jsonify(film)