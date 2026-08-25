import os
import shutil
from datetime import datetime
import json
 
class TaskSubmission:
    def __init__(self, patient_id, task_id, file_path):
        self.patient_id = patient_id
        self.task_id = task_id
        self.file_path = file_path
        self.timestamp = datetime.now().isoformat()
        self.review_status = 'Pending'   # Pending / Reviewed - Normal / Needs Follow-up / Escalated
        self.notes = None
 
    def validate_file(self):
        return self.file_path.endswith(('.txt', '.csv', '.pdf'))
 
    def save_file(self):
        if not self.validate_file():
            raise ValueError('Only .txt, .csv, and .pdf files are allowed')
        ext = os.path.splitext(self.file_path)[1]
        dest_path = f'submissions/{self.patient_id}/{self.task_id}{ext}'
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy(self.file_path, dest_path)
        self.file_path = dest_path
 
    def save(self):
        with open('data/task_submissions.json', 'r+') as f:
            data = json.load(f)
            data[f'{self.patient_id}_{self.task_id}'] = {
                'patient_id': self.patient_id,
                'task_id': self.task_id,
                'file_path': self.file_path,
                'timestamp': self.timestamp,
                'review_status': self.review_status,
                'notes': self.notes
            }
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
