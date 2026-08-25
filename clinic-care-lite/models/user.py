import bcrypt
import json
import re
 
class User:
    def __init__(self, user_id, name, email, password, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.role = role
        self.theme = 'dark' if role == 'clinician' else 'colorful'
 
    @staticmethod
    def validate_id(user_id, role):
        if not re.match(r'^\d{8}$', user_id):
            return False
        if role == 'clinician' and user_id[-4:] != '0000':
            return False
        if role == 'patient' and not (2022 <= int(user_id[-4:]) <= 2028):
            return False
        return True
 
    @staticmethod
    def validate_password(password):
        return (len(password) >= 8 and
                re.search(r'[A-Z]', password) and
                re.search(r'[a-z]', password) and
                re.search(r'\d', password) and
                re.search(r'[!@#$%^&*]', password))
 
    def save(self):
        with open('data/users.json', 'r+') as f:
            data = json.load(f)
            data[self.user_id] = {
                'name': self.name,
                'email': self.email,
                'password': self.password.decode('utf-8'),
                'role': self.role,
                'theme': self.theme
            }
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
