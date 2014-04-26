from flask import Flask
from flask import render_template, jsonify

app = Flask(__name__)

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/categories')
def categories():
    category_list = {
            1: 'drunk text',
            2: 'cringe pic'
            }

    return jsonify(category_list)
    
if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
