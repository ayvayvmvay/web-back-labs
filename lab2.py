from flask import Blueprint, url_for, redirect, request, abort, render_template

lab2 = Blueprint('lab2', __name__)
@lab2.route('/lab2/a')

# laba2
def a() :
    return 'без слеша'

@lab2.route('/lab2/a/')
def a2() :
    return 'со слешем'

flower_list = [
    {"name": "роза", "price": 100},
    {"name": "тюльпан", "price": 70},
    {"name": "незабудка", "price": 50},
    {"name": "ромашка", "price": 40},
]
@lab2.route('/lab2/add_flower/')
def add_flower_post():
    name = request.form.get("name")
    price = request.form.get("price")
    if not name or not price:
        return "Ошибка: не заданы имя или цена", 400
    flower_list.append({"name": name, "price": int(price)})
    return redirect("/lab2/flowers/")

@lab2.route('/lab2/add_flower/')
def add_flower_no_name():
    return "вы не задали имя цветка", 400

@lab2.route('/lab2/flowers/')
def all_flowers():
    return render_template("flowers.html", flowers=flower_list)




@lab2.route('/lab2/flowers/delete/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect('/lab2/flowers/')
# @lab2.route('/lab2/flowers/clear')
# def clear_flowers():
#     flower_list.clear()
#     return redirect('/lab2/flowers/')
   


@lab2.route('/lab2/example')
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



@lab2.route('/lab2/')
def lab22():
    return render_template('lab2.html')




@lab2.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers/')

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@lab2.route('/lab2/calc/<int:a>/<int:b>')
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

@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')
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

@lab2.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)

vegetables = [
    {"name": "Картофель", "desc": "Крупный молодой картофель", "img": "potato.jpg"},
    {"name": "Морковь", "desc": "Сладкая хрустящая морковь", "img": "carrot.jpg"},
    {"name": "Свёкла", "desc": "Сочная свёкла насыщенного цвета", "img": "beet.jpg"},
    {"name": "Капуста", "desc": "Белокочанная капуста", "img": "cabbage.jpg"},
    {"name": "Огурец", "desc": "Свежий зелёный огурец", "img": "cucumber.jpg"},
    {"name": "Помидор", "desc": "Спелый красный томат", "img": "tomato.jpg"},
    {"name": "Перец", "desc": "Болгарский перец яркого цвета", "img": "pepper.jpg"},
    {"name": "Баклажан", "desc": "Глянцевый фиолетовый баклажан", "img": "eggplant.jpg"},
    {"name": "Лук", "desc": "Золотистый репчатый лук", "img": "onion.jpg"},
    {"name": "Чеснок", "desc": "Ароматный свежий чеснок", "img": "garlic.jpg"},
    {"name": "Кабачок", "desc": "Молодой светло-зелёный кабачок", "img": "zucchini.jpg"},
    {"name": "Брокколи", "desc": "Плотные соцветия брокколи", "img": "broccoli.jpg"},
    {"name": "Цветная капуста", "desc": "Нежная белая цветная капуста", "img": "cauliflower.jpg"},
    {"name": "Редис", "desc": "Хрустящий розовый редис", "img": "radish.jpg"},
    {"name": "Тыква", "desc": "Крупная ярко-оранжевая тыква", "img": "pumpkin.jpg"},
    {"name": "Кукуруза", "desc": "Сладкая кукуруза в початках", "img": "corn.jpg"},
    {"name": "Сельдерей", "desc": "Зелёный черешковый сельдерей", "img": "celery.jpg"},
    {"name": "Петрушка", "desc": "Свежая зелёная петрушка", "img": "parsley.jpg"},
    {"name": "Укроп", "desc": "Ароматный пучок укропа", "img": "dill.jpg"},
    {"name": "Шпинат", "desc": "Свежие зелёные листья шпината", "img": "spinach.jpg"}
]

@lab2.route('/lab2/vegetables')
def vegetables_gallery():
    return render_template('vegetables.html', vegetables=vegetables)