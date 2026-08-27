import sqlite3
import csv

def init_db(db_path='gridcare.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('admin', 'engineer', 'technician', 'customer_service'))
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS substations (
            substation_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            region TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS outages (
            outage_id INTEGER PRIMARY KEY AUTOINCREMENT,
            substation_id INTEGER NOT NULL,
            reported_by INTEGER NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'Open' CHECK (status IN ('Open', 'In Progress', 'Resolved')),
            reported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            resolved_at TEXT,
            FOREIGN KEY (substation_id) REFERENCES substations(substation_id),
            FOREIGN KEY (reported_by) REFERENCES users(user_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS work_orders (
            work_order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            outage_id INTEGER NOT NULL,
            assigned_technician INTEGER,
            scheduled_date TEXT,
            status TEXT DEFAULT 'Pending' CHECK (status IN ('Pending', 'Scheduled', 'Completed')),
            FOREIGN KEY (outage_id) REFERENCES outages(outage_id),
            FOREIGN KEY (assigned_technician) REFERENCES users(user_id)
        )
    ''')
    cur.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
                complaint_text TEXT NOT NULL,
                outage_id INTEGER ,
                reported_by INTEGER NOT NULL,
                reported_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (outage_id) REFERENCES outages(outage_id),
                FOREIGN KEY (reported_by) REFERENCES users(user_id)
            )
        ''')
    #Single query inserting 3 substations at once
    cur.execute('''
        INSERT or IGNORE INTO users (username, password_hash, role) VALUES
            ('sheryl', '0000', 'admin'),
            ('Jeremy', '0000', 'engineer'),
            ('Ekow', '0000', 'technician'),
            ('Abu', '0000', 'customer_service')
    ''')

    try:
        with open('substations.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader,None)  # Skip the header row
            for row in reader:
                if row and len(row) >= 3:  # Ensure there are enough columns    
                    sub_id=int(row[0].strip())  # Convert substation_id to integer
                    name=row[1].strip()
                    region =row[2].strip()
                    cur.execute('''
                        INSERT OR IGNORE INTO substations (substation_id, name, region) VALUES (?, ?, ?)
                    ''', (sub_id, name, region))
    except FileNotFoundError:
        print("substations.csv file not found. Please ensure the file is in the correct directory.")
    conn.commit()
    return conn

    
def add_user(username,password):
    conn = sqlite3.connect("gridcare.db")
    cursor= conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username,password_hash,role) VALUES (?,?,?)",(username,password,'customer_service'))#tell python to insert a newrow at specifc place user and pass then the ?,? are kinda placeholder values tell python to treat it as data not code then user,pass is the actual data
        conn.commit()
        return True
    except sqlite3.IntegrityError:#pops when u try to register an existing username
        return False
    finally:
        conn.close()    

def add_complaint(complaint_text, outage_id, reported_by):
    conn = sqlite3.connect("gridcare.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO complaints (complaint_text, outage_id, reported_by) VALUES (?, ?, ?)",
            (complaint_text, outage_id, reported_by)
        )
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()
        
   
        
        
#chcking for matching username and pas
# def validate_user (username,password):
#     conn = sqlite3.connect("gridcare.db")
#     cursor= conn.cursor()
    
#     cursor.execute("SELECT * FROM users, role WHERE username = ? AND password_hash = ?",(username,password))#select username and password if  they are = placeholder(?)
#     result=cursor.fetchone()
#     conn.close()
#     return result is not None#returns non if no record is found

def authenticate_user(username, password):
    """
    Checks if username and password match a user in the database.
    Returns (user_id, role) if valid, or None if invalid.
    """
    conn = sqlite3.connect("gridcare.db")
    cursor = conn.cursor()
    
    # Query for the user
    cursor.execute(
        "SELECT user_id, role FROM users WHERE username = ? AND password_hash = ?", 
        (username.strip(), password.strip())
    )
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result  # Returns tuple: (user_id, role) e.g., (1, 'admin')
    
    return None  # Login failed
#we treated this diff cus we alr had the file in the db and we just wanted to add new substations to it so we created a new function to import substations from a csv file
def import_substations(csv_path="substations.csv"):
    conn = sqlite3.connect("gridcare.db")
    cursor = conn.cursor()
    
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute(
                "INSERT OR IGNORE INTO substations (substation_id, name, region) VALUES (?, ?, ?)",
                (row['substation_id'], row['name'], row['region'])
            )
    
    conn.commit()
    conn.close()
def get_substations():
    """Fetches all substations from the database as a list of tuples (id, name, region)."""
    conn = sqlite3.connect("gridcare.db")
    cursor = conn.cursor()
    cursor.execute("SELECT substation_id, name, region FROM substations ORDER BY name ASC")
    substations = cursor.fetchall()  # Returns list of tuples: [(1, 'Achimota', 'Greater Accra'), ...]
    conn.close()
    return substations
    

def add_outage(substation_id, reported_by, description):
    conn = sqlite3.connect("gridcare.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO outages (substation_id, reported_by, description) VALUES (?, ?, ?)",
            (substation_id, reported_by, description)
        )
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()

'''what these funtion do :
- `import_substations`: Imports substation data from a CSV file into the database.
- `get_substations`: Fetches all substations from the database and returns them as a list of dictionaries.
- `add_outage`: Adds a new outage record to the database.

it also pulls 44 imported substation sorted alphabetically ba name
so engineers can select the substation from a dropdown menu in the GUI when reporting an outage.
'''

def get_open_outages():
    """Fetches open outages from the database."""
    conn = sqlite3.connect("gridcare.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.outage_id, s.name, o.description, o.status
        FROM outages o
        JOIN substations s ON o.substation_id = s.substation_id
        WHERE o.status = 'Open'
        ORDER BY o.reported_at DESC
    ''')
    open_outages = cursor.fetchall()
    conn.close()
    return open_outages

def get_technician():
    """Fetches all users with the technician role."""
    conn = sqlite3.connect("gridcare.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username FROM users WHERE role = 'technician'")
    technician = cursor.fetchall()
    conn.close()
    return technician
def assign_work_order(outage_id, technician_id,scheduled_date):
    """Assigns a work order to a technician."""
    conn=sqlite3.connect("gridcare.db")
    cursor=conn.cursor()
    try:
        #insert the technician_id into the assigned_to column of the outages table for the given outage_id
        cursor.execute('''
            INSERT INTO work_orders (outage_id, assigned_technician, scheduled_date,status)
            VALUES (?,?,?, 'Scheduled')
            
        ''', (outage_id,technician_id, scheduled_date))

        cursor.execute("UPDATE outages SET status = 'In Progress' WHERE outage_id = ?",(outage_id,))
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()

def get_technician_work_orders(technician_id):
    conn = sqlite3.connect("gridcare.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT work_order_id, outage_id, scheduled_date, status FROM work_orders WHERE assigned_technician = ?",
        (technician_id,)
    )
    result = cursor.fetchall()
    conn.close()
    return result

def mark_work_order_complete(work_order_id):
    conn = sqlite3.connect("gridcare.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE work_orders SET status = 'Completed' WHERE work_order_id = ?",
            (work_order_id,)
        )
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()




     

   

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
