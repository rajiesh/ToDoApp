import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

USER_SERVICE_URL = 'http://localhost:5002'
DB_SERVICE_URL = 'http://localhost:5000'

def authorize_user(username, token):
    authorize_endpoint = f'{USER_SERVICE_URL}/authorize'
    headers = {'Content-Type': 'application/json'}
    data = {'username': username, 'token': token}

    response = requests.post(authorize_endpoint, headers=headers, json=data)

    if response.status_code == 200:
        return True
    else:
        return False

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    headers = request.headers
    print("Headers: ", headers.get('Authorization'))
    token = headers.get('Authorization').split()[1]
    todo_text = data.get('text')
    username = data.get('username')

    if not authorize_user(username, token):
        return jsonify({'message': 'Unauthorized'}), 403

    url = f'{DB_SERVICE_URL}/todos'
    data = {'user_id': username, 'text': todo_text}

    response = requests.post(url, json=data)

    if response.status_code != 201:
        return jsonify({'message': 'Failed to create ToDo in DB'}), 500

    return jsonify({'message': 'Todo created successfully'}), 201


@app.route('/todos', methods=['GET'])
def get_todos():
    username = request.args.get('username')
    token = request.args.get('token')

    if not authorize_user(username, token):
        return jsonify({'message': 'Unauthorized'}), 403

    url = f'{DB_SERVICE_URL}/todos/{username}'

    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'message': 'Failed to create ToDo in DB'}), 500

    return jsonify(response.content), 200

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    username = request.args.get('username')
    token = request.args.get('token')

    if not authorize_user(username, token):
        return jsonify({'message': 'Unauthorized'}), 403

    url = f'{DB_SERVICE_URL}/todos/{todo_id}'

    response = requests.delete(url)

    if response.status_code != 200:
        return jsonify({'message': 'Failed to Delete ToDo in DB'}), 500

    return jsonify({'message': 'Todo deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
