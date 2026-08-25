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
        return redirect(url_for('dashboard'))
    return render_template('login.html', error='Invalid credentials')
 
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    role = session['role']
    if role == 'clinician':
        return render_template('clinician_dashboard.html')
    return render_template('patient_dashboard.html')
 
# Additional routes for health-task creation, submission, review, messaging, etc.
if __name__ == '__main__':
    app.run(debug=True)