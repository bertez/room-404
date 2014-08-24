import json
import sqlite3
from flask import Flask
from flask import render_template, Response, request, g, session
from auth import requires_auth

app = Flask(__name__)
DATABASE = 'data.db'
MAX_SCORE = 5
MIN_SCORE = 1
DEFAULT_TEXT = 'I tried to cheat Room 404 and it did not work out'
MAX_TEXT_LENGTH = 300

secret = '' #set your secret key here

try:
    from production_cfg import secret
except ImportError:
    pass

app.secret_key = secret


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def control_rows():
    db = get_db()
    cur = db.cursor()

    #control number of rows
    cur.execute('DELETE FROM Confessions where id NOT IN (SELECT id from Confessions ORDER BY id DESC LIMIT 5000)')
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
        'text': confession[2],
        'score': confession[3]
    }

    session['other_id'] = other_confession

    return Response(json.dumps(other_confession), mimetype='application/json')


@app.route('/save', methods = ['POST'])
def save():
    mine = request.json['mine']
    other = request.json['other']
    db = get_db()
    cur = db.cursor()

    available_categories = [x[0] for x in cur.execute('SELECT id from Categories').fetchall()]

    #extra sanitizing
    _category = mine['category'] in available_categories or 1
    _text = mine['text'] or DEFAULT_TEXT
    _text = _text[:MAX_TEXT_LENGTH]
    _score = sorted([MIN_SCORE, mine['score'], MAX_SCORE])[1]
    _other_id = session['other_id']['id']
    _other_score = sorted([session['other_id']['score'] - 1, other['score'],session['other_id']['score'] + 1 ])[1]

    #Insert
    cur.execute(u'INSERT INTO Confessions VALUES(NULL,?,?,?)', (_category, _text, _score))
    not_this = cur.lastrowid

    #Update other score
    cur.execute('UPDATE Confessions SET score=? WHERE id=?', (_other_score, _other_id))

    db.commit()
    session.clear()

    cur.execute('SELECT Confessions.text, Confessions.score, Categories.image from Confessions, Categories WHERE Categories.id = Confessions.id_category AND Confessions.id != ? ORDER BY RANDOM() LIMIT 20 ', (not_this,))

    confession_list = []

    confessions = cur.fetchall()

    for confession in confessions:
        confession_as_dict = {
            'text': confession[0],
            'score': confession[1],
            'image': confession[2]
        }
        confession_list.append(confession_as_dict)

    room_content = {
        'mine': mine,
        'other': confession_list
    }

    control_rows()

    return Response(json.dumps(room_content), mimetype='application/json')

@app.route('/admin', methods = ['GET', 'POST'])
@requires_auth
def admin():
    db = get_db()
    cur = get_db().cursor()

    if request.method == 'POST':
        delete_id = request.json['id']
        print delete_id

        try:
            cur.execute('DELETE from Confessions WHERE id=?', (delete_id,))
            db.commit()
            return 'OK'
        except sqlite3.Error, msg:
            print msg
            return msg, 500


    cur.execute('SELECT id, text from Confessions ORDER BY id desc')

    log = [dict(id=row[0], text=row[1]) for row in cur.fetchall()]

    return render_template('shitty-admin.html', log=log)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
