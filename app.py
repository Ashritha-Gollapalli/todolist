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

@app.route('/', methods=['GET', 'POST'])
def index():
    todos = load_todos()
    if request.method == 'POST':
        new_todo = request.form.get('todo')
        if new_todo:
            todos.append(new_todo)
            save_todos(todos)
        return redirect(url_for('index'))
    return render_template('index.html', todos=todos)

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todos = load_todos()
    if 0 <= todo_id < len(todos):
        todos.pop(todo_id)
        save_todos(todos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
