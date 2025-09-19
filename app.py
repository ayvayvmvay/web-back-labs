from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "Нет такой страницы", 404

@app.route("/")

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




