import json
import sqlite3
from flask import Flask
from flask import render_template, Response, request, g

app = Flask(__name__)
DATABASE = 'data.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def control_rows():
    db = get_db()
    cur = db.cursor()

    #control number of rows
    print 'deleting old rows'
    cur.execute('DELETE FROM Confessions where id NOT IN (SELECT id from Confessions ORDER BY id DESC LIMIT 1000)')
    db.commit()


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/categories')
def categories():
    category_list = []

    cur = get_db().cursor()

    cur.execute('SELECT * from Categories ORDER BY RANDOM() LIMIT 8')

    cats = cur.fetchall()

    for cat in cats:
        cur.execute('SELECT id from Confessions where id_category=?', (cat[0],))
        total_confessions = len(cur.fetchall())

        category_as_dict = {
            'id': cat[0],
            'name': cat[1],
            'image': cat[2],
            'total': total_confessions
        }
        category_list.append(category_as_dict)

    confession_count = len(cur.execute('SELECT * from Confessions').fetchall())

    totals = {
        'confessions': confession_count,
        'categories': category_list
    }

    return Response(json.dumps(totals),  mimetype='application/json')


@app.route('/confess',  methods = ['POST'])
def confess():
    chosen_category = request.json['category']

    cur = get_db().cursor()

    cur.execute('SELECT * from Confessions where id_category=? ORDER BY RANDOM() LIMIT 1', (chosen_category,))

    confession = cur.fetchone()

    other_confession = {
        'id': confession[0],
        'category': confession[1],
        'text': confession[2],
        'score': confession[3]
    }

    return Response(json.dumps(other_confession), mimetype='application/json')


@app.route('/save', methods = ['POST'])
def save():
    mine = request.json['mine']
    other = request.json['other']
    db = get_db()
    cur = db.cursor()

    #Insert
    cur.execute(u'INSERT INTO Confessions VALUES(NULL,?,?,?)', (mine['category'], mine['text'], mine['score']))
    not_this = cur.lastrowid

    #Update other score
    cur.execute('UPDATE Confessions SET score=? WHERE id=?', (other['score'], other['id']))

    db.commit()

    cur.execute('SELECT * from Confessions WHERE id != ? ORDER BY RANDOM() LIMIT 20 ', (not_this,))

    confession_list = []

    confessions = cur.fetchall()

    for confession in confessions:
        confession_as_dict = {
            'category': confession[1],
            'text': confession[2],
            'score': confession[3]
        }
        confession_list.append(confession_as_dict)

    room_content = {
        'mine': mine,
        'other': confession_list
    }

    control_rows()

    return Response(json.dumps(room_content), mimetype='application/json')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
