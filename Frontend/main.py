from time import sleep
import requests
import streamlit as st

USER_SERVICE_URL = 'http://localhost:5002'
TODO_SERVICE_URL = 'http://localhost:5001'

def register_user(username, password):
    url = f'{USER_SERVICE_URL}/register'
    data = {'username': username, 'password': password}

    response = requests.post(url, json=data)

    if response.status_code == 201:
        st.success('User registered successfully')
    else:
        st.error('User registration failed')

def login_user(username, password):
    url = f'{USER_SERVICE_URL}/login'
    data = {'username': username, 'password': password}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        token = response.json().get('token')
        return token
    else:
        st.error('Invalid username or password')
        return None

def create_todo(username, token, text):
    url = f'{TODO_SERVICE_URL}/todos'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    data = {'username': username, 'text': text}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        st.success('Todo created successfully')
    else:
        st.error('Failed to create todo')

def get_todos(username, token):
    url = f'{TODO_SERVICE_URL}/todos'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'username': username}

    response = requests.get(url, headers=headers, json=data)

    if response.status_code == 200:
        todos = response.json().get('todos')
        return todos
    else:
        st.error('Failed to retrieve todos')
        return []

def delete_todo(username, token, todo_id):
    url = f'{TODO_SERVICE_URL}/todos/{todo_id}'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'username': username}

    response = requests.delete(url, headers=headers, json=data)

    if response.status_code == 200:
        st.success('Todo deleted successfully')
    else:
        st.error('Failed to delete todo')

def main():
    st.title('To-Do Application')

    st.sidebar.title('User Actions')
    action = st.sidebar.selectbox('Select Action', ['Register', 'Login'])

    if action == 'Register':
        st.header('Register')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')

        if st.button('Register'):
            register_user(username, password)

    elif action == 'Login':
        st.header('Login')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')

        if st.button('Login'):
            token = login_user(username, password)

            if token:
                st.success('Login successful')

                st.sidebar.title('To-Do Actions')
                todo_action = st.sidebar.selectbox('Select Action', ['Create Todo', 'View Todos'])

                if todo_action == 'Create Todo':
                    st.header('Create Todo')
                    text = st.text_input('Todo Text')

                    create_button = st.button('Create', key='create_todo')
                    if create_button:
                        create_todo(token, text)

                elif todo_action == 'View Todos':
                    st.header('Todos')
                    todos = get_todos(token)

                    for todo in todos:
                        st.write(f'- {todo}')
                        if st.button(f'Delete Todo {todo["id"]}'):
                            delete_todo(token, todo['id'])

if __name__ == '__main__':
    main()
