from flask import Blueprint, render_template, request, jsonify, session
import random

lab9 = Blueprint('lab9', __name__)

gifts = []

def init_gifts():
    """Создает ровно 10 подарков с твоими картинками"""
    if len(gifts) == 0:
        # Список твоих файлов (подарки внутри)
        image_files = [
            "3851175.png",
            "6272910.png",
            "8803517.png",
            "3787564.png",
            "439-4397899_thumb-image-transparent-iphone-gift-emoji-png-png.png",
            "6459276.png",
            "1280516.png",
            "4213958.png",
            "gift_box_present_icon_225155.png",
            "3702999.png"
        ]
        
        # Список уникальных поздравлений (ровно 10)
        wishes = [
            "Счастья!", "Здоровья!", "Любви!", "Денег!", 
            "Удачи!", "Успехов!", "Радости!", "Везения!", 
            "Добра!", "Тепла!"
        ]
        
        # Создаем 10 коробок
        for i in range(10):
            gifts.append({
                "id": i + 1,
                "x": random.randint(20, 700), 
                "y": random.randint(20, 400),
                "open": False,
                "message": wishes[i],
                "image": image_files[i] # Уникальная картинка для каждой коробки
            })

@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    init_gifts()
    if 'gift_count' not in session:
        session['gift_count'] = 0
    return render_template('lab9/index.html', gifts=gifts, count=session['gift_count'])

@lab9.route('/lab9/open', methods=['POST'])
def open_gift():
    gift_id = int(request.form.get('gift_id'))
    
    gift = None
    for g in gifts:
        if g['id'] == gift_id:
            gift = g
            break
            
    if not gift:
        return jsonify({"error": "Not found"}), 404

    if gift['open']:
        return jsonify({
            "status": "already_open", 
            "message": gift['message'], 
            "image": gift['image']
        })

    if session.get('gift_count', 0) >= 3:
        return jsonify({"status": "limit", "message": "Лимит исчерпан!"})

    gift['open'] = True
    session['gift_count'] = session.get('gift_count', 0) + 1
    
    return jsonify({
        "status": "success",
        "message": gift['message'],
        "image": gift['image'],
        "count": session['gift_count']
    })

@lab9.route('/lab9/reset')
def reset():
    gifts.clear()
    init_gifts()
    session['gift_count'] = 0
    return "Сброшено. <a href='/lab9/'>Назад</a>"