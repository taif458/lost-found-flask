
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return connn

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM lost_items').fetchall()
    conn.close()
    return render_template('index.html', items=items)



@app.route('/add', methods=['GET', 'POST'])
def add_lost_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        description = request.form['description']
        location = request.form['location']
        date_lost = request.form['date_lost']
        contact_info = request.form['contact_info']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO lost_items (item_name, description, location, date_lost, contact_info) VALUES (?, ?, ?, ?, ?)',
            (item_name, description, location, date_lost, contact_info)
        )
        conn.commit()
        conn.close()

        return redirect('/')
    



@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        conn = get_db_connection()
        results = conn.execute(
            "SELECT * FROM lost_items WHERE item_name LIKE ? OR location LIKE ? OR description LIKE ?",
            ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')
        ).fetchall()
        conn.close()
    return render_template('search.html', results=results)


if __name__ == '__main__':
    app.run(host="0.0.0.0",
    port=5000 , debug=True)