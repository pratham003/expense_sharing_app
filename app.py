from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    with sqlite3.connect("expenses.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            amount REAL)''')
        conn.commit()

init_db()

# Add expense for a participant
@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.json
    name = data.get("name")
    amount = data.get("amount")

    if not name or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Invalid input. Enter a valid name and amount."}), 400

    with sqlite3.connect("expenses.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (name, amount) VALUES (?, ?)", (name, amount))
        conn.commit()

    return jsonify({"message": f"Expense of ₹{amount:.2f} added for {name}."})

# Calculate balances
@app.route("/get_balances", methods=["GET"])
def get_balances():
    with sqlite3.connect("expenses.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, SUM(amount) FROM expenses GROUP BY name")
        data = cursor.fetchall()

    if not data:
        return jsonify({"error": "No expenses recorded yet."})

    total_spent = sum(amount for _, amount in data)
    num_participants = len(data)
    per_person = total_spent / num_participants if num_participants else 0

    balances = {name: round(amount - per_person, 2) for name, amount in data}

    return jsonify(balances)

# Home route
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
