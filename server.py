import json
from flask import Flask
from flask import render_template, Response, request

app = Flask(__name__)

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/categories')
def categories():
    #replace with db logic
    category_list = [
            {
                'id': 1,
                'name': 'cringe pics'
                },
            {
                'id': 2,
                'name': 'drunk text'
                }
            ]

    return Response(json.dumps(category_list),  mimetype='application/json')

@app.route('/confess',  methods = ['POST'])
def confess():
    #do some db logic here
    my_confession = request.json

    other_confession = {
            'category': 1,
            'text': 'confession text',
            'score': 4
            }

    response = {
            'mine': my_confession,
            'other': other_confession
            }

    return Response(json.dumps(response), mimetype='application/json');

if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
