from flask import Blueprint, render_template

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    name =  'Anonymous'
    return render_template('lab5/lab5.html', name=name)