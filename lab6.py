from flask import Blueprint, render_template, request, session, current_app
from psycopg2.extras import RealDictCursor
import sqlite3
import psycopg2
from os import path

lab6 = Blueprint('lab6', __name__)
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='daniil_volkov_knowledge_base',
            user='daniil_volkov_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab6.route('/lab6/')
def lab():

    return render_template('lab6/lab6.html')




@lab6.route('/lab6/json-rpc-api', methods=['POST'])


def api():
    data = request.json
    id = data['id']
    if data['method'] == 'info':
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM offices ORDER BY number")
        else:
            cur.execute("SELECT * FROM offices ORDER BY number")

        offices = cur.fetchall()


        login = session.get('login')
        total = 0

        if login:
            for office in offices:
                if office['tenant'] == login:
                    total += office['price']        
        db_close(conn, cur)


        return {
            'jsonrpc': '2.0',
            'result': {
                "offices": offices,
                "total": total
            },            'id': id
        }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {'code': 1, 'message': 'Unauthorized'},


            'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']
        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number=%s", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number=?", (office_number,))

        office = cur.fetchone()

        if office['tenant']:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {'code': 2, 'message': 'Office already booked'},
                'id': id
            }

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE offices SET tenant=%s WHERE number=%s", (login, office_number))
        else:
            cur.execute("UPDATE offices SET tenant=? WHERE number=?", (login, office_number))

        db_close(conn, cur)

        return {'jsonrpc': '2.0', 'result': 'success', 'id': id}
    if data['method'] == 'cancellation':
        office_number = data['params']
        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number=%s", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number=?", (office_number,))

        office = cur.fetchone()

        if not office['tenant']:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {'code': 3, 'message': 'Office not booked'},
                'id': id
            }

        if office['tenant'] != login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {'code': 4, 'message': 'Not your booking'},
                'id': id
            }

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE offices SET tenant='' WHERE number=%s", (office_number,))
        else:
            cur.execute("UPDATE offices SET tenant='' WHERE number=?", (office_number,))

        db_close(conn, cur)

        return {'jsonrpc': '2.0', 'result': 'success', 'id': id}
    return {
        'jsonrpc': '2.0',
        'error': {'code': -32601, 'message': 'Method not found'},


        'id': id
    }

