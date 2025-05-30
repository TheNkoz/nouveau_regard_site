from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reponses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                age INTEGER,
                quartier TEXT,
                avis TEXT
            )
        """)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')

@app.route('/resultats')
def resultats():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute("SELECT quartier, COUNT(*) FROM reponses GROUP BY quartier")
        data = cursor.fetchall()
    return render_template('resultats.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    nom = request.form['nom']
    age = request.form['age']
    quartier = request.form['quartier']
    avis = request.form['avis']
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("INSERT INTO reponses (nom, age, quartier, avis) VALUES (?, ?, ?, ?)",
                     (nom, age, quartier, avis))
    return redirect('/resultats')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

