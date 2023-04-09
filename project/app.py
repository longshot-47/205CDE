from flask import Flask, render_template, request
import pymysql
import time

app = Flask(__name__, static_url_path='', static_folder='templates', template_folder='templates')
@app.route('/')

def home():
    return render_template('book.html')

@app.route('/login', methods=['POST', 'GET'])

def login():
    
    uid = request.form.get('uid')
    pw = request.form.get('pw')

    connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from idpw WHERE id = \'%s\' and pw = \'%s\'"%( uid, pw ))
        if not cursor.rowcount:             #check ID and password match with database
            return render_template('login.html')
        else:
            cursor.execute('SELECT * FROM booked')
            book = cursor.fetchall()
            length1 = len(book)
            cursor.execute('SELECT * FROM not_confirmed')
            not_confirmed = cursor.fetchall()
            length2 = len(not_confirmed)
            cursor.execute('SELECT * FROM confirmed')
            confirm = cursor.fetchall()
            length3 = len(confirm)
            refresh = time.strftime("%Y-%m-%d %H:%M:%S")
            return render_template('admin.html', booked = book, len1 = length1, not_confirmed = not_confirmed, len2 = length2, confirmed = confirm, len3 = length3, time = refresh)
    
        
@app.route('/submit', methods=['POST', 'GET'])

def submit():
    
    email = request.form.get('email')
    date = request.form.get('date')
    time = request.form.get('time')
    food = request.form.get('food')
    amount = 0
    amount = request.form.get('amount')
    people = request.form.get('people')
    staff = request.form.get('staff')

    connection = pymysql.connect(user='root',
                                password='Peter.515',
                                db='best', 
                                cursorclass=pymysql.cursors.DictCursor)
    
    with connection.cursor() as cursor:
        cursor.execute("Insert INTO booked (email, date, start_time, food, food_amount, people_amount, staff) VAlUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')"%( email, date, time, food, amount, people, staff ))
        connection.commit()
    return render_template('success.html')

@app.route('/menu', methods=['POST', 'GET'])

def menu():             #back to main menu(admin.html)
        
        connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
        
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM booked')
            book = cursor.fetchall()
            length1 = len(book)
            cursor.execute('SELECT * FROM not_confirmed')
            not_confirmed = cursor.fetchall()
            length2 = len(not_confirmed)
            cursor.execute('SELECT * FROM confirmed')
            confirm = cursor.fetchall()
            length3 = len(confirm)
            refresh = time.strftime("%Y-%m-%d %H:%M:%S")
            return render_template('admin.html', booked = book, len1 = length1, not_confirmed = not_confirmed, len2 = length2, confirmed = confirm, len3 = length3, time = refresh)

@app.route('/open_accept', methods=['POST', 'GET'])        

def open_accept():
    
    connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
    
    with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM booked')
            book = cursor.fetchall()
            length1 = len(book)
            cursor.execute('SELECT * FROM not_confirmed')
            not_confirmed = cursor.fetchall()
            length2 = len(not_confirmed)
            cursor.execute('SELECT * FROM confirmed')
            confirm = cursor.fetchall()
            length3 = len(confirm)
            return render_template('accept.html', booked = book, len1 = length1, not_confirmed = not_confirmed, len2 = length2, confirmed = confirm, len3 = length3)
    
@app.route('/process_accept', methods=['POST', 'GET'])

def process_accept():
     
     connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
     
     with connection.cursor() as cursor:
          process_email = request.form.get('process_new')
          cursor.execute("SELECT * from booked WHERE email = \'%s\'"%(process_email))
          process = cursor.fetchall()
          return render_template('email.html', email = process_email, detail = process)
     
@app.route('/complete_process', methods=['POST', 'GET'])

def complete_process():
     
    connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
    
    with connection.cursor() as cursor:
         
        send_email = request.values.get('email')
        cursor.execute("INSERT INTO not_confirmed SELECT * FROM booked WHERE email = \'%s\'"%(send_email))
        connection.commit()
        cursor.execute("DELETE FROM booked WHERE email = \'%s\';"%(send_email))
        connection.commit()
        return menu()
          
@app.route('/open_update', methods=['POST', 'GET'])

def open_update():

    connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
    
    with connection.cursor() as cursor:
          
        cursor.execute('SELECT * FROM booked')
        book = cursor.fetchall()
        length1 = len(book)
        cursor.execute('SELECT * FROM not_confirmed')
        not_confirmed = cursor.fetchall()
        length2 = len(not_confirmed)
        return render_template('update.html', booked = book, len1 = length1, not_confirmed = not_confirmed, len2 = length2)

@app.route('/open_update_new', methods=['POST', 'GET'])

def open_update_new():
     
     connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
     
     with connection.cursor() as cursor:
          cursor.execute('SELECT * FROM booked')
          book = cursor.fetchall()
          length1 = len(book)
          update_email = request.form.get('update_new')
          cursor.execute("SELECT * from booked WHERE email = \'%s\'"%(update_email))
          return render_template('update_new.html', booked = book, len1 = length1)
     
@app.route('/process_update_new', methods=['POST', 'GET'])

def process_update_new():
     
     connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
     
     date = request.form.get('date')
     time = request.form.get('time')
     food = request.form.get('food')
     amount = request.form.get('amount')
     people = request.form.get('people')
     staff = request.form.get('staff')

     with connection.cursor() as cursor:
          update_email = request.form.get('process_new')
          cursor.execute("update `booked` set `date` = \'%s\', `start_time` = \'%s\', `food` = \'%s\', `food_amount` = \'%s\', `people_amount` =\'%s\', `staff` =\'%s\' where `booked`.`email` = \'%s\'" %(date, time, food, amount, people, staff, update_email))
          connection.commit()
          return open_update()
     
@app.route('/open_update_not', methods=['POST', 'GET'])

def open_update_not():
     
     connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
     
     with connection.cursor() as cursor:
          cursor.execute('SELECT * FROM not_confirmed')
          not_confirmed = cursor.fetchall()
          length1 = len(not_confirmed)
          update_email = request.form.get('update_not')
          cursor.execute("SELECT * from not_confirmed WHERE email = \'%s\'"%(update_email))
          return render_template('update_not.html', not_confirmed = not_confirmed, len1 = length1)
     
@app.route('/process_update_not', methods=['POST', 'GET'])

def process_update_not():
     
     connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
     
     date = request.form.get('date')
     time = request.form.get('time')
     food = request.form.get('food')
     amount = request.form.get('amount')
     people = request.form.get('people')
     staff = request.form.get('staff')

     with connection.cursor() as cursor:
          update_email = request.form.get('process_not')
          cursor.execute("update `not_confirmed` set `date` = \'%s\', `start_time` = \'%s\', `food` = \'%s\', `food_amount` = \'%s\', `people_amount` =\'%s\', `staff` =\'%s\' where `not_confirmed`.`email` = \'%s\'" %(date, time, food, amount, people, staff, update_email))
          connection.commit()
          return open_update()
     
@app.route('/open_confirm', methods=['POST', 'GET'])

def open_confirm():
     
    connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
    
    with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM not_confirmed')
                not_confirmed = cursor.fetchall()
                length1 = len(not_confirmed)
                cursor.execute('SELECT * FROM confirmed')
                confirm = cursor.fetchall()
                length2 = len(confirm)
                return render_template('confirm.html',not_confirmed = not_confirmed, len1 = length1, confirmed = confirm, len2 = length2)   
    
@app.route('/process_confirm', methods=['POST', 'GET'])

def process_confirm():
     
     connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
     
     with connection.cursor() as cursor:
          process_email = request.form.get('process_confirm')
          cursor.execute("SELECT * from not_confirmed WHERE email = \'%s\'"%(process_email))
          process = cursor.fetchall()
          return render_template('confirm_email.html', email = process_email, detail = process)
     
@app.route('/complete_confirm', methods=['POST', 'GET'])

def complete_confirm():
     
    connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
    
    with connection.cursor() as cursor:
         
        send_email = request.values.get('email')
        cursor.execute("INSERT INTO confirmed SELECT * FROM not_confirmed WHERE email = \'%s\'"%(send_email))
        connection.commit()
        cursor.execute("DELETE FROM not_confirmed WHERE email = \'%s\';"%(send_email))
        connection.commit()
        return menu()
    
@app.route('/open_delete', methods=['POST', 'GET'])

def open_delete():
     return render_template('delete.html')

@app.route('/delete_new', methods=['POST', 'GET'])

def delete_new():
     
     connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
     
     with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM booked')
            book = cursor.fetchall()
            length1 = len(book)
            return render_template('delete_new.html', booked = book, len1 = length1)
     
@app.route('/process_delete_new', methods=['POST', 'GET'])

def process_delete_new():
     
     connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
     
     with connection.cursor() as cursor:
          process_email = request.form.get('process_delete')
          cursor.execute("DELETE FROM booked WHERE email = \'%s\'"%(process_email))
          connection.commit()
          return menu()
     
@app.route('/delete_not', methods=['POST', 'GET'])

def delete_not():
     
     connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
     
     with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM not_confirmed')
            not_confirmed = cursor.fetchall()
            length1 = len(not_confirmed)
            return render_template('delete_not.html', not_confirmed = not_confirmed, len1 = length1)
     
@app.route('/process_delete_not', methods=['POST', 'GET'])

def process_delete_not():
     
     connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
     
     with connection.cursor() as cursor:
          process_email = request.form.get('process_delete')
          cursor.execute("DELETE FROM not_confirmed WHERE email = \'%s\'"%(process_email))
          connection.commit()
          return menu()
     
@app.route('/delete_confirm', methods=['POST', 'GET'])

def delete_confirm():
     
     connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
     
     with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM confirmed')
            confirmed = cursor.fetchall()
            length1 = len(confirmed)
            return render_template('delete_confirm.html', confirmed = confirmed, len1 = length1)
     
@app.route('/process_delete_confirm', methods=['POST', 'GET'])

def process_delete_confirm():
     
     connection = pymysql.connect(user='root',
                             password='Peter.515',
                             db='best', 
                             cursorclass=pymysql.cursors.DictCursor)
     
     with connection.cursor() as cursor:
          process_email = request.form.get('process_delete')
          cursor.execute("DELETE FROM confirmed WHERE email = \'%s\'"%(process_email))
          connection.commit()
          return menu()
