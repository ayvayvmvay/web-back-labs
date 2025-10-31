from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if not x1 or not x2:
        return render_template('lab4/div.html', error="Введите оба числа!")

    x1 = float(x1)
    x2 = float(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error="Ошибка: делить на ноль нельзя")

    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods=['POST'])
def sum_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    x1 = float(x1) if x1 else 0
    x2 = float(x2) if x2 else 0
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')


@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    x1 = float(x1) if x1 else 1
    x2 = float(x2) if x2 else 1
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if not x1 or not x2:
        return render_template('lab4/sub.html', error="Ошибка: оба поля должны быть заполнены!")
    x1 = float(x1)
    x2 = float(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/pow', methods=['POST'])
def pow_():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if not x1 or not x2:
        return render_template('lab4/pow.html', error="Ошибка: оба поля должны быть заполнены!")
    x1 = float(x1)
    x2 = float(x2)
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error="Ошибка: 0⁰ не определено!")
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0
tree_max = 10


@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'POST':
        operation = request.form.get('operation')
        if operation == 'cut' and tree_count > 0:
            tree_count -= 1
        elif operation == 'plant' and tree_count < tree_max:
                tree_count += 1

        return redirect('/lab4/tree')

    if operation == 'cut':
        tree_count -=1
    elif operation == 'plant':
        tree_count +=1
        
    return render_template('lab4/tree.html', tree_count=tree_count, tree_max=tree_max)

users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Иванов', 'gender': 'м'},
    {'login': 'bob', 'password': '555', 'name': 'Борис Смирнов', 'gender': 'м'},
    {'login': 'dan', 'password': '111', 'name': 'Даниил Петров', 'gender': 'м'},
    {'login': 'abc', 'password': '444', 'name': 'Анна Обычная', 'gender': 'ж'}]
@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            return render_template('lab4/login.html', authorized=True, login=session['login'], name=session['name'])

    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        return render_template('lab4/login.html', error='Не введён логин', authorized=False, login='')
    if not password:
        return render_template('lab4/login.html', error='Не введён пароль', authorized=False, login=login)
    
    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']

            return redirect('/lab4/login')
                    
    error = 'Неверные логин или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)




@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')

    login = request.form.get('login')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    if not login or not name or not password or not confirm:
        return render_template('lab4/register.html', error='Заполните все поля!')
    if password != confirm:
        return render_template('lab4/register.html', error='Пароль и подтверждение не совпадают!')
    for user in users:
        if user['login'] == login:
            return render_template('lab4/register.html', error='Пользователь с таким логином уже существует!')

    users.append({'login': login, 'password': password, 'name': name})
    return redirect('/lab4/login')


@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    return render_template('lab4/users.html', users=users, current=session['login'])


@lab4.route('/lab4/edit', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_login = session['login']
    user = next((u for u in users if u['login'] == current_login), None)

    if request.method == 'GET':
        return render_template('lab4/edit.html', user=user)

    new_login = request.form.get('login')
    new_name = request.form.get('name')
    new_password = request.form.get('password')
    confirm = request.form.get('confirm')

    if not new_login or not new_name:
        return render_template('lab4/edit.html', user=user, error='Логин и имя обязательны!')

    if new_password or confirm:
        if new_password != confirm:
            return render_template('lab4/edit.html', user=user, error='Пароль и подтверждение не совпадают!')
        user['password'] = new_password

    user['login'] = new_login
    user['name'] = new_name
    session['login'] = new_login
    session['name'] = new_name
    return redirect('/lab4/users_list')


@lab4.route('/lab4/delete', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    login = session['login']
    global users
    users = [u for u in users if u['login'] != login]
    session.clear()
    return redirect('/lab4/login')




@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')

    temp = request.form.get('temperature')

    if not temp:
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')

    try:
        temp = float(temp)
    except ValueError:
        return render_template('lab4/fridge.html', error='Ошибка: введите числовое значение температуры')

    if temp < -12:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    elif temp > -1:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    elif -12 <= temp <= -9:
        snowflakes = 3
    elif -8 <= temp <= -5:
        snowflakes = 2
    elif -4 <= temp <= -1:
        snowflakes = 1
    else:
        return render_template('lab4/fridge.html', error='Ошибка: недопустимое значение температуры')

    return render_template('lab4/fridge.html', temperature=temp, snowflakes=snowflakes)


@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain_order():
    prices = {
        'ячмень': 12000,
        'овёс': 8500,
        'пшеница': 9000,
        'рожь': 15000
    }

    if request.method == 'GET':
        return render_template('lab4/grain.html', prices=prices)

    grain = request.form.get('grain')
    weight = request.form.get('weight')

    if not grain:
        return render_template('lab4/grain.html', prices=prices, error='Ошибка: не выбрано зерно')

    if not weight:
        return render_template('lab4/grain.html', prices=prices, error='Ошибка: не указан вес')

    try:
        weight = float(weight)
    except ValueError:
        return render_template('lab4/grain.html', prices=prices, error='Ошибка: вес должен быть числом')

    if weight <= 0:
        return render_template('lab4/grain.html', prices=prices, error='Ошибка: вес должен быть больше 0')
    if weight > 100:
        return render_template('lab4/grain.html', prices=prices, error='Ошибка: такого объёма сейчас нет в наличии')

    price_per_ton = prices[grain]
    total = price_per_ton * weight
    discount = 0

    if weight > 10:
        discount = total * 0.1
        total -= discount

    return render_template('lab4/grain.html', prices=prices, grain=grain, weight=weight, total=total, discount=discount)