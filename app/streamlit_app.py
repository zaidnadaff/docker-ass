# from flask import Flask, request, jsonify, render_template
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# app = Flask(__name__)

# # Database configuration
# DATABASE_URL = "sqlite:///tasks.db"
# engine = create_engine(DATABASE_URL)
# Base = declarative_base()

# # Define the Task model
# class Task(Base):
#     __tablename__ = 'tasks'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(100), nullable=False)
#     description = Column(String(200))

# # Create tables
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/tasks', methods=['GET'])
# def get_tasks():
#     session = Session()
#     tasks = session.query(Task).all()
#     return jsonify([{'id': task.id, 'title': task.title, 'description': task.description} for task in tasks])

# @app.route('/tasks', methods=['POST'])
# def create_task():
#     session = Session()
#     data = request.json
#     new_task = Task(title=data['title'], description=data.get('description', ''))
#     session.add(new_task)
#     session.commit()
#     return jsonify({'id': new_task.id, 'title': new_task.title, 'description': new_task.description})

# @app.route('/tasks/<int:task_id>', methods=['PUT'])
# def update_task(task_id):
#     session = Session()
#     task = session.query(Task).get(task_id)
#     if task:
#         data = request.json
#         task.title = data.get('title', task.title)
#         task.description = data.get('description', task.description)
#         session.commit()
#         return jsonify({'id': task.id, 'title': task.title, 'description': task.description})
#     return jsonify({'error': 'Task not found'}), 404

# @app.route('/tasks/<int:task_id>', methods=['DELETE'])
# def delete_task(task_id):
#     session = Session()
#     task = session.query(Task).get(task_id)
#     if task:
#         session.delete(task)
#         session.commit()
#         return jsonify({'message': 'Task deleted'})
#     return jsonify({'error': 'Task not found'}), 404

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "sqlite:///tasks.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the Task model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(200))

# Create tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_all_tasks():
    session = Session()
    tasks = session.query(Task).all()
    session.close()
    return tasks

def add_task(title, description):
    session = Session()
    new_task = Task(title=title, description=description)
    session.add(new_task)
    session.commit()
    session.close()

def update_task(task_id, title, description):
    session = Session()
    task = session.query(Task).get(task_id)
    if task:
        task.title = title
        task.description = description
        session.commit()
    session.close()

def delete_task(task_id):
    session = Session()
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()
    session.close()

# Streamlit UI
st.title('Task Manager')

# Sidebar for adding new tasks
st.sidebar.header('Add New Task')
new_task_title = st.sidebar.text_input('Task Title')
new_task_description = st.sidebar.text_area('Task Description')
if st.sidebar.button('Add Task'):
    if new_task_title:
        add_task(new_task_title, new_task_description)
        st.sidebar.success('Task added successfully!')
    else:
        st.sidebar.error('Title is required!')

# Main content area
st.header('Tasks')

# Get all tasks
tasks = get_all_tasks()

# Display tasks in an expander
for task in tasks:
    with st.expander(f"Task: {task.title}"):
        # Create columns for the form
        col1, col2, col3 = st.columns([3, 2, 1])
        
        # Edit form
        with col1:
            edited_title = st.text_input(f'Title {task.id}', task.title)
            edited_description = st.text_area(f'Description {task.id}', task.description)
        
        # Update button
        with col2:
            if st.button(f'Update Task {task.id}'):
                update_task(task.id, edited_title, edited_description)
                st.success('Task updated!')
                st.rerun()
        
        # Delete button
        with col3:
            if st.button(f'Delete Task {task.id}', type='primary'):
                delete_task(task.id)
                st.success('Task deleted!')
                st.rerun()

# Add some CSS to make it look better
st.markdown("""
    <style>
        .stButton button {
            width: 100%;
        }
        .stExpander {
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)