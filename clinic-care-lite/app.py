from flask import Flask, render_template, request, session, redirect, url_for
import json
import bcrypt
from models.user import User
from models.health_task import HealthTask
from models.task_submission import TaskSubmission
from utils.email_handler import send_email
 
app = Flask(__name__)
app.secret_key = 'your-secret-key'
 
@app.route('/')
def index():
    return render_template('login.html')
 
@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    password = request.form['password']
    with open('data/users.json', 'r') as f:
        users = json.load(f)
    if user_id in users and bcrypt.checkpw(password.encode('utf-8'), users[user_id]['password'].encode('utf-8')):
        session['user_id'] = user_id
        session['role'] = users[user_id]['role']
        session['name'] = users[user_id]['name']
        return redirect(url_for('dashboard'))
    return render_template('login.html', error='Invalid credentials')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':    
        name = request.form['name']
        email = request.form['email']
        user_id = request.form['user_id']
        password = request.form['password']
        role = request.form['role']
        if User.validate_id(user_id, role) and User.validate_password(password):
            new_user = User(user_id, name, email, password, role)
            new_user.save()
            return redirect(url_for('index'))
        return render_template('register.html', error='Invalid ID or password format')
    return render_template('register.html')
            
 
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    role = session['role']
    if role == 'clinician':
        return render_template('clinician_dashboard.html', name=session['name'])
    return render_template('patient_dashboard.html', name=session['name'])

@app.route('/create_task', methods=['POST'])
def create_task():
    if 'user_id' not in session or session['role'] != 'clinician':
        return redirect(url_for('index'))
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']
    patient_id = request.form['patient_id']
    with open('data/users.json', 'r') as f:
        users = json.load(f)
    if patient_id not in users or users[patient_id]['role'] != 'patient':
        return redirect(url_for('dashboard'))
    clinic_id = session['user_id']
    with open('data/health_tasks.json', 'r') as f:
        existing_tasks = json.load(f)
    task_id = str(len(existing_tasks) + 1)
    new_task = HealthTask(task_id, title, description, due_date, clinic_id, patient_id)
    new_task.save()
    return redirect(url_for('dashboard'))


# Additional routes for health-task creation, submission, review, messaging, etc.
if __name__ == '__main__':
    app.run(debug=True)