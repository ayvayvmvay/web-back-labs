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


@lab3.route('/lab3/train')
def train():
    errors = {}
    fio = request.args.get('fio', '').strip()
    shelf = request.args.get('shelf', '')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    age = request.args.get('age', '')
    departure = request.args.get('departure', '').strip()
    destination = request.args.get('destination', '').strip()
    date = request.args.get('date', '')
    insurance = request.args.get('insurance')

    if request.args:
        if not fio:
            errors['fio'] = 'Введите ФИО'
        if not shelf:
            errors['shelf'] = 'Выберите полку'
        if not age or not age.isdigit() or not (1 <= int(age) <= 120):
            errors['age'] = 'Укажите корректный возраст'
        if not departure:
            errors['departure'] = 'Укажите пункт выезда'
        if not destination:
            errors['destination'] = 'Укажите пункт назначения'
        if not date:
            errors['date'] = 'Укажите дату'

        if not errors:
            price = 1000 if int(age) >= 18 else 700
            if shelf in ['нижняя', 'нижняя боковая']:
                price += 100
            if linen:
                price += 75
            if baggage:
                price += 250
            if insurance:
                price += 150
            ticket_type = 'Детский билет' if int(age) < 18 else 'Взрослый билет'
            return render_template('lab3/train_ticket.html',
                                   fio=fio,
                                   shelf=shelf,
                                   linen=bool(linen),
                                   baggage=bool(baggage),
                                   age=age,
                                   departure=departure,
                                   destination=destination,
                                   date=date,
                                   insurance=bool(insurance),
                                   price=price,
                                   ticket_type=ticket_type)

    return render_template('lab3/train_form.html',
                           errors=errors,
                           fio=fio,
                           shelf=shelf,
                           linen=linen,
                           baggage=baggage,
                           age=age,
                           departure=departure,
                           destination=destination,
                           date=date,
                           insurance=insurance)


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_style')
    return resp

products = [
    {"name": "iPhone 11", "price": 30990, "weight": "194g", "color": "черный"},
    {"name": "iPhone 12", "price": 38990, "weight": "164g", "color": "белый"},
    {"name": "iPhone 13", "price": 40990, "weight": "174g", "color": "синий"},
    {"name": "iPhone 14", "price": 43990, "weight": "172g", "color": "красный"},
    {"name": "iPhone 14 Plus", "price": 55990, "weight": "203g", "color": "черный"},
    {"name": "iPhone 14 Pro", "price": 70990, "weight": "204g", "color": "серебро"},
    {"name": "iPhone 14 Pro Max", "price": 80990, "weight": "240g", "color": "зеленый"},
    {"name": "iPhone 15", "price": 48990, "weight": "171g", "color": "белый"},
    {"name": "iPhone 15 Plus", "price": 55990, "weight": "201g", "color": "черный"},
    {"name": "iPhone 15 Pro", "price": 79990, "weight": "187g", "color": "красный"},
    {"name": "iPhone 15 Pro Max", "price": 94990, "weight": "221g", "color": "синий"},
    {"name": "iPhone 16e", "price": 51990, "weight": "190g", "color": "золотой"},
    {"name": "iPhone 16", "price": 57990, "weight": "198g", "color": "серебро"},
    {"name": "iPhone 16 Plus", "price": 65990, "weight": "212g", "color": "черный"},
    {"name": "iPhone 16 Pro", "price": 90990, "weight": "180g", "color": "белый"},
    {"name": "iPhone 16 Pro Max", "price": 105990, "weight": "225g", "color": "красный"},
    {"name": "iPhone 17", "price": 119990, "weight": "185g", "color": "зеленый"},
    {"name": "iPhone Air", "price": 130990, "weight": "162g", "color": "серый"},
    {"name": "iPhone 17 Pro", "price": 139990, "weight": "188g", "color": "синий"},
    {"name": "iPhone 17 Pro Max", "price": 154990, "weight": "230g", "color": "черный"},
]


@lab3.route('/lab3/products')
def products_page():
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')
    min_price = min(p["price"] for p in products)
    max_price = max(p["price"] for p in products)

    user_min = request.args.get('min_price', type=int) or (int(min_price_cookie) if min_price_cookie else min_price)
    user_max = request.args.get('max_price', type=int) or (int(max_price_cookie) if max_price_cookie else max_price)

    if user_min > user_max:
        user_min, user_max = user_max, user_min

    filtered = [p for p in products if user_min <= p["price"] <= user_max]

    resp = make_response(render_template(
        'lab3/products.html',
        products=filtered,
        count=len(filtered),
        min_price=user_min,
        max_price=user_max,
        min_price_all=min_price,
        max_price_all=max_price
    ))

    resp.set_cookie('min_price', str(user_min))
    resp.set_cookie('max_price', str(user_max))

    return resp

@lab3.route('/lab3/products/reset')
def reset_products():
    resp = make_response(redirect('/lab3/products'))
    resp.delete_cookie('min_price')
    resp.delete_cookie('max_price')
    return resp
