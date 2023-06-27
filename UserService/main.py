import datetime
import jwt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'V9tyKP6cyAN-mc'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username, password)
    db.session.add(new_user)
    db.session.commit()

    token = generate_token(username)

    return jsonify({'message': 'User registered successfully', 'token': token}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        return jsonify({'message': 'Invalid username or password'}), 401

    token = generate_token(username)

    return jsonify({'message': 'Logged in successfully', 'token': token}), 200

@app.route('/authorize', methods=['POST'])
def authorize():
    data = request.get_json()
    token = data.get('token')

    if not verify_token(token):
        return jsonify({'message': 'Unauthorized'}), 403

    return jsonify({'message': 'Authorized'}), 200

def generate_token(username):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)

    payload = {'username': username, 'exp': expiration}

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.filter_by(username=payload['username']).first()

        if user:
            return True
        else:
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)
