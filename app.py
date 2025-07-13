from flask import Flask, render_template, request, redirect
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price TEXT,
            fuel TEXT,
            body TEXT,
            image TEXT
        )""")
init_db()

@app.route('/')
def home():
    with sqlite3.connect('database.db') as conn:
        cars = conn.execute("SELECT * FROM cars").fetchall()
    return render_template('index.html', cars=cars)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        fuel = request.form['fuel']
        body = request.form['body']
        image = request.files['image']
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            with sqlite3.connect('database.db') as conn:
                conn.execute("INSERT INTO cars (title, price, fuel, body, image) VALUES (?, ?, ?, ?, ?)",
                             (title, price, fuel, body, image.filename))
        return redirect('/admin')
    with sqlite3.connect('database.db') as conn:
        cars = conn.execute("SELECT * FROM cars").fetchall()
    return render_template('admin.html', cars=cars)

@app.route('/delete/<int:id>')
def delete(id):
    with sqlite3.connect('database.db') as conn:
        conn.execute("DELETE FROM cars WHERE id=?", (id,))
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
