from flask import Flask, render_template, request, redirect, url_for, session
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secretkey123' 


items = []

ADMIN_PASSWORD = "admin123"

@app.context_processor
def inject_datetime():
    return dict(datetime=datetime)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_lost', methods=['GET', 'POST'])
def add_lost():
    if request.method == 'POST':
        name = request.form.get('name')
        item_name = request.form.get('item_name')
        description = request.form.get('description')
        
        if not all([name, item_name, description]):
            return "Error: Missing form fields", 400 
        
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Missing"
        claim_status = "Unclaimed"
        report_id = random.randint(10000, 99999)

        item = {
            'id': report_id,
            'name': name,
            'item_name': item_name,
            'description': description,
            'date': date,
            'status': status,
            'claim_status': claim_status
        }
        items.append(item)
        return render_template('search.html', report_id=report_id)
    return render_template('add_lost.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    found_item = None
    not_found = False

    if request.method == 'POST':
        report_id = request.form['report_id']
        for item in items:
            if str(item['id']) == report_id.strip():
                found_item = item
                break
        if not found_item:
            not_found = True

    return render_template('search.html', item=found_item, not_found=not_found)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return render_template('login.html', error="Incorrect password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('admin_panel.html', items=items)

@app.route('/update_status/<int:item_id>', methods=['POST'])
def update_status(item_id):
    for item in items:
        if item['id'] == item_id:
            item['status'] = request.form['status']
    return redirect(url_for('admin_panel'))

@app.route('/update_claim/<int:item_id>', methods=['POST'])
def update_claim(item_id):
    for item in items:
        if item['id'] == item_id:
            item['claim_status'] = request.form['claim_status']
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',
    port=10000)
