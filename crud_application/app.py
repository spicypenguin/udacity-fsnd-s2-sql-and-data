from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import json
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jsinclair@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(
        db.Integer,
        db.ForeignKey('todolists.id'),
        nullable=False
    )

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list')

    def __repr__(self):
        return f'<TodoList {self.id} {self.name}>'


@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template(
        'index.html',
        data=Todo.query.filter(Todo.list_id == list_id).order_by('id').all(),
        lists=TodoList.query.all()
    )


@app.route('/todos/create', methods=['POST'])
def create_todo():
    request_data = request.get_json()
    description = request_data.get('description')
    list_id = request_data.get('list_id')

    if description and list_id:
        error = False
        body = {}
        try:
            new_todo = Todo(description=description)
            new_todo.list = TodoList.query.get(list_id)
            db.session.add(new_todo)
            db.session.commit()
            body['description'] = new_todo.description
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if not error:
            return jsonify(body)

    return abort(400)


@app.route('/todos/<todo_id>/completed', methods=['POST'])
def mark_completed(todo_id):
    request_data = request.get_json()
    completed = request_data.get('completed')

    if completed is not None:
        try:
            todo = Todo.query.get(todo_id)
            todo.completed = completed
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

        return redirect(url_for('index'))
    else:
        return abort(400)


@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    error = True
    try:
        Todo.query.filter(Todo.id == todo_id).delete()
        db.session.commit()
        error = False
    except:
        db.session.rollback()
    finally:
        db.session.close()

    if not error:
        return jsonify({})
    else:
        return abort(500)


@app.route('/lists/create', methods=['POST'])
def create_todo_list():
    request_data = request.get_json()
    name = request_data.get('name')

    if name:
        error = False
        body = {}
        try:
            new_todo_list = TodoList(name=name)
            db.session.add(new_todo_list)
            db.session.commit()
            body = {
                'id': new_todo_list.id,
                'name': new_todo_list.name
            }
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if not error:
            return jsonify(body)

    return abort(400)


@app.route('/lists/<list_id>/completed', methods=['POST'])
def mark_list_completed(list_id):
    request_data = request.get_json()
    completed = request_data.get('completed')

    if completed is not None:
        try:
            todo_list = TodoList.query.get(list_id)
            for todo in todo_list.todos:
                todo.completed = completed
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

        return redirect(url_for('index'))
    else:
        return abort(400)


if __name__ == '__main__':
    app.debug = True
    app.run()
