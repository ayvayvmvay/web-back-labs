from flask import Blueprint, render_template, request, redirect, session, current_app
from lab8_db import db
from lab8_db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_, func

lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html',
                               error='Имя пользователя не должно быть пустым')

    if not password_form:
        return render_template('lab8/register.html',
                               error='Пароль не должен быть пустым')
    
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)

    return redirect('/lab8/')


@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/login.html', error="Логин не должен быть пустым")

    if not password_form:
        return render_template('lab8/login.html', error="Пароль не должен быть пустым")

    user = users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):

        remember = bool(request.form.get('remember'))

        login_user(user, remember=remember)

        return redirect('/lab8/')

    return render_template('lab8/login.html', 
                           error='Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/articles/')
@login_required
def articles_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)


@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title')
    text = request.form.get('text')

    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    if not title or not text:
        return render_template(
            'lab8/create.html',
            error='Название и текст статьи не должны быть пустыми'
        )

    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=text,
        is_favorite=is_favorite,
        is_public=is_public,
        likes=0
    )

    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/articles/')


@lab8.route('/lab8/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return "Доступ запрещен", 403

    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)

    title = request.form.get('title')
    text = request.form.get('text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    if not title or not text:
        return render_template(
            'lab8/edit.html',
            article=article,
            error="Поля не должны быть пустыми"
        )

    article.title = title
    article.article_text = text
    article.is_favorite = is_favorite
    article.is_public = is_public

    db.session.commit()
    return redirect('/lab8/articles/') 


@lab8.route('/lab8/delete/<int:article_id>/')
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return "Доступ запрещен", 403

    db.session.delete(article)
    db.session.commit()

    return redirect('/lab8/articles/')


@lab8.route('/lab8/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/public/')
def public_articles():
    public_list = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/public.html', articles=public_list)


@lab8.route('/lab8/search/')
def search_articles():
    query = request.args.get("q", "")

    if not query:
        return render_template('lab8/search.html', articles=[])

    q_lower = f"%{query.lower()}%"

    if current_user.is_authenticated:
        results = articles.query.filter(
            or_(
                func.lower(articles.title).like(q_lower),
                func.lower(articles.article_text).like(q_lower)
            ),
            or_(
                articles.login_id == current_user.id,
                articles.is_public == True
            )
        ).all()
    else:
        results = articles.query.filter(
            or_(
                func.lower(articles.title).like(q_lower),
                func.lower(articles.article_text).like(q_lower)
            ),
            articles.is_public == True
        ).all()

    return render_template('lab8/search.html', articles=results, query=query)