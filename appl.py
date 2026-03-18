from flask import Flask, render_template, request, redirect

app = Flask(__name__)

FILE = "tasks.txt"

def get_tasks():
    try:
        with open(FILE, "r") as f:
            tasks = f.readlines()
    except:
        tasks = []
    return tasks

def save_task(task):
    with open(FILE, "a") as f:
        f.write(task + "\n")

def delete_task(index):
    tasks = get_tasks()
    tasks.pop(index)
    with open(FILE, "w") as f:
        for task in tasks:
            f.write(task)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        task = request.form["task"]
        save_task(task)
        return redirect("/")

    tasks = get_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:index>")
def delete(index):
    delete_task(index)
    return redirect("/")

app.run(debug=True)