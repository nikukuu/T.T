from flask import Flask, flash, render_template, url_for, redirect, request, session
import os
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_mysqldb import MySQL
import MySQLdb.cursors
import threading
import time
import qrcode
import cv2
import webbrowser
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'uwuwers'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max size
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'splitshare'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

mysql = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    connection = MySQLdb.connect(
        host='localhost',
        user='root',
        password='',
        database='splitshare'
    )
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    connection.close()
    
    if user:
        return User(user_id)
    else:
        return None

@login_manager.user_loader
def load_user(username):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT username FROM register WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(username)
    return None

@app.before_request
def require_login():
    allowed_routes = ['login', 'sign_up', 'base', 'home', 'mainF', 'code', 'room', 'homepage', 'about']
    if 'username' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('homepage'))

#main
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/about')
def about():
    return render_template('Aboutus.html')

@app.route('/base')
def base():
    return render_template('base.html')

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    success_message = request.args.get('success')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT username, password FROM register WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user is None:
            return render_template('base.html', error='User does not exist')
        elif password == user[1]:
            session['username'] = username  # Set session username
            user_obj = User(username)  # Create User object
            login_user(user_obj)  # Use Flask-Login to log in
            return redirect(url_for('home'))
        else:
            return render_template('base.html', error='Invalid password')

    return render_template('base.html', success=success_message)

#sign up
@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM register WHERE username = %s", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            return render_template('sign_up.html', error='Username already exists. Please choose a different username.')

        cur.execute("INSERT INTO register (email, username, password) VALUES (%s, %s, %s)", (email, username, password))
        mysql.connection.commit()
        cur.close()

        # Redirect to login page with success message
        return redirect(url_for('login', success='Your account has been created. You can now log in.'))
    return render_template('sign_up.html')

#dashboard
@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Get the overall amount the user owes
        cur.execute("""
            SELECT SUM(amount) as total_owed
            FROM debts
            WHERE borrower = %s
        """, (username,))
        total_owed = cur.fetchone()['total_owed'] or 0

        # Get the list of users who owe the logged-in user
        cur.execute("""
            SELECT borrower, SUM(amount) as total_amount
            FROM debts
            WHERE lender = %s
            GROUP BY borrower
        """, (username,))
        borrowers = cur.fetchall()

        cur.close()

        return render_template('home.html', username=username, total_owed=total_owed, borrowers=borrowers)
    else:
        return redirect(url_for('login'))

#user profile    
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    username = current_user.id  # Get the current logged-in user's username
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT email, username FROM register WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user:
        if request.method == 'POST' and 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{username}.{file.filename.rsplit('.', 1)[1].lower()}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                user['photo'] = url_for('static', filename=f'uploads/{filename}')
        
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))

#logout    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('homepage.html')

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
            cur.execute("""
                INSERT INTO rooms (room_id, group_name, creator, username, created_at)
                VALUES (%s, %s, %s, %s, NOW())
            """, (room_id, group_name, username, username))
            mysql.connection.commit()

            # Log activity
            activity_message = f"created a group named '{group_name} (room_id: {room_id})"
            cur.execute("""
                    INSERT INTO activity_logs (username, activity, room_id)
                    VALUES (%s, %s, %s)
            """, (username, activity_message, room_id))

            mysql.connection.commit()
            cur.close()

            session['room_id'] = room_id

            join_url = url_for('join', room_id=room_id, _external=True)
            img = qrcode.make(join_url)
            base_dir = os.path.dirname(__file__)
            qr_dir = os.path.join(base_dir, 'static', 'qr')

            if not os.path.exists(qr_dir):
                os.makedirs(qr_dir)
            
            filename = f"kyuar_{room_id}.png"
            file_path = os.path.join(qr_dir, filename)
            
            img.save(file_path)
            
            qr_code_url = url_for('static', filename=f'qr/{filename}')

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

        # Get the group name before the conditional block
        cur.execute("SELECT group_name FROM rooms WHERE room_id = %s", (room_id,))
        group = cur.fetchone()
        group_name = group['group_name'] if group else 'Unknown'

        # Check if the user is already a member
        cur.execute("SELECT * FROM members WHERE room_id = %s AND username = %s", (room_id, username))
        member = cur.fetchone()
        if not member:
            # Add user to the members table
            cur.execute("INSERT INTO members (room_id, username) VALUES (%s, %s)", (room_id, username))
            mysql.connection.commit()

            # Recalculate debts for new member
            cur.execute("SELECT * FROM expenses WHERE room_id = %s", (room_id,))
            expenses = cur.fetchall()

            cur.execute("SELECT username FROM members WHERE room_id = %s", (room_id,))
            members = cur.fetchall()

            num_members = len(members)
            for expense in expenses:
                split_amount = expense['amount'] / num_members
                for member in members:
                    borrower = member['username']
                    if borrower != expense['paid_by']:
                        cur.execute("INSERT INTO debts (room_id, lender, borrower, amount) VALUES (%s, %s, %s, %s)",
                                    (room_id, expense['paid_by'], borrower, split_amount))

            mysql.connection.commit()

        # Fetch the expenses and members for rendering
        cur.execute("SELECT * FROM expenses WHERE room_id = %s", (room_id,))
        expenses = cur.fetchall()

        cur.execute("SELECT username FROM members WHERE room_id = %s", (room_id,))
        members = cur.fetchall()

        # Log the activity
        cur.execute("""
            INSERT INTO activity_logs (username, activity, room_id)
            VALUES (%s, %s, %s)
        """, (username, f"{username} joined the group {group_name} (room_id {room_id})", room_id))
        mysql.connection.commit()

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

        return render_template('room.html', room_id=room_id, debts=debts, expenses=expenses, has_expenses=has_expenses, members=members, group_name=group_name)
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
@app.route('/mainF/<int:room_id>', methods=['GET'])
@login_required
def mainF(room_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Get room information
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM rooms WHERE room_id = %s", (room_id,))
    room_info = cur.fetchone()
    if not room_info:
        return "Room not found", 404

    # Get members
    cur.execute("SELECT username FROM members WHERE room_id = %s", (room_id,))
    members = cur.fetchall()

    # Get expenses
    cur.execute("SELECT * FROM expenses WHERE room_id = %s", (room_id,))
    expenses = cur.fetchall()
    has_expenses = len(expenses) > 0

    cur.close()

    success = request.args.get('success', None)

    return render_template('mainF.html', room_id=room_id, members=members, expenses=expenses,
                           has_expenses=has_expenses, username=username, room_info=room_info, success=success)

#calculation
@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'username' in session:
        description = request.form['description']
        expense = float(request.form['expense'])
        paid_by = request.form['paid_by']
        room_id = request.form['room_id']  # Retrieve room_id from the form
        username = session.get('username')

        if room_id:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Insert the expense with the current timestamp
            cur.execute("""
                INSERT INTO expenses (room_id, description, amount, paid_by, created_at)
                VALUES (%s, %s, %s, %s, NOW())
            """, (room_id, description, expense, paid_by))
            mysql.connection.commit()

            # Delete existing debts related to this expense (modify as necessary)
            cur.execute("DELETE FROM debts WHERE room_id = %s AND lender = %s", (room_id, paid_by))
            mysql.connection.commit()

            # Recalculate debts
            cur.execute("SELECT username FROM members WHERE room_id = %s", (room_id,))
            members = cur.fetchall()
            num_members = len(members)
            split_amount = expense / num_members

            for member in members:
                borrower = member['username']
                if borrower != paid_by:
                    cur.execute("""
                        INSERT INTO debts (room_id, lender, borrower, amount, description)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (room_id, paid_by, borrower, split_amount, description))
            
            cur.execute("SELECT group_name FROM rooms WHERE room_id = %s", (room_id,))
            group = cur.fetchone()
            group_name = group['group_name'] if group else 'Unknown'

            mysql.connection.commit()

            # Log the activity
            cur.execute("""
                INSERT INTO activity_logs (username, activity, room_id, activity_time)
                VALUES (%s, %s, %s, NOW())
            """, (username, f"You added an expense of ₱{expense} for {description} in group {group_name} (room_id {room_id})", room_id))
            mysql.connection.commit()
            
            cur.close()

            return redirect(url_for('mainF', room_id=room_id, success='True'))
        else:
            return redirect(url_for('mainF', room_id=room_id, success='False'))
    else:
        return redirect(url_for('login'))
    
# Groups and expenses
@app.route('/groups_expenses')
def groups_expenses():
    if 'username' in session:
        username = session['username']
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Fetch active rooms the user is part of
        cur.execute("""
            SELECT rooms.room_id, rooms.group_name, rooms.creator, rooms.created_at, rooms.is_active, rooms.ended_at
            FROM rooms 
            JOIN members ON rooms.room_id = members.room_id 
            WHERE members.username = %s AND rooms.is_active = 1
            ORDER BY rooms.created_at DESC
        """, (username,))
        rooms = cur.fetchall()

        rooms_dict = {room['room_id']: room for room in rooms}
        
        # Fetch expenses for the rooms
        expenses_dict = {}
        for room_id in rooms_dict:
            cur.execute("""
                SELECT id, description, amount, paid_by, created_at 
                FROM expenses 
                WHERE room_id = %s
            """, (room_id,))
            expenses_dict[room_id] = cur.fetchall()
        
        # Fetch members for the rooms
        members_dict = {}
        for room_id in rooms_dict:
            cur.execute("""
                SELECT username 
                FROM members 
                WHERE room_id = %s
            """, (room_id,))
            members = cur.fetchall()
            members_dict[room_id] = [member['username'] for member in members]
        
        cur.close()
        
        return render_template('groups_expenses.html', username=username, rooms_dict=rooms_dict, expenses_dict=expenses_dict, members_dict=members_dict)
    else:
        return redirect(url_for('login'))

#edit expense
@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if request.method == 'POST':
            description = request.form['description']
            amount = float(request.form['amount'])
            paid_by = request.form['paid_by']

            # Update the expense in the database
            cur.execute("""
                UPDATE expenses 
                SET description = %s, amount = %s, paid_by = %s 
                WHERE id = %s
            """, (description, amount, paid_by, expense_id))
            mysql.connection.commit()

            # Recalculate debts
            cur.execute("SELECT room_id FROM expenses WHERE id = %s", (expense_id,))
            room_id = cur.fetchone()['room_id']

            cur.execute("DELETE FROM debts WHERE room_id = %s AND description = %s", (room_id, description))
            mysql.connection.commit()

            cur.execute("SELECT username FROM members WHERE room_id = %s", (room_id,))
            members = cur.fetchall()
            num_members = len(members)
            split_amount = amount / num_members

            for member in members:
                borrower = member['username']
                if borrower != paid_by:
                    cur.execute("""
                        INSERT INTO debts (room_id, lender, borrower, amount, description)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (room_id, paid_by, borrower, split_amount, description))
            
            # Log the activity
            room_info = get_room_info(room_id)
            cur.execute("""
                INSERT INTO activity_logs (username, activity, room_id)
                VALUES (%s, %s, %s)
            """, (username, f"{username} edited the expense {description} in group {room_info['group_name']}", room_id))

            mysql.connection.commit()
            cur.close()

            return redirect(url_for('groups_expenses'))
        else:
            cur.execute("SELECT * FROM expenses WHERE id = %s", (expense_id,))
            expense = cur.fetchone()

            cur.execute("SELECT username FROM members WHERE room_id = %s", (expense['room_id'],))
            members = cur.fetchall()
            cur.close()

            return render_template('edit_expense.html', expense=expense, members=members)
    else:
        return redirect(url_for('login'))

@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    if 'username' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Retrieve the necessary details from the expense
        cur.execute("SELECT room_id, paid_by, amount, description FROM expenses WHERE id = %s", (expense_id,))
        expense = cur.fetchone()
        
        if expense:
            room_id = expense['room_id']
            paid_by = expense['paid_by']
            amount = expense['amount']
            description = expense['description']

            # Delete the expense
            cur.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
            mysql.connection.commit()

            # Delete related debts
            cur.execute("DELETE FROM debts WHERE room_id = %s AND lender = %s AND amount = %s", (room_id, paid_by, amount))
            mysql.connection.commit()
            
            # Log the activity
            username = session['username']
            room_info = get_room_info(room_id)
            cur.execute("""
                INSERT INTO activity_logs (username, activity, room_id)
                VALUES (%s, %s, %s)
            """, (username, f"{username} deleted the expense {description} in group {room_info['group_name']}", room_id))

            mysql.connection.commit()

            cur.close()

        return redirect(url_for('groups_expenses'))
    else:
        return redirect(url_for('login'))

@app.route('/settle_up/<int:room_id>', methods=['GET', 'POST'])
@login_required
def settle_up(room_id):
    username = session['username']
    room_info = get_room_info(room_id)
    
    # Ensure the user is the creator of the room
    if username != room_info['creator']:
        return "Access Denied", 403

    if request.method == 'POST':
        payer = request.form['payer']
        recipient = request.form['recipient']
        amount = float(request.form['amount'])
        date = request.form['date']
        payment_method = request.form['payment_method']

        cur = mysql.connection.cursor()
        try:
            # Insert settlement record
            cur.execute("""
                INSERT INTO settlements (room_id, payer, recipient, amount, date, payment_method)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (room_id, payer, recipient, amount, date, payment_method))

            # Commit the transaction
            mysql.connection.commit()

            # Log the activity
            cur.execute("""
                INSERT INTO activity_logs (username, activity, room_id)
                VALUES (%s, %s, %s)
            """, (username, f"{username} recorded a payment from {payer} to {recipient} in group {room_info['group_name']}", room_id))

            # Commit the activity log
            mysql.connection.commit()
        finally:
            cur.close()

        return redirect(url_for('groups_expenses'))

    # Get the members of the group
    members = get_room_members(room_id)
    return render_template('settle_up.html', room_id=room_id, members=members, username=username)

@app.route('/end_group/<int:room_id>', methods=['POST'])
def end_group(room_id):
    if 'username' in session:
        username = session['username']
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Check if the user is the creator of the group
        cur.execute("SELECT creator, group_name FROM rooms WHERE room_id = %s", (room_id,))
        room = cur.fetchone()
        
        if room and room['creator'] == username:
            cur.execute("UPDATE rooms SET is_active = 0, ended_at = NOW() WHERE room_id = %s", (room_id,))
            mysql.connection.commit()
        
        # Fetch the group name before ending it
        cur.execute("SELECT group_name FROM rooms WHERE room_id = %s AND creator = %s", (room_id, username))
        group = cur.fetchone()
        
        if group:
            group_name = group['group_name']
            
            # Update the room's status to inactive
            cur.execute("""
                UPDATE rooms
                SET is_active = FALSE
                WHERE room_id = %s AND creator = %s
            """, (room_id, username))
            
            # Log the activity
            cur.execute("""
                INSERT INTO activity_logs (username, activity, room_id, activity_time)
                VALUES (%s, %s, %s, NOW())
            """, (username, f"{username} ended the group {group_name} (room_id: {room_id})", room_id))
                
            mysql.connection.commit()
            
            cur.close()
        
        # Get the members of the group
        members = get_room_members(room_id)
        return redirect(url_for('groups_expenses', room_id=room_id, members=members, username=username))
    else:
        return redirect(url_for('login'))


def get_room_info(room_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT room_id, group_name, username AS creator FROM rooms WHERE room_id = %s", (room_id,))
    room_info = cur.fetchone()
    cur.close()
    return room_info

def get_room_members(room_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT username FROM members WHERE room_id = %s", (room_id,))
    members = cur.fetchall()
    cur.close()
    return members

@app.route('/activity')
def activity():
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Get the activity logs for the rooms the user is a member of
        cur.execute("""
            SELECT al.*
            FROM activity_logs al
            JOIN members m ON al.room_id = m.room_id
            WHERE m.username = %s
            ORDER BY al.activity_time DESC
        """, (username,))
        activities = cur.fetchall()
        cur.close()

        # Format the date and time manually
        for activity in activities:
            activity_time = activity['activity_time']
            month = activity_time.strftime('%b')
            day = activity_time.day
            hour = activity_time.hour % 12 or 12  # Convert to 12-hour format
            minute = activity_time.strftime('%M')
            am_pm = activity_time.strftime('%p')
            activity['activity_time'] = f"{month} {day}, {hour}:{minute} {am_pm}"

        return render_template('activity.html', activities=activities)
    else:
        return redirect(url_for('login'))
    
@app.route('/history')
def history():
    if 'username' in session:
        username = session['username']
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Fetch ended rooms the user is part of
        cur.execute("""
            SELECT rooms.room_id, rooms.group_name, rooms.creator, rooms.created_at, rooms.is_active, rooms.ended_at
            FROM rooms 
            JOIN members ON rooms.room_id = members.room_id 
            WHERE members.username = %s AND rooms.is_active = 0
            ORDER BY rooms.ended_at DESC
        """, (username,))
        rooms = cur.fetchall()

        rooms_dict = {room['room_id']: room for room in rooms}
        
        # Fetch expenses for the rooms
        expenses_dict = {}
        for room_id in rooms_dict:
            cur.execute("""
                SELECT id, description, amount, paid_by, created_at 
                FROM expenses 
                WHERE room_id = %s
            """, (room_id,))
            expenses_dict[room_id] = cur.fetchall()
        
        # Fetch members for the rooms
        members_dict = {}
        for room_id in rooms_dict:
            cur.execute("""
                SELECT username 
                FROM members 
                WHERE room_id = %s
            """, (room_id,))
            members = cur.fetchall()
            members_dict[room_id] = [member['username'] for member in members]
        
        cur.close()
        
        return render_template('history.html', username=username, rooms_dict=rooms_dict, expenses_dict=expenses_dict, members_dict=members_dict)
    else:
        return redirect(url_for('login'))

@app.route('/statistics')
def statistics():
    if 'username' in session:
        username = session['username']
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Calculate start dates for weekly, monthly, and yearly periods
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week
        start_of_month = today.replace(day=1)  # First day of the current month
        start_of_year = today.replace(month=1, day=1)  # First day of the current year

        # Fetch total expenses for the week
        cur.execute("""
            SELECT SUM(amount) as total_weekly_expenses
            FROM expenses
            WHERE created_at >= %s AND created_at < %s
        """, (start_of_week, today))
        total_weekly_expenses = cur.fetchone()['total_weekly_expenses']

        # Fetch total expenses for the month
        cur.execute("""
            SELECT SUM(amount) as total_monthly_expenses
            FROM expenses
            WHERE created_at >= %s AND created_at < %s
        """, (start_of_month, today))
        total_monthly_expenses = cur.fetchone()['total_monthly_expenses']

        # Fetch total expenses for the year
        cur.execute("""
            SELECT SUM(amount) as total_yearly_expenses
            FROM expenses
            WHERE created_at >= %s AND created_at < %s
        """, (start_of_year, today))
        total_yearly_expenses = cur.fetchone()['total_yearly_expenses']

        cur.close()

        return render_template('statistics.html', username=username, total_weekly_expenses=total_weekly_expenses, total_monthly_expenses=total_monthly_expenses, total_yearly_expenses=total_yearly_expenses)
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)