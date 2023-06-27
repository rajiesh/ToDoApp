from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'  # Change the database URI as per your setup
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(200), nullable=False)

    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    user_id = data.get('user_id')
    text = data.get('text')

    new_todo = Todo(user_id, text)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message': 'Todo created successfully'}), 201

@app.route('/todos/<user_id>', methods=['GET'])
def get_todo(user_id):
    todo = Todo.query.get(user_id)

    if not todo:
        return jsonify({'message': 'Todo not found'}), 404

    return jsonify({'id': todo.id, 'user_id': todo.user_id, 'text': todo.text}), 200

@app.route('/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    text = data.get('text')

    todo = Todo.query.get(todo_id)

    if not todo:
        return jsonify({'message': 'Todo not found'}), 404

    todo.text = text
    db.session.commit()

    return jsonify({'message': 'Todo updated successfully'}), 200

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)

    if not todo:
        return jsonify({'message': 'Todo not found'}), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': 'Todo deleted successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
