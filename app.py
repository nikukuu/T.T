import threading
import time
from flask import Flask, render_template, url_for, redirect, request, session,g
import os
from flask_mysqldb import MySQL
import MySQLdb.cursors
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
    allowed_routes = ['login', 'sign_up', 'base', 'mainF', 'code']
    if 'username' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('login'))

@app.route('/')
def base():
    return render_template('base.html')

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


@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))
    
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
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return render_template('base.html')

@app.route('/groups', methods=['POST', 'GET'])
def groups():
    qr_code_url = None
    if request.method == 'POST' and request.form.get('action') == 'create_code':
        img = qrcode.make("hello world")
        base_dir = os.path.dirname(__file__)
        static_dir = os.path.join(base_dir, 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        filename = f"kyuar_{int(time.time())}.png"
        file_path = os.path.join(static_dir, filename)
        img.save(file_path)
        qr_code_url = url_for('static', filename=filename)

    return render_template('groups.html', qr_code_url=qr_code_url)


@app.route('/join', methods=['GET'])
def join(room_id, username):
    if 'username' in session and session['username'] == username:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO members (room_id, username) VALUES (%s, %s)", (room_id, username))
        mysql.connection.commit()
        cur.close()
        return render_template('room.html', message=f"User {username} has joined room {room_id}")
    else:
        return redirect(url_for('login'))

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

@app.route('/mainF')
def mainF():
    return render_template('mainF.html')

if __name__ == '__main__':
    app.run(debug=True)
