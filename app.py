from flask import Flask, url_for, request, redirect, abort, render_template, session
import datetime
from lab1 import lab1
from lab2 import lab2
import datetime
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
import os
from rgz import rgz



app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретный_ключ123')
app.config['DB_TYPE'] = 'sqlite'
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(rgz)


  

@app.route('/')
@app.route('/index')
def index():
    return '''<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header><h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1></header>
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/lab2">Вторая лабораторная</a></li>
                <li><a href="/lab3">Третья лабораторная</a></li>
                <li><a href="/lab4">Четвертая лабораторная</a></li>
                <li><a href="/lab5">Пятая лабораторная</a></li>
                <li><a href="/lab6">Шестая лабораторная</a></li>





            </ul>
        </nav>
        <footer>
            <p>Шевченко Иван Юрьевич, ФБИ-34, 3 курс, 2025</p>
        </footer>
    </body>
</html>'''



journal = []

@app.errorhandler(404)
def not_found(err):
    img = url_for('static', filename='404.jpg')
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr
    url = request.url

    entry = f"{time} — {ip} — {url}"
    journal.append(entry)

    log_html = "<h3>Журнал:</h3><ul>"
    for record in journal[-10:]:
        log_html += f"<li>{record}</li>"
    log_html += "</ul>"

    img = url_for('static', filename='404.jpg')


    return f'''<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Ошибка 404</title>
    <style>
      body {{
        background: white;
        color: black;
        font-family: Arial;
        text-align: center;
        padding: 40px;
      }}
      h1 {{
        color: black;
      }}
      img {{
        width: 250px;
        margin: 20px;
      }}
      .journal {{
        text-align: left;
        margin-top: 30px;
      }}
    </style>
</head>
<body>
     <h1>Страница не найдена</h1>
    <p><b>Ваш IP:</b> {ip}</p>
    <p><b>Дата и время:</b> {time}</p>
    <p><a href="/">Вернуться на главную</a></p>
      <img src="{img}" alt="404">
    <div class="journal">
        {log_html}
    </div>
</body>
</html>''', 404





@app.errorhandler(500)
def handle_500(err):
    return '''<!doctype html>
<html>
<head><meta charset="utf-8"><title>Ошибка 500</title></head>
<body>
  <h1>Внутренняя ошибка сервера (500)</h1>
  <p>Произошла ошибка. Попробуйте позже.</p>
  <a href="/">На главную</a>
</body>
</html>''', 500 
