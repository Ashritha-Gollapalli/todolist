from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)
TODO_FILE = 'todos.json'


def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f)

@app.route("/", methods=["GET", "POST"])
def index():
    todos = load_todos()  # Load from file
    
    if request.method == "POST":
        new_task = request.form.get("task")
        if new_task:
            todos.append({"task": new_task, "complete": False})
            save_todos(todos)  # Save updated list
        return redirect(url_for("index"))
    
    # Calculate completion progress
    total = len(todos)
    completed = sum(1 for todo in todos if todo["complete"])
    progress = int((completed / total) * 100) if total > 0 else 0
    
    return render_template("index.html", todos=todos, progress=progress)
@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    todos = load_todos()
    if 0 <= todo_id < len(todos):
        todos[todo_id]["complete"] = not todos[todo_id]["complete"]
        save_todos(todos)
    return redirect(url_for('index'))




@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todos = load_todos()
    if 0 <= todo_id < len(todos):
        todos.pop(todo_id)
        save_todos(todos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
