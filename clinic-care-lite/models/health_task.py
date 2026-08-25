import json
from datetime import datetime
 
class HealthTask:
    def __init__(self, task_id, title, description, due_date, clinic_id):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.clinic_id = clinic_id
 
    def save(self):
        with open('data/health_tasks.json', 'r+') as f:
            data = json.load(f)
            data[self.task_id] = {
                'title': self.title,
                'description': self.description,
                'due_date': self.due_date,
                'clinic_id': self.clinic_id
            }
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
