from flask import Blueprint, render_template, request, abort, jsonify

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')

films = [
    {
        "title": "Intouchables",
        "title_ru": "1+1",
        "year": 2011,
        "description": "Пострадав в результате несчастного случая, богатый аристократ Филипп нанимает в помощники человека, который менее всего подходит для этой работы, – молодого жителя предместья Дрисса, только что освободившегося из тюрьмы. Несмотря на то, что Филипп прикован к инвалидному креслу, Дриссу удается привнести в размеренную жизнь аристократа дух приключений."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения."
    },
    {
        "title": "The Gentlemen",
        "title_ru": "Джентльмены",
        "year": 2019,
        "description": "Один ушлый американец ещё со студенческих лет приторговывал наркотиками, а теперь придумал схему нелегального обогащения с использованием поместий обедневшей английской аристократии и очень неплохо на этом разбогател. Другой пронырливый журналист приходит к Рэю, правой руке американца, и предлагает тому купить киносценарий, в котором подробно описаны преступления его босса при участии других представителей лондонского криминального мира — партнёра-еврея, китайской диаспоры, чернокожих спортсменов и даже русского олигарха."
    }
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    films.pop(id)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def update_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    
    film = request.get_json()
    
    if film.get('description') == '':
        return {'description': 'Заполните описание'}, 400

    films[id] = film
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    if film.get('description') == '':
        return {'description': 'Заполните описание'}, 400

    films.append(film)
    return jsonify(film)