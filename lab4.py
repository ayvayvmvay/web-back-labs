from flask import Blueprint, render_template, request, redirect
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
