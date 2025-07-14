from flask import Flask, request, jsonify, send_from_directory
from flask_cars import CARS
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

DB_FILE = 'cars.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER,
            body TEXT,
            fuel TEXT,
            image TEXT
        )""")
        conn.commit()

@app.route('/upload', methods=['POST'])
def upload_car():
    name = request.form.get('name')
    price = request.form.get('price')
    body = request.form.get('body')
    fuel = request.form.get('fuel')
    image = request.files.get('image')

    if not all([name, price, body, fuel, image]):
        return jsonify({'error': 'Missing fields'}), 400

    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO cars (name, price, body, fuel, image) VALUES (?, ?, ?, ?, ?)",
                  (name, int(price), body, fuel, filename))
        conn.commit()

    return jsonify({'message': 'Car uploaded successfully'})

@app.route('/cars', methods=['GET'])
def get_cars():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM cars")
        cars = [
            dict(id=row[0], name=row[1], price=row[2], body=row[3], fuel=row[4], image=row[5])
            for row in c.fetchall()
        ]
    return jsonify(cars)

@app.route('/delete/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT image FROM cars WHERE id=?", (car_id,))
        row = c.fetchone()
        if row and row[0]:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], row[0]))
            except FileNotFoundError:
                pass
        c.execute("DELETE FROM cars WHERE id=?", (car_id,))
        conn.commit()
    return jsonify({'message': 'Car deleted successfully'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
