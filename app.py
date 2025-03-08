from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100.0},
    {'id': 2, 'date': '2023-06-02', 'amount': -300.0},
    {'id': 3, 'date': '2023-06-03', 'amount': 800.0}
]

@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions)

@app.route('/add', methods=['GET','POST'])
def add_transaction():
    if request.method == 'POST':
        transaction = {
            'id': len(transactions)+1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transaction)
        return redirect(url_for('get_transactions'))
    
    return render_template('form.html')

@app.route('/edit/<int:transaction_id>', methods=['GET','POST'])
def edit_transaction(transaction_id):
    if not transaction_id:
        return {"message": "Invalid input"}
    
    if request.method == 'GET':
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                return render_template('edit.html', transaction = transaction)
        return {'message':'transaction not found'}
    
    if request.method == 'POST':
        #Get the request form from template
        date = request.form['date']
        amount = request.form['amount']

        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = float(amount)

                return redirect(url_for('get_transactions'))


@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)

            return redirect(url_for('get_transactions'))

@app.route('/search', methods=['GET','POST'])
def search_transactions():
    if request.method == 'POST':
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])

        filtered_transactions = [transaction for transaction in transactions if transaction['amount']>=min_amount and transaction['amount']<=max_amount]
        return render_template('transactions.html',transactions= filtered_transactions)
    
    return render_template('search.html')

@app.route('/balance')
def total_balance():
    balance = f"Total Balance: {sum([trans['amount'] for trans in transactions])}"
    return render_template('transactions.html', transactions=transactions, total_balance=balance)

if __name__ == "__main__":
    app.run(debug=True)