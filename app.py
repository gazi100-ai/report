from flask import Flask, render_template, request, redirect
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_FILE = 'deposit_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_data()
    today_str = datetime.now().strftime('%Y-%m-%d')
    yesterday_str = (datetime.now().date()).isoformat()
    report = {}

    if request.method == 'POST':
        msd = float(request.form['msd'])
        itd = float(request.form['itd'])
        mtdr = float(request.form['mtdr'])

        today_total = msd + itd + mtdr
        yesterday_total = data.get('last_total', 0)

        if today_total > yesterday_total:
            change_type = "INCREASE"
            change_amount = today_total - yesterday_total
        else:
            change_type = "DECREASE"
            change_amount = yesterday_total - today_total

        report = {
            'date': datetime.now().strftime('%d-%m-%y'),
            'branch': "Nalchity Bazar",
            'today_balance': f"{today_total:,.2f}",
            'yesterday_balance': f"{yesterday_total:,.0f}",
            'change_type': change_type,
            'change_amount': f"{change_amount:,.2f}"
        }

        data['last_total'] = today_total
        save_data(data)

    return render_template('index.html', report=report)

if __name__ == '__main__':
    app.run(debug=True)