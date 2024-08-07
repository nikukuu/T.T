from flask import Flask, flash, jsonify, render_template, url_for, redirect, request, session
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
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'uwuwers'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max size
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'splitshare'

mysql = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class User(UserMixin):
    def __init__(self, id=None, username=None, email=None, first_name=None, last_name=None, phone_number=None, profile_picture=None, instagram=None, facebook=None, twitter=None, github=None):
        self.id = id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.profile_picture = profile_picture
        self.instagram = instagram
        self.facebook = facebook
        self.twitter = twitter
        self.github = github

    def get_id(self):
        return str(self.id)
    
    def update(self, username, email, first_name, last_name, phone_number, profile_picture, instagram, facebook, twitter, github):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.profile_picture = profile_picture
        self.instagram = instagram
        self.facebook = facebook
        self.twitter = twitter
        self.github = github

    @staticmethod
    def get(user_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, email, first_name, last_name, phone_number, profile_picture, instagram, facebook, twitter, github FROM register WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        if user:
            return User(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10])
        return None

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email, first_name, last_name, phone_number, profile_picture, instagram, facebook, twitter, github FROM register WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()

    if user_data:
        session['username'] = user_data[1]  # Set username in session
        return User(
            id=user_data[0],
            username=user_data[1],
            email=user_data[2],
            first_name=user_data[3],
            last_name=user_data[4],
            phone_number=user_data[5],
            profile_picture=user_data[6],
            instagram=user_data[7],
            facebook=user_data[8],
            twitter=user_data[9],
            github=user_data[10]
        )
    return None

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
        
        # Fetch user data from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, password, email, first_name, last_name, phone_number FROM register WHERE username = %s", (username,))
        user_data = cur.fetchone()
        cur.close()

        if user_data is None:
            return render_template('base.html', error='User does not exist')
        elif password == user_data[2]:  # Compare plain text passwords
            user = User(
                id=user_data[0],
                username=user_data[1],
                email=user_data[3],
                first_name=user_data[4],
                last_name=user_data[5],
                phone_number=user_data[6]
            )
            login_user(user)  # Use Flask-Login to log in
            return redirect(url_for('home'))
        else:
            return render_template('base.html', error='Invalid password')

    return render_template('base.html', success=success_message)

#sign up
@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        # Debugging lines
        print(request.form)  # To see what data is being posted

        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')

        if not all([email, username, password, first_name, last_name, phone_number]):
            return render_template('sign_up.html', error='All fields are required.')

        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM register WHERE username = %s", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            return render_template('base.html', error='Username already exists. Please choose a different username.')

        cur.execute("""
            INSERT INTO register (email, username, password, first_name, last_name, phone_number) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (email, username, password, first_name, last_name, phone_number))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login', success='Your account has been created. You can now log in.'))

    return render_template('base.html')

#dashboard
@app.route('/home')
def home():
    username = current_user.username
    profile_picture = current_user.profile_picture
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

    return render_template('home.html', username=username, total_owed=total_owed, borrowers=borrowers, profile_picture=profile_picture)

#user profile    
@app.route('/profile')
@login_required
def profile():
    username = current_user.username
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM register WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    return render_template('profile.html', user=user)

#update credentials
@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        # Retrieve the data from the form
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        address = request.form['address']
        profile_picture = request.files['profile_picture']
        # Retrieve social media links
        instagram = request.form.get('instagram')
        facebook = request.form.get('facebook')
        twitter = request.form.get('twitter')
        github = request.form.get('github')

        # Handle file upload
        profile_picture_path = current_user.profile_picture  # Default to existing picture
        if profile_picture and allowed_file(profile_picture.filename):
            filename = secure_filename(profile_picture.filename)
            profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profile_picture.save(profile_picture_path)

        # Update the database with new values
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE register 
            SET username = %s, first_name = %s, last_name = %s, email = %s, phone_number = %s, address = %s, profile_picture = %s,
                instagram = %s, facebook = %s, twitter = %s, github = %s
            WHERE id = %s
        """, (username, first_name, last_name, email, phone_number, address, profile_picture_path,
              instagram, facebook, twitter, github, current_user.id))
        mysql.connection.commit()

        # Update the session and current_user data
        current_user.username = username
        current_user.email = email
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.phone_number = phone_number
        current_user.profile_picture = profile_picture_path
        current_user.instagram = instagram
        current_user.facebook = facebook
        current_user.twitter = twitter
        current_user.github = github

        # If username has changed, update the session
        if session['username'] != username:
            session['username'] = username

        cur.close()

        # Redirect to the profile page
        return redirect(url_for('profile', success= 'You have successfully updated your profile!'))

    return render_template('profile.html', user=current_user)


#logout    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('homepage.html')

@app.route('/groups', methods=['POST', 'GET'])
@login_required
def groups():
    qr_code_url = None
    room_id = None  # Initialize room_id to None
    if request.method == 'POST' and request.form.get('action') == 'create_group':
        username = current_user.username
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

    return render_template('groups.html', qr_code_url=qr_code_url, room_id=room_id)

@app.route('/active_groups')
@login_required
def active_groups():
    username = current_user.username
    profile_picture = current_user.profile_picture

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Fetch active rooms the user is part of
    cur.execute("""
        SELECT rooms.room_id, rooms.group_name
        FROM rooms 
        JOIN members ON rooms.room_id = members.room_id 
        WHERE members.username = %s AND rooms.is_active = 1
        ORDER BY rooms.created_at DESC
    """, (username,))
    rooms = cur.fetchall()
    
    cur.close()

    return render_template('active_groups.html', rooms=rooms, username=username, profile_picture=profile_picture)

#join a room
@app.route('/join/<int:room_id>', methods=['GET'])
@login_required
def join(room_id):
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Get the group name and creation date
        cur.execute("SELECT group_name, created_at FROM rooms WHERE room_id = %s", (room_id,))
        group = cur.fetchone()
        group_name = group['group_name'] if group else 'Unknown'
        created_at = group['created_at'].strftime("%b %d, %Y") if group and group['created_at'] else 'Unknown Date'

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

        return render_template('room.html', room_id=room_id, debts=debts, expenses=expenses, has_expenses=has_expenses, members=members, group_name=group_name, created_at=created_at)
    else:
        return redirect(url_for('login'))
    
@app.route('/code')
@login_required
def code():
    return render_template('code.html')

#qr scanner
@app.route('/scan_qr')
def scan_qr():
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

            cv2.imshow('QR Scanner (Click the letter C on your keybord to close camera)', img)
            if cv2.waitKey(1) == ord('c'):
                break

        cap.release()
        cv2.destroyAllWindows()

    threading.Thread(target=open_qr_scanner).start()
    return '', 204  # No content response

@app.route('/join_by_code', methods=['POST', 'GET'])
@login_required
def join_by_code():
    if 'username' in session:
        username = session['username']
        room_id = request.form.get('room_id')  # Using .get() to avoid KeyError

        if room_id:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Get room_id from the room_id (assuming the form sends room_id directly)
            cur.execute("SELECT room_id FROM rooms WHERE room_id = %s", (room_id,))
            room = cur.fetchone()

            if room:
                room_id = room['room_id']
                return redirect(url_for('join', room_id=room_id))
            else:
                flash('Invalid room ID. Please try again.', 'danger')
                return redirect(url_for('code'))
        else:
            flash('Room ID is required. Please try again.', 'danger')
            return redirect(url_for('scan_qr'))
    else:
        return redirect(url_for('login'))

@app.route('/session/<int:room_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def mainF(room_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Get room information
    cur.execute("SELECT * FROM rooms WHERE room_id = %s", (room_id,))
    room_info = cur.fetchone()
    if not room_info:
        return "Room not found", 404

    # Format the creation date
    created_at = room_info['created_at']
    if created_at:
        created_at = datetime.strptime(str(created_at), '%Y-%m-%d %H:%M:%S').strftime('%b %d, %Y')

    # Check if the user is the creator of the group
    is_creator = (room_info['creator'] == username)

    # Get members
    cur.execute("SELECT username FROM members WHERE room_id = %s", (room_id,))
    members = cur.fetchall()

    # Get expenses
    cur.execute("SELECT * FROM expenses WHERE room_id = %s", (room_id,))
    expenses = cur.fetchall()
    has_expenses = len(expenses) > 0

    if request.method == 'POST' and request.is_json:
        # Handle expense addition
        data = request.get_json()
        description = data.get('description')
        expense = data.get('expense')
        paid_by = data.get('paid_by')

        if description and expense and paid_by:
            try:
                cur.execute("""
                    INSERT INTO expenses (room_id, description, amount, paid_by)
                    VALUES (%s, %s, %s, %s)
                """, (room_id, description, expense, paid_by))
                mysql.connection.commit()

                # Recalculate debts
                cur.execute("DELETE FROM debts WHERE room_id = %s AND lender = %s", (room_id, paid_by))
                mysql.connection.commit()

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
                
                mysql.connection.commit()

                return jsonify({
                    'description': description,
                    'amount': expense,
                    'paid_by': paid_by
                }), 201
            except Exception as e:
                mysql.connection.rollback()
                return jsonify({'error': str(e)}), 500

        return jsonify({'error': 'Invalid input'}), 400

    elif request.method == 'PUT' and request.is_json:
        # Handle expense editing
        data = request.get_json()
        expense_id = data.get('expense_id')
        description = data.get('description')
        amount = data.get('amount')
        paid_by = data.get('paid_by')

        try:
            # Update the expense in the database
            cur.execute("""
                UPDATE expenses 
                SET description = %s, amount = %s, paid_by = %s 
                WHERE id = %s AND room_id = %s
            """, (description, amount, paid_by, expense_id, room_id))
            mysql.connection.commit()

            # Recalculate debts
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
            cur.execute("""
                INSERT INTO activity_logs (username, activity, room_id)
                VALUES (%s, %s, %s)
            """, (username, f"{username} edited the expense {description} in group {room_info['group_name']}", room_id))

            mysql.connection.commit()

            return jsonify({
                'description': description,
                'amount': amount,
                'paid_by': paid_by
            }), 200

        except Exception as e:
            mysql.connection.rollback()
            return jsonify({'error': str(e)}), 500

    elif request.method == 'DELETE':
        # Handle expense removal
        expense_id = request.args.get('expense_id')
        if not expense_id:
            return jsonify({'error': 'No expense ID provided'}), 400

        try:
            cur.execute("DELETE FROM expenses WHERE id = %s AND room_id = %s", (expense_id, room_id))
            mysql.connection.commit()

            # Remove related debts
            cur.execute("DELETE FROM debts WHERE room_id = %s AND expense_id = %s", (room_id, expense_id))
            mysql.connection.commit()

            # Log the activity
            cur.execute("""
                INSERT INTO activity_logs (username, activity, room_id)
                VALUES (%s, %s, %s)
            """, (username, f"Removed an expense", room_id))

            mysql.connection.commit()

            return jsonify({'success': 'Expense removed'}), 200

        except Exception as e:
            mysql.connection.rollback()
            return jsonify({'error': str(e)}), 500

    # Handle settlement
    if request.method == 'POST' and 'payer' in request.form:
        payer = request.form['payer']
        recipient = request.form['recipient']
        amount = float(request.form['amount'])
        date = request.form['date']
        payment_method = request.form['payment_method']

        try:
            # Insert settlement record
            cur.execute("""
                INSERT INTO settlements (room_id, payer, recipient, amount, date, payment_method)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (room_id, payer, recipient, amount, date, payment_method))
            mysql.connection.commit()

            # Log the activity
            cur.execute("""
                INSERT INTO activity_logs (username, activity, room_id)
                VALUES (%s, %s, %s)
            """, (username, f"{username} recorded a payment from {payer} to {recipient} in group {room_info['group_name']}", room_id))
            mysql.connection.commit()

        except Exception as e:
            mysql.connection.rollback()
            flash(f"An error occurred: {e}", "error")

        return redirect(url_for('mainF', room_id=room_id))

    cur.close()

    success = request.args.get('success', None)

    return render_template('session.html', room_id=room_id, members=members, expenses=expenses,
                           has_expenses=has_expenses, username=username, room_info=room_info, success=success,
                           created_at=created_at, is_creator=is_creator)

#Dito
@app.route('/settle/<room_id>', methods=['GET', 'POST'])
def settle_up(room_id):
    if request.method == 'POST':
        payer = request.form['payer']
        recipient = request.form['recipient']
        amount = float(request.form['amount'])
        date = request.form['date']
        payment_method = request.form['payment_method']
        
        # Update balances
        update_user_balance(payer, -amount)  # Deduct amount from payer
        update_user_balance(recipient, amount)  # Add amount to recipient
        
        # Redirect to GET request to fetch updated data
        return redirect(url_for('settle_up', room_id=room_id))
    
    # For GET requests, render the page with user balances
    members = get_members(room_id)
    user_balances = get_user_balances(room_id)
    
    return render_template('settle.html', room_id=room_id, members=members, user_balances=user_balances)

def get_user_balances(room_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT u.username, u.balance 
        FROM register u 
        JOIN room_members rm ON u.id = rm.user_id 
        WHERE rm.room_id = %s
    """, (room_id,))
    user_balances = cur.fetchall()
    cur.close()
    return [{'username': user[0], 'balance': user[1]} for user in user_balances]

def update_user_balance(username, amount):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE register SET balance = balance + %s WHERE username = %s", (amount, username))
    mysql.connection.commit()
    cur.close()

def get_members(room_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT u.username 
        FROM register u 
        JOIN room_members rm ON u.id = rm.user_id 
        WHERE rm.room_id = %s
    """, (room_id,))
    members = cur.fetchall()
    cur.close()
    return [{'username': member[0]} for member in members]
#Hanggang dito



@app.route('/groups_list')
@login_required
def groups_list():
    username = session['username']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
            
        cur.execute("""
            SELECT rooms.room_id, rooms.group_name
            FROM rooms 
            JOIN members ON rooms.room_id = members.room_id 
            WHERE members.username = %s AND rooms.is_active = 1
            ORDER BY rooms.created_at DESC
        """, (username,))
        groups = cur.fetchall()
    except MySQLdb.Error as e:
        flash(f"An error occurred: {e}", "error")
        groups = []
    finally:
        cur.close()
    
    return render_template('groups_list.html', groups=groups)


@app.route('/group_redirect/<int:room_id>')
@login_required
def group_redirect(room_id):
    username = session['username']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        cur.execute("SELECT creator FROM rooms WHERE room_id = %s", (room_id,))
        room = cur.fetchone()
        
        if room:
            if room['creator'] == username:
                return redirect(url_for('mainF', room_id=room_id))
            else:
                return redirect(url_for('join', room_id=room_id))
        else:
            flash("Group not found.", "error")
            return redirect(url_for('groups_list'))
    except MySQLdb.Error as e:
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for('groups_list'))
    finally:
        cur.close()
    

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

#settle up
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
        return redirect(url_for('groups_list', room_id=room_id, members=members, username=username))
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

@app.route('/statistics/<int:room_id>')
def statistics(room_id):
    if 'username' in session:
        username = session['username']
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Fetch total expenses for each month of the current year for the specific room
        cur.execute("""
            SELECT 
                MONTH(created_at) as month, 
                SUM(amount) as total_expenses
            FROM expenses
            WHERE YEAR(created_at) = YEAR(CURDATE()) AND room_id = %s
            GROUP BY MONTH(created_at)
            ORDER BY MONTH(created_at)
        """, (room_id,))
        monthly_expenses = cur.fetchall()
        
        cur.close()

        # Prepare data for visualization
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        expenses = [0] * 12
        for expense in monthly_expenses:
            month_index = expense['month'] - 1
            expenses[month_index] = expense['total_expenses']

        return render_template('statistics.html', username=username, months=months, expenses=expenses, room_id=room_id)
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)