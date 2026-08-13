import sqlite3

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
    #Single query inserting 3 substations at once
    cur.execute('''
        INSERT INTO users (username, password_hash, role) VALUES
            ('kofi', 'adminpass', 'admin'),
            ('ama', 'engineerpass', 'engineer'),
            ('papa yaw', 'technicianpass', 'technician'),
            ('victor', 'customerpass', 'customer_service')
    ''')
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


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")