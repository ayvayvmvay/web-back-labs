from flask import Blueprint, render_template
from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    return render_template('lab3/lab3.html')
    name = request.cookies.get('name') or 'Аноним'
    name_color = request.cookies.get('name_color') or '#000000'
    age = request.cookies.get('age') or 'не указан'
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)



@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cokie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')

    errors = {}

    if request.args:
        if not user:
            errors['user'] = 'Введите имя'
        if not age:
            errors['age'] = 'Заполните возраст'

        if not errors:
            return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors={})

    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    drink = request.args.get('drink')
    milk = request.args.get('milk')
    sugar = request.args.get('sugar')

    prices = {
        'coffee': 120,
        'black-tea': 80,
        'green-tea': 70
    }

    price = prices.get(drink, 0)
    if milk == 'on':
        price += 30
    if sugar == 'on':
        price += 10

    return render_template('lab3/pay.html', drink=drink, milk=milk, sugar=sugar, price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    text_color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')

    if text_color or bg_color or font_size or font_style:
        resp = make_response(redirect('/lab3/settings'))
        if text_color:
            resp.set_cookie('color', text_color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_style:
            resp.set_cookie('font_style', font_style)
        return resp

    return render_template('lab3/settings.html',
        color=request.cookies.get('color'),
        bg_color=request.cookies.get('bg_color'),
        font_size=request.cookies.get('font_size'),
        font_style=request.cookies.get('font_style')
    )