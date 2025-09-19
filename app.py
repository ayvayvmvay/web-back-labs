from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

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
            </ul>
        </nav>
        <footer>
            <p>Шевченко Иван Юрьевич, ФБИ-34, 3 курс, 2025</p>
        </footer>
    </body>
</html>'''

@app.route('/lab1')
def lab1():
    return '''<!doctype html>
<html>
    <head><title>Лабораторная 1</title></head>
    <body>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, 
        а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, 
        сознательно предоставляющих лишь самые базовые возможности.</p>
        <p><a href="/">На корень сайта</a></p>
    </body>
</html>'''


@app.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/lab1/author">author</a>
            </body>
        </html>""", 200, {
            "X-Server": "sample",
            'Content-Type': 'text/plain; charset=utf-8'
            }


@app.route("/lab1/author")
def author():
    name = "Шевченко Иван Юрьевич"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""


@app.route('/lab1/image')
def image():
    css = url_for('static', filename='lab1.css')
    img = url_for('static', filename='oak.jpg')
    html = f'''<!doctype html>

<html>
    <head>
        <meta charset="utf-8">
        <title>Дуб</title>
        <link rel="stylesheet" href="{css}">
    </head>
    <body>
        <h1>Дуб</h1>
        <img class="lab1" src="{img}" alt="Дуб">
    </body>
</html>'''
    return html


count = 0


count = 0
@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr 
    clear_url = url_for('clear_counter')
    return f'''
<!doctype html>
<html>
    <head><title>Счётчик</title></head>
    <body>
        Сколько раз вы сюда заходили: {count}
        <hr>
        Дата и время: {time} <br>
        Запрошенный адрес: {url} <br>
        Ваш IP-адрес: {client_ip} <br>
        <p><a href="{clear_url}">Очистить счётчик</a></p>
    </body>
</html>
'''

@app.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect(url_for('counter'))

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html"
<html>
    <body>
        <h1>Создано успешноo</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''',201

@app.route("/400")
def bad_request():
    return '''<!doctype html>
<html>
<head>
    <title>400 Bad Request</title>
</head>
<body>
    <h1>400 Bad Request</h1>
    <p>Сервер не может обработать запрос из-за синтаксической ошибки.</p>
</body>
</html>''', 400

@app.route("/401")
def unauthorized():
    return '''<!doctype html>
<html>
<head>
    <title>401 Unauthorized</title>
</head>
<body>
    <h1>401 Unauthorized</h1>
    <p>Для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
</body>
</html>''', 401

@app.route("/402")
def payment_required():
    return '''<!doctype html>
<html>
<head>
    <title>402 Payment Required</title>
</head>
<body>
    <h1>402 Payment Required</h1>
    <p>Для доступа к ресурсу требуется оплата.</p>
</body>
</html>''', 402

@app.route("/403")
def forbidden():
    return '''<!doctype html>
<html>
<head>
    <title>403 Forbidden</title>
</head>
<body>
    <h1>403 Forbidden</h1>
    <p>Доступ к ресурсу запрещен.</p>
</body>
</html>''', 403

@app.route("/405")
def method_not_allowed():
    return '''<!doctype html>
<html>
<head>
    <title>405 Method Not Allowed</title>
</head>
<body>
    <h1>405 Method Not Allowed</h1>
    <p>Метод нельзя применить для данного ресурса.</p>
</body>
</html>''', 405

@app.route("/418")
def teapot():
    return '''<!doctype html>
<html>
<head>
    <title>418 I'm a teapot</title>
</head>
<body>
    <h1>418 I'm a teapot</h1>
    <p>Я чайник и не могу заваривать кофе.</p>
</body>
</html>''', 418

@app.errorhandler(404)
def not_found(err):
    img = url_for('static', filename='404.png')
    return f'''<!doctype html>
<html>
<head><meta charset="utf-8"><title>Ошибка 404</title>
<style>
  body {{
    background: white;
    color: black;
    font-family:Arial;
    text-align:center;
    padding:40px
    }}
  h1 {{
    color:#ff6b6b
    }}
  img {{
    width:300px;
    margin-top:20px
    }}
</style>
</head>
<body>
  <h1>Страница не найдена (404)</h1>
  <p>Такой страницы нет.</p>
  <img src="{img}" alt="404">
  <p><a href="/">Вернуться на главную</a></p>
</body>
</html>''', 404
