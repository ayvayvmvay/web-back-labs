from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.route("/")
@app.route("/web")

def start():    
    
    return "<!doctype html>"\
        "<html>"\
        "   <body>"\
        "       <h1>web-сервер на flask</h1>"\
        "   </body>"\
        "</html>"


@app.route("/author")
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


@app.route('/image')
def image():
    path = url_for("static", filename="oak.jpg")
    return '''
<!doctype html>
<html>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''


count = 0
@app.route('/counter')
def counter():
    global count
    count +=1
    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr 
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + time + ''' <br>
        Запрошенный адрес: ''' + url + ''' <br>
        Ваш IP-адрес: ''' + client_ip + ''' <br>
    </body>
</html>
'''

@app.route("/info")
def info():
    return redirect("/author")

@app.route("/created")
def created():
    return '''git commit -m "код 201"
<!doctype html"
<html>
    <body>
        <h1>Создано успешноo</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''',201

