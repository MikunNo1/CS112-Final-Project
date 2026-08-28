from flask import Flask, render_template, request, session, redirect, url_for
import json
import bcrypt
import os
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
    #Clinician Dashboard Section
    if 'user_id' not in session:
        return redirect(url_for('index'))
    role = session['role']
    if role == 'clinician':
        with open('data/task_submissions.json', 'r') as f:
            submissions = json.load(f)
        return render_template('clinician_dashboard.html', name=session['name'], submissions=submissions)
        
#Patient Dashboard Section        
    with open('data/health_tasks.json', 'r') as f:
        all_tasks = json.load(f)
    my_tasks = {tid: t for tid, t in all_tasks.items() if t['patient_id'] == session['user_id']}
    with open('data/task_submissions.json', 'r') as f:
        all_subs = json.load(f)
    my_subs = {sid: s for sid, s in all_subs.items() if s['patient_id'] == session['user_id']}
    return render_template('patient_dashboard.html', name=session['name'], tasks=my_tasks, submissions=my_subs)

# Additional routes for health-task creation, submission, review, messaging, etc.

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

@app.route('/submit_task', methods=['POST'])
def submit_task():
    if 'user_id' not in session or session['role'] != 'patient':
        return redirect(url_for('index'))

    task_id = request.form['task_id']
    uploaded_file = request.files['submission_file']
    patient_id = session['user_id']

    temp_path = uploaded_file.filename
    uploaded_file.save(temp_path)

    submission = TaskSubmission(patient_id, task_id, temp_path)
    try:
        submission.save_file()
        submission.save()
    except ValueError:
        os.remove(temp_path)
        return redirect(url_for('dashboard'))

    os.remove(temp_path)
    return redirect(url_for('dashboard'))

@app.route('/review_submission', methods=['POST'])
def review_submission():
    if 'user_id' not in session or session['role'] != 'clinician':
        return redirect(url_for('index'))
    sub_id = request.form['sub_id']
    review_status = request.form['review_status']
    notes = request.form['notes']
    with open('data/task_submissions.json', 'r+') as f:
        submissions = json.load(f)
        if sub_id in submissions:
            submissions[sub_id]['review_status'] = review_status
            submissions[sub_id]['notes'] = notes
        f.seek(0)
        f.truncate()
        json.dump(submissions, f, indent=4)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)