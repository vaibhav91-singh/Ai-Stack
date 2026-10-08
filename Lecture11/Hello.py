import flask
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

# Example API: Get details of a book
@app.route('/api/book', methods=['GET'])
def get_book():
    book = {
        "id": 1,
        "title": "Python Basics",
        "author": "John Doe",
        "year": 2025
    }
    return jsonify(book)

if __name__ == '__main__':
    app.run(debug=True)