from flask import Flask, render_template, url_for, redirect, request, session,g
import os
from flask_mysqldb import MySQL
import MySQLdb.cursors
import threading
import time
import qrcode
import cv2
import webbrowser

app = Flask(__name__)
app.secret_key = 'uwu'

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "splitshare"

mysql = MySQL(app)

@app.before_request
def require_login():
    allowed_routes = ['login', 'sign_up', 'base', 'mainF', 'code', 'room']
    if 'username' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('login'))

#main
@app.route('/')
def base():
    return render_template('base.html')

#login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT username, password FROM register WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user is None:
            return render_template('base.html', error='User does not exist')
        elif password == user [1]:
            session['username'] = user[0]
            return redirect(url_for('home'))
        else:
            return render_template('base.html', error='Invalid or wrong password')
    return render_template('base.html')

#sign up
@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO register (email, username, password) VALUES (%s, %s, %s)", (email, username, password))

        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('sign_up.html')

#dashboard
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

#user profile    
@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT email, username FROM register WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        
        if user:
            return render_template('profile.html', user=user)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

#logout    
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return render_template('base.html')

# qr generator and main function
@app.route('/groups', methods=['POST', 'GET'])
def groups():
    qr_code_url = None
    if request.method == 'POST' and request.form.get('action') == 'create_group':
        if 'username' in session:
            username = session['username']
            group_name = request.form['group_name']
            room_id = int(time.time())

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO rooms (room_id, group_name, username) VALUES (%s, %s, %s)", (room_id, group_name, username))
            mysql.connection.commit()
            cur.close()

            session['room_id'] = room_id

            join_url = url_for('join', room_id=room_id, _external=True)
            img = qrcode.make(join_url)
            base_dir = os.path.dirname(__file__)
            static_dir = os.path.join(base_dir, 'static')

            if not os.path.exists(static_dir):
                os.makedirs(static_dir)
            
            filename = f"kyuar_{room_id}.png"
            file_path = os.path.join(static_dir, filename)
            
            img.save(file_path)
            
            qr_code_url = url_for('static', filename=filename)

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO members (room_id, username) VALUES (%s, %s)", (room_id, username))
            mysql.connection.commit()
            cur.close()
            
    return render_template('groups.html', qr_code_url=qr_code_url)

#join a room
@app.route('/join/<int:room_id>', methods=['GET'])
def join(room_id):
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cur.execute("SELECT * FROM members WHERE room_id = %s AND username = %s", (room_id, username))
        member = cur.fetchone()
        if not member:
            cur.execute("INSERT INTO members (room_id, username) VALUES (%s, %s)", (room_id, username))
            mysql.connection.commit()

        cur.execute("SELECT * FROM expenses WHERE room_id = %s", (room_id,))
        expenses = cur.fetchall()

        cur.execute("SELECT username FROM members WHERE room_id = %s", (room_id,))
        members = cur.fetchall()

        cur.close()

        debts = []
        for expense in expenses:
            split_amount = expense['amount'] / len(members)
            for member in members:
                if member['username'] != expense['paid_by']:
                    debts.append({
                        'description': expense['description'],
                        'amount': expense['amount'],
                        'paid_by': expense['paid_by'],
                        'borrower': member['username'],
                        'split_amount': split_amount
                    })

        has_expenses = len(expenses) > 0
        
        return render_template('room.html', room_id=room_id, debts=debts, expenses=expenses, has_expenses=has_expenses, members=members)
    else:
        return redirect(url_for('login'))

#qr scanner
@app.route('/code')
def code():
    def open_qr_scanner():
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print("Error: Could not open video device")
            return

        detector = cv2.QRCodeDetector()
        while True:
            success, img = cap.read()
            if not success:
                print("Failed to capture frame")
                continue

            data, bbox, _ = detector.detectAndDecode(img)
            if data:
                webbrowser.open(data)
                break

            cv2.imshow('qr scanner', img)
            if cv2.waitKey(1) == ord('c'):
                break

        cap.release()
        cv2.destroyAllWindows()

    threading.Thread(target=open_qr_scanner).start()
    return render_template('code.html')

#main function
@app.route('/mainF')
def mainF():
    if 'username' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cur.execute("SELECT room_id FROM rooms ORDER BY room_id DESC LIMIT 1")
        room = cur.fetchone()
        
        if room:
            room_id = room['room_id']
            session['room_id'] = room_id

            cur.execute("SELECT username FROM members WHERE room_id = %s", (room_id,))
            members = cur.fetchall()
        else:
            room_id = None
            members = []
        
        cur.close()
        
        success = request.args.get('success', None)
        
        return render_template('mainF.html', room_id=room_id, members=members, success=success)
    else:
        return redirect(url_for('login'))

#calculation
@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'username' in session:
        description = request.form['description']
        expense = float(request.form['expense'])
        paid_by = request.form['paid_by']
        room_id = session.get('room_id')

        if room_id:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cur.execute("INSERT INTO expenses (room_id, description, amount, paid_by) VALUES (%s, %s, %s, %s)", (room_id, description, expense, paid_by))

            cur.execute("SELECT username FROM members WHERE room_id = %s", (room_id,))
            members = cur.fetchall()
            
            num_members = len(members)
            split_amount = expense / num_members

            for member in members:
                borrower = member['username']
                if borrower != paid_by:
                    
                    cur.execute("SELECT COUNT(*) FROM debts WHERE room_id = %s AND lender = %s AND borrower = %s", (room_id, paid_by, borrower))
                    exists = cur.fetchone()['COUNT(*)']

                    if not exists:
                        cur.execute("INSERT INTO debts (room_id, lender, borrower, amount) VALUES (%s, %s, %s, %s)", (room_id, paid_by, borrower, split_amount))

            mysql.connection.commit()
            cur.close()

            return redirect(url_for('mainF', success=True))
        else:
            return redirect(url_for('mainF', success=False))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
