from flask import Flask, url_for, request, redirect, abort, render_template
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
<head><meta charset="utf-8"><title>Лабораторная 1</title></head>
<body>
    <h1>Лабораторная 1</h1>
    <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, 
    а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, 
    сознательно предоставляющих лишь самые базовые возможности.</p>
    <p><a href="/">На корень сайта</a></p>
    <h2>Список роутов</h2>
    <ul>
        <li><a href="/">Главная страница</a></li>
        <li><a href="/index">Index</a></li>
        <li><a href="/lab1/web">/lab1/web</a></li>
        <li><a href="/lab1/author">/lab1/author</a></li>
        <li><a href="/lab1/image">/lab1/image</a></li>
        <li><a href="/lab1/counter">/lab1/counter</a></li>
        <li><a href="/lab1/counter/clear">/lab1/counter/clear</a></li>
        <li><a href="/lab1/info">/lab1/info</a></li>
        <li><a href="/lab1/created">/lab1/created</a></li>
        <li><a href="400">400 Bad Request</a></li>
        <li><a href="401">401 Unauthorized</a></li>
        <li><a href="402">402 Payment Required</a></li>
        <li><a href="403">403 Forbidden</a></li>
        <li><a href="404">Страница не найдена (404)</a></li>
        <li><a href="405">405 Method Not Allowed</a></li>
        <li><a href="418">418 I'm a teapot</a></li>
        <li><a href="/cause_500">Внутренняя ошибка сервера (500)</a></li>
    </ul>
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
                <p>Факультет: """ + faculty + """</sp>
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


    headers = {
        'Content-Language': 'ru',
        'X-Project': 'lab1',
        'X-Author': 'Shevchenko'
    }
    return html, 200, headers


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


ournal = []

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



@app.route('/cause_500')
def cause_500():
    raise RuntimeError("Ошибка для проверки 500")



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

# laba2
@app.route('/lab2/a')
def a() :
    return 'без слеша'

@app.route('/lab2/a/')
def a2() :
    return 'со слешем'


flower_list = ['василек', 'георгин', 'тюльпан', 'роза']

@app.route('/lab2/add_flower/')
def add_flower_no_name():
    return 'вы не задали имя цветка', 400


@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
    <!doctype html>
    <html>
        <body>
            <h1>Добавлен новый цветок</h1>
            <p>Название нового цветка: {name}</p>
            <p>Всего цветов: {len(flower_list)}</p>
            <p>Полный список: {flower_list}</p>
            <p><a href="/lab2/flowers/">Посмотреть все цветы</a></p>
        </body>
    </html>
    '''

@app.route('/lab2/flowers/')
def all_flowers():
    flowers_html = '<ul>'
    for f in flower_list:
        flowers_html += f'<li>{f}</li>'
    flowers_html += '</ul>'
    return f'''
    <!doctype html>
    <html>
        <head><meta charset="utf-8"><title>Все цветы</title></head>
        <body>
            <h1>Список всех цветов</h1>
            {flowers_html}
            <p>Всего цветов: {len(flower_list)}</p>
            <p><a href="/lab2/">Назад к лабораторной</a></p>
        </body>
    </html>
    '''


@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    flower = flower_list[flower_id]
    return f'''
   <!doctype html>
    <html>
        <head><meta charset="utf-8"><title>{flower}</title></head>
        <body>
            <h1>Цветок: {flower}</h1>
            <p>Индекс: {flower_id}</p>
            <p><a href="/lab2/flowers/">Посмотреть все цветы</a></p>
        </body>
    </html>
    '''

# @app.route('/lab2/flowers/clear')
# def clear_flowers():
#     flower_list.clear()
#     return redirect('/lab2/flowers/')
   


@app.route('/lab2/example')
def example():
    name, lab_numb, group, course = 'Шевченко Иван', 2, 'ФБИ-34', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'aпельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', name=name, lab_num=lab_numb, group=group,
course=course, fruits=fruits)



@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')




@app.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers/')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return f'''
    <!doctype html>
    <html>
    <head><meta charset="utf-8"><title>Калькулятор</title></head>
    <body>
        <h1>Калькулятор</h1>
        <ul>
            <li>{a} + {b} = {a + b}</li>
            <li>{a} - {b} = {a - b}</li>
            <li>{a} * {b} = {a * b}</li>
            <li>{a} / {b if b != 0 else 1} = {a / b if b != 0 else 'Нельзя делить на 0'}</li>
            <li>{a} ** {b} = {a ** b}</li>
        </ul>
        <p><a href="/lab2/">Назад</a></p>
    </body>
    </html>
    '''

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_a(a):
    return redirect(f'/lab2/calc/{a}/1')

    return redirect(f'/lab2/calc/{a}/1')

books = [
    {'author': 'Ф. Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 600},
    {'author': 'Л. Толстой', 'title': 'Война и мир', 'genre': 'Роман', 'pages': 1200},
    {'author': 'А. Пушкин', 'title': 'Евгений Онегин', 'genre': 'Поэма', 'pages': 300},
    {'author': 'М. Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'И. Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 350},
    {'author': 'Н. Гоголь', 'title': 'Мёртвые души', 'genre': 'Роман', 'pages': 400},
    {'author': 'А. Чехов', 'title': 'Вишнёвый сад', 'genre': 'Пьеса', 'pages': 120},
    {'author': 'А. Грин', 'title': 'Алые паруса', 'genre': 'Повесть', 'pages': 200},
    {'author': 'В. Набоков', 'title': 'Лолита', 'genre': 'Роман', 'pages': 450},
    {'author': 'А. Беляев', 'title': 'Человек-амфибия', 'genre': 'Фантастика', 'pages': 300}
]

@app.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)

