from flask import Blueprint, render_template, request, redirect
import psycopg2
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    name =  'Anonymous'
    return render_template('lab5/lab5.html', name=name)


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    login = request.form.get('login')
    password = request.form.get('password')
    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'daniil_volkov_knowledge_base',
        user = 'daniil_volkov_knowledge_base',
        password = '123'
    )
    cur = conn.cursor()
    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html', error="Такой пользователь уже существует")
    cur.execute(f"INSERT INTO users (login,password) VALUES ('{login}', '{password}');")
    conn.commit()
    cur.close()
    conn.close()
    return render_template('lab5/success.html', login=login)    