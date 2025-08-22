from flask import Flask, render_template, request, redirect, url_for, session
from data.users import atm_users

app = Flask(__name__)
app.secret_key = "secure123"  # Needed for session handling


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form['account']
        pin = request.form['pin']
        if account in atm_users and atm_users[account]['pin'] == pin:
            session['account'] = account
            return redirect(url_for('menu'))
        else:
            return render_template('login.html', error="Invalid account or PIN")
    return render_template('login.html')


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if 'account' not in session:
        return redirect(url_for('login'))

    account = session['account']
    message = ""

    if request.method == 'POST':
        action = request.form['action']

        if action == 'balance':
            message = f"Your current balance is ₹{atm_users[account]['balance']}"

        elif action == 'deposit':
            amount = float(request.form['amount'])
            atm_users[account]['balance'] += amount
            message = f"✅ ₹{amount} deposited successfully."

        elif action == 'withdraw':
            amount = float(request.form['amount'])
            if amount <= atm_users[account]['balance']:
                atm_users[account]['balance'] -= amount
                message = f"₹{amount} withdrawn successfully."
            else:
                message = "❌ Insufficient balance."

        elif action == 'logout':
            session.pop('account', None)
            return redirect(url_for('login'))

    return render_template('menu.html', message=message, balance=atm_users[account]['balance'])


if __name__ == '__main__':
    app.run(debug=True)
