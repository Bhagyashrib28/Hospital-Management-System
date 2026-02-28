# from flask import Flask,render_template, request, redirect, url_for
# import sqlite3

# app = Flask(__name__)

# def get_db_connection():
#     conn = sqlite3.connect('hospital.db')
#     conn.row_factory = sqlite3.Row  # This allows accessing columns by name
#     return conn

# @app.route('/')
# def index():
#     conn = get_db_connection()
#     patients = conn.execute('SELECT id FROM patients').fetchall()
#     doctors = conn.execute('SELECT id FROM doctors').fetchall()
#     conn.close()
#     return render_template('index.html', patients=patients, doctors=doctors)

# # --- Patient Routes ---

# @app.route('/patients')
# def patients():
#     conn = get_db_connection()
#     patients = conn.execute('SELECT * FROM patients').fetchall()
#     doctors = conn.execute('SELECT name FROM doctors').fetchall()
#     conn.close()
#     return render_template('patient.html', patients=patients, doctors=doctors)

# @app.route('/add_patient', methods=['POST'])
# def add_patient():
#     name = request.form['name']
#     age = request.form['age']
#     blood_group = request.form['blood_group']
#     condition = request.form['condition']
#     doctor = request.form['doctor']
#     status = request.form['status']
#     admission_date = request.form['admission_date']

#     conn = get_db_connection()
#     conn.execute('''
#         INSERT INTO patients (name, age, blood_group, condition, doctor, status, admission_date)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#     ''', (name, age, blood_group, condition, doctor, status, admission_date))
#     conn.commit()
#     conn.close()
#     return redirect(url_for('patients'))

# # --- Doctor Routes ---

# @app.route('/doctors')
# def doctors():
#     conn = get_db_connection()
#     doctors = conn.execute('SELECT * FROM doctors').fetchall()
#     conn.close()
#     return render_template('doctor.html', doctors=doctors)

# @app.route('/add_doctor', methods=['POST'])
# def add_doctor():
#     name = request.form['name']
#     specialty = request.form['specialty']
#     availability = request.form['availability']
#     schedule = request.form['schedule']

#     conn = get_db_connection()
#     conn.execute('''
#         INSERT INTO doctors (name, specialty, availability, schedule)
#         VALUES (?, ?, ?, ?)
#     ''', (name, specialty, availability, schedule))
#     conn.commit()
#     conn.close()
#     return redirect(url_for('doctors'))

# @app.route('/delete_doctor/<int:id>', methods=['POST'])
# def delete_doctor(id):
#     conn = get_db_connection()
#     conn.execute('DELETE FROM doctors WHERE id = ?', (id,))
#     conn.commit()
#     conn.close()
#     return redirect(url_for('doctors'))

# # --- Chatbot Route ---

# @app.route('/chatbot')
# def chatbot():
#     return render_template('chatbot.html')

# if __name__ == '__main__':
#     # Initialize DB before starting
#     from database import init_db
#     init_db()
#     app.run(debug=True)



import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify
from google import genai
from dotenv import load_dotenv
import database

# Load Environment Variables (for GEMINI_API_KEY)
load_dotenv()

app = Flask(__name__)

# Initialize Gemini Client
# Ensure GEMINI_API_KEY is set in your .env file
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



def get_db_connection():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Dashboard Route ---
@app.route('/')
def index():
    conn = get_db_connection()
    patients = conn.execute('SELECT id FROM patients').fetchall()
    doctors = conn.execute('SELECT id FROM doctors').fetchall()
    conn.close()
    return render_template('index.html', patients=patients, doctors=doctors)

# --- Patient Routes ---
@app.route('/patients')
def patients():
    conn = get_db_connection()
    patients = conn.execute('SELECT * FROM patients').fetchall()
    doctors = conn.execute('SELECT name FROM doctors').fetchall()
    conn.close()
    return render_template('patient.html', patients=patients, doctors=doctors)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO patients (name, age, blood_group, condition, doctor, status, admission_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (request.form['name'], request.form['age'], request.form['blood_group'], 
          request.form['condition'], request.form['doctor'], request.form['status'], 
          request.form['admission_date']))
    conn.commit()
    conn.close()
    return redirect(url_for('patients'))

# --- Doctor Routes ---
@app.route('/doctors')
def doctors():
    conn = get_db_connection()
    doctors = conn.execute('SELECT * FROM doctors').fetchall()
    conn.close()
    return render_template('doctor.html', doctors=doctors)

# hii
@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    password = request.form.get('password')
    
    if password != "admin123":
        # Returns a simple message if the password is wrong
        return "<h3>Doctor schedule can only be changed by authorized users. Incorrect password.</h3><a href='/doctors'>Back</a>", 403

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO doctors (name, specialty, availability, schedule)
        VALUES (?, ?, ?, ?)
    ''', (request.form['name'], request.form['specialty'], 
          request.form['availability'], request.form['schedule']))
    conn.commit()
    conn.close()
    return redirect(url_for('doctors'))

@app.route('/delete_doctor/<int:id>', methods=['POST'])
def delete_doctor(id):
    password = request.form.get('password')
    
    if password != "admin123":
        return "<h3>Doctor schedule can only be changed by authorized users.</h3><a href='/doctors'>Back</a>", 403

    conn = get_db_connection()
    conn.execute('DELETE FROM doctors WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('doctors'))
# book appointment 

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        # 1. Get data from the fetch request
        name = request.form.get('name')
        email = request.form.get('email')
        department = request.form.get('department')
        date = request.form.get('date')
        notes = request.form.get('notes')

        # 2. Save to SQLite database
        try:
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO appointments (name, email, department, appointment_date, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, department, date, notes))
            conn.commit()
            conn.close()
            return jsonify({"status": "success", "message": "Appointment logged"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    # If it's a GET request (user just visiting the page)
    return render_template('book_appointment.html')

# --- Chatbot AI Routes ---
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_message = data.get("message")
    
    if not user_message:
        return jsonify({"response": "I didn't catch that. Try typing something!"}), 400

    try:
        # Generate content using Gemini 1.5 Flash
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=user_message
        )
        bot_response = response.text
        
        # Save the interaction to SQLite
        database.log_interaction(user_message, bot_response)
        
        return jsonify({"response": bot_response})
    
    except Exception as e:
        return jsonify({"response": f"Sorry, I'm having trouble connecting. Error: {str(e)}"}), 500




if __name__ == '__main__':
    database.init_db()  # Ensure database and tables exist
    app.run(debug=True)