import sqlite3
import bcrypt

DB_NAME = "hello.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # Create predictions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            input_data TEXT,
            predicted_diseases TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def add_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        return False  # Email already exists

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
    
    conn.commit()
    conn.close()
    return True

def authenticate_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    conn.close()

    if user and bcrypt.checkpw(password.encode(), user[0]):
        return True
    return False

def save_prediction(email, input_data, predicted_diseases):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Ensure predicted_diseases is a list
    if isinstance(predicted_diseases, str):
        predicted_diseases = [predicted_diseases]

    cursor.execute("""
        INSERT INTO predictions (email, input_data, predicted_diseases)
        VALUES (?, ?, ?)
    """, (email, str(input_data), ", ".join(predicted_diseases)))

    conn.commit()
    conn.close()

def get_user_predictions(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT input_data, predicted_diseases, timestamp FROM predictions
        WHERE email = ?
    """, (email,))
    rows = cursor.fetchall()
    conn.close()

    # Debugging: print the rows to see their structure
    print("Rows:", rows)

    predictions = []
    for row in rows:
        input_data, predicted_diseases, timestamp = row  # Unpacking each tuple correctly
        predictions.append({"input_data": input_data, "predicted_diseases": predicted_diseases, "timestamp": timestamp})
    
    return predictions

