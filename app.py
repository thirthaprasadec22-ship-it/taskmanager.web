from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("tasks.db")

def create_table():
    conn = get_db()
    conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, done INTEGER)")
    conn.close()

create_table()

@app.route("/", methods=["GET","POST"])
def index():
    conn = get_db()

    if request.method == "POST":
        task = request.form["task"]
        conn.execute("INSERT INTO tasks (task, done) VALUES (?,0)",(task,))
        conn.commit()

    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/done/<int:id>")
def done(id):
    conn = get_db()
    conn.execute("UPDATE tasks SET done=1 WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect("/")

app.run(debug=True)