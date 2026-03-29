from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import csv
import io
import json

app = Flask(__name__)

# Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'  # Change this to your MySQL password
app.config['MYSQL_DB'] = 'dms_db'
app.config['SECRET_KEY'] = 'your_secret_key_change_me'

mysql = MySQL(app)

# Decorator for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, username, password FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - DMS</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .login-container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }
            .login-container h1 { color: #333; margin-bottom: 30px; text-align: center; font-size: 28px; }
            .form-group { margin-bottom: 20px; }
            .form-group label { display: block; margin-bottom: 8px; color: #555; font-weight: 500; }
            .form-group input { width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 5px; font-size: 14px; transition: border-color 0.3s; }
            .form-group input:focus { outline: none; border-color: #667eea; }
            .btn { width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 5px; font-size: 16px; font-weight: 600; cursor: pointer; transition: background 0.3s; }
            .btn:hover { background: #764ba2; }
            .error { color: #e74c3c; font-size: 14px; margin-top: 10px; text-align: center; }
            .success { color: #27ae60; font-size: 14px; margin-top: 10px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>📊 DMS Login</h1>
            <form id="loginForm">
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" id="username" required placeholder="Enter username">
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" id="password" required placeholder="Enter password">
                </div>
                <button type="submit" class="btn">Login</button>
                <div id="message"></div>
            </form>
        </div>
        <script>
            document.getElementById('loginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                const messageEl = document.getElementById('message');
                
                try {
                    const response = await fetch('/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, password })
                    });
                    
                    if (response.ok) {
                        messageEl.innerHTML = '<div class="success">Login successful! Redirecting...</div>';
                        setTimeout(() => window.location.href = '/dashboard', 1000);
                    } else {
                        const data = await response.json();
                        messageEl.innerHTML = '<div class="error">' + data.message + '</div>';
                    }
                } catch (error) {
                    messageEl.innerHTML = '<div class="error">Connection error</div>';
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ==================== DASHBOARD & VIEWS ====================

@app.route('/dashboard')
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) FROM students')
    total_students = cursor.fetchone()[0]
    
    cursor.execute('SELECT AVG(gpa) FROM students')
    avg_gpa = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM students WHERE enrollment_date > DATE_SUB(NOW(), INTERVAL 30 DAY)')
    new_students = cursor.fetchone()[0]
    
    cursor.close()
    
    return render_template('dashboard.html', 
                         total_students=total_students,
                         avg_gpa=round(avg_gpa, 2) if avg_gpa else 0,
                         new_students=new_students,
                         username=session['username'])

# ==================== CRUD API ROUTES ====================

@app.route('/api/students', methods=['GET'])
@login_required
def get_students():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    department = request.args.get('department', '')
    limit = 10
    offset = (page - 1) * limit
    
    cursor = mysql.connection.cursor()
    
    # Build query
    query = 'SELECT * FROM students WHERE 1=1'
    params = []
    
    if search:
        query += ' AND (student_name LIKE %s OR email LIKE %s OR roll_number LIKE %s)'
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
    
    if department:
        query += ' AND department = %s'
        params.append(department)
    
    # Get total count
    count_query = 'SELECT COUNT(*) FROM students WHERE 1=1'
    if search:
        count_query += ' AND (student_name LIKE %s OR email LIKE %s OR roll_number LIKE %s)'
    if department:
        count_query += ' AND department = %s'
    
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    query += ' ORDER BY id DESC LIMIT %s OFFSET %s'
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    students = cursor.fetchall()
    cursor.close()
    
    students_list = []
    for student in students:
        students_list.append({
            'id': student[0],
            'roll_number': student[1],
            'student_name': student[2],
            'email': student[3],
            'phone': student[4],
            'department': student[5],
            'gpa': float(student[6]),
            'enrollment_date': student[7].strftime('%Y-%m-%d') if student[7] else ''
        })
    
    return jsonify({
        'students': students_list,
        'total': total,
        'page': page,
        'pages': (total + limit - 1) // limit
    })

@app.route('/api/students', methods=['POST'])
@login_required
def create_student():
    data = request.get_json()
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO students (roll_number, student_name, email, phone, department, gpa, enrollment_date)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        ''', (data['roll_number'], data['student_name'], data['email'], data['phone'], data['department'], data['gpa']))
        
        mysql.connection.commit()
        cursor.close()
        return jsonify({'status': 'success', 'message': 'Student added successfully'}), 201
    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/students/<int:student_id>', methods=['PUT'])
@login_required
def update_student(student_id):
    data = request.get_json()
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''
            UPDATE students 
            SET student_name = %s, email = %s, phone = %s, department = %s, gpa = %s
            WHERE id = %s
        ''', (data['student_name'], data['email'], data['phone'], data['department'], data['gpa'], student_id))
        
        mysql.connection.commit()
        cursor.close()
        return jsonify({'status': 'success', 'message': 'Student updated successfully'})
    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
@login_required
def delete_student(student_id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('DELETE FROM students WHERE id = %s', (student_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'status': 'success', 'message': 'Student deleted successfully'})
    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return jsonify({'status': 'error', 'message': str(e)}), 400

# ==================== EXPORT ROUTE ====================

@app.route('/api/export', methods=['GET'])
@login_required
def export_data():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM students ORDER BY id DESC')
    students = cursor.fetchall()
    cursor.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Roll Number', 'Name', 'Email', 'Phone', 'Department', 'GPA', 'Enrollment Date'])
    
    for student in students:
        writer.writerow(student)
    
    output.seek(0)
    return output.getvalue(), 200, {
        'Content-Disposition': 'attachment; filename=students_export.csv',
        'Content-Type': 'text/csv'
    }

# ==================== ANALYTICS ROUTE ====================

@app.route('/api/analytics')
@login_required
def get_analytics():
    cursor = mysql.connection.cursor()
    
    # Department-wise count
    cursor.execute('SELECT department, COUNT(*) as count FROM students GROUP BY department')
    dept_data = cursor.fetchall()
    
    # GPA distribution
    cursor.execute('''
        SELECT 
            CASE 
                WHEN gpa >= 3.5 THEN 'A (3.5+)'
                WHEN gpa >= 3.0 THEN 'B (3.0-3.4)'
                WHEN gpa >= 2.5 THEN 'C (2.5-2.9)'
                ELSE 'D (<2.5)'
            END as grade,
            COUNT(*) as count
        FROM students
        GROUP BY grade
        ORDER BY gpa DESC
    ''')
    gpa_data = cursor.fetchall()
    
    cursor.close()
    
    return jsonify({
        'departments': {item[0]: item[1] for item in dept_data},
        'gpa_distribution': {item[0]: item[1] for item in gpa_data}
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
