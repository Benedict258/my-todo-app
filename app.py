from flask import Flask, render_template, request, redirect

app = Flask(__name__)

file_name = "task_app.txt"

# Load tasks from the file
def load_tasks():
    try:
        with open(file_name, "r") as file:
            tasks = file.readlines()
        return [task.strip() for task in tasks]
    except FileNotFoundError:
        return []

# Save tasks to the file
def save_tasks(tasks):
    with open(file_name, "w") as file:
        for task in tasks:
            file.write(task + "\n")

# Load tasks on startup
to_do = load_tasks()

@app.route("/")
def home():
    return render_template("index.html", tasks=to_do)

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form["task"]
    if task:
        to_do.append(task)
        save_tasks(to_do)
    return redirect("/")

@app.route("/delete/<int:task_index>")
def delete_task(task_index):
    if 0 <= task_index < len(to_do):
        to_do.pop(task_index)
        save_tasks(to_do)
    return redirect("/")

if __name__ == "__main__":
    # Allow the app to run on all network interfaces (important for platforms like Heroku)
    app.run(host="0.0.0.0", port=5000)
