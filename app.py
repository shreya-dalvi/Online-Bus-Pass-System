from calendar import c
import email
from multiprocessing import connection
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pymysql
import mysql.connector
import razorpay
import json
#import db.yaml

app = Flask(__name__)
app.secret_key = 'online bus pass system'
var_list=list()
var_list2=list()
var_list3=list()
var_list4=list()
var_list5=list()
var_list6=list()
var_list7=list()
curr_username = ''


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'passsys'

mysql = MySQL(app)


#*************************************************************************************************************************************************
@app.route('/')
def index():
    return render_template('index.html')


#*************************************************************************************************************************************************
@app.route('/login',methods=['GET', 'POST'])
def login():
    mesage=''
    if request.method == 'POST' and 'uname' in request.form and 'password' in request.form:
        uname=request.form['uname']
        password=request.form['password']
        var_list4.append(uname)
        var_list5.append(uname)
        var_list6.append(uname)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE uname = %s AND pword = %s',(uname, password))
        user=cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['fname']= user['fname']
            session['uname'] = user['uname']
            session['email'] = user['email']
            session['mobile'] = user['mobile']
            session['password'] = user['pword']
            mesage='Logged in successfully !'
            return render_template('index2.html', mesage = mesage)
        else:
            mesage='Incorrect Username or Password!'
    return render_template('login.html')


#*************************************************************************************************************************************************
@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        userName = details['uname']
        emailId = details['email']
        contactNo = details['mobile']
        passWord = details['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (fname, uname, email, mobile, pword) VALUES (%s, %s, %s, %s, %s)", (firstName, userName, emailId, contactNo, passWord))
        mysql.connection.commit()
        cur.close()
        return login()
    return render_template('register.html')


#*************************************************************************************************************************************************
@app.route('/commonpage',methods=['GET', 'POST'])
def commonpage():
    if request.method == 'POST':
        userDetails=request.form
        name = userDetails['name']
        age = userDetails['age']
        gender = userDetails['gender']
        aadhar = userDetails['aadhar']
        category = userDetails['category']
        type = userDetails['type']
        region = userDetails['region']
        tdate = userDetails['tdate']
        key1 = request.form.get("aadhar")
        key2 = request.form.get("tdate")
        key3 = request.form.get("type")
        key4 = request.form.get("region")

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO commonpasses(name, age, gender, aadhar, category, type, region, tdate) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (name, age, gender, aadhar, category, type, region, tdate))
        print(key1)
        var_list.append(key1)
        var_list.append(key2)
        var_list.append(key3)

        var_list2.append(key1)
        var_list2.append(key2)
        var_list2.append(key3)

        var_list3.append(key1)
        var_list3.append(key2)
        var_list3.append(key3)

        print(key1)
        mysql.connection.commit()
        cur.close()
        return details()
    return render_template('commonpage.html')


#*************************************************************************************************************************************************
@app.route('/about us')
def about():
    return render_template('about.html')


#*************************************************************************************************************************************************
@app.route('/contact us')
def contact():
    return render_template('contact.html')


#*************************************************************************************************************************************************
@app.route('/forgotpassword',methods=['GET', 'POST'])
def forgot_password():
    mesage=''
    if request.method == 'POST' and 'uname' in request.form and 'email' in request.form:
        uname=request.form['uname']
        email=request.form['email']
        var_list7.append(uname)
        print(var_list7)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE uname = %s AND email = %s',(uname, email))
        user=cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['uname'] = user['uname']
            session['email'] = user['email']
            mesage='Success'
            return redirect(url_for('changepassword'))
        else:
            mesage='Incorrect Username or Email!'
    return render_template('forgotp.html')


#*************************************************************************************************************************************************
@app.route('/RTI')
def rti():
    return render_template('rti.html')


#*************************************************************************************************************************************************
@app.route('/changepassword',methods=['GET','POST'])
def changepassword():
    connection = pymysql.connect(host='localhost',
                                         database='passsys',
                                         user='root',
                                         password='mysql')
    cursor = connection.cursor()
    if request.method == "POST":
        details = request.form
        passWord = details['password']
        curr_username = var_list7.pop()
        var_list7.append(curr_username)
        print(curr_username)
        update_stmt = "update users set pword=%s where uname=%s"
        cursor.execute(update_stmt,(passWord, curr_username))
        connection.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('changePassword.html')


#*************************************************************************************************************************************************
@app.route('/FAQs')
def faqs():
    return render_template('FAQs.html')


#*************************************************************************************************************************************************
@app.route('/home')
def index2():
    return render_template('index2.html')


#*************************************************************************************************************************************************
@app.route('/about')
def about2():
    return render_template('about2.html')


#*************************************************************************************************************************************************
@app.route('/contact')
def contact2():
    return render_template('contact2.html')


#*************************************************************************************************************************************************
@app.route('/paymentFailed')
def payfail():
    return render_template('paymentfailed.html')


#*************************************************************************************************************************************************
@app.route('/myprofile',methods=['GET', 'POST'])
def myprofile():
    connection = pymysql.connect(host='localhost',
                                         database='passsys',
                                         user='root',
                                         password='mysql')
    cursor = connection.cursor()
    curr_username = var_list4.pop()
    var_list4.append(curr_username)
    print(curr_username)
    select_stmt = "select * from users where uname=%s"
    cursor.execute(select_stmt,(curr_username))
    records = cursor.fetchall()
    for i in records:
        print(i)
    cursor.close()
    return render_template('MyProfile.html', value=records)


#*************************************************************************************************************************************************
@app.route('/updateprofile',methods=['GET', 'POST'])
def updateprofile():
    connection = pymysql.connect(host='localhost',
                                         database='passsys',
                                         user='root',
                                         password='mysql')
    cursor = connection.cursor()
    curr_username = var_list5.pop()
    var_list5.append(curr_username)
    print(curr_username)
    select_stmt = "select * from users where uname=%s"
    cursor.execute(select_stmt,(curr_username))
    records = cursor.fetchall()
    for i in records:
        print(i)
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        emailId = details['email']
        contactNo = details['mobile']
        passWord = details['password']
        curr_username = var_list6.pop()
        var_list6.append(curr_username)
        var_list4.append(curr_username)
        var_list5.append(curr_username)
        print(firstName, emailId, contactNo, passWord)
        update_stmt = "update users set fname=%s, email=%s, mobile=%s, pword=%s where uname=%s"
        cursor.execute(update_stmt,(firstName, emailId, contactNo, passWord, curr_username))
        connection.commit()
        cursor.close()
        return myprofile()
    return render_template('UpdateProf.html', value=records)

#*************************************************************************************************************************************************
@app.route('/details',methods=['GET', 'POST'])
def details():
    connection = pymysql.connect(host='localhost',
                                         database='passsys',
                                         user='root',
                                         password='mysql')

    sql_select_Query = "select * from commonpasses"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    # get all records
    #records = cursor.fetchall()
    key1 = var_list.pop()
    key2 = var_list.pop()
    key3 = var_list.pop()

    var_list.append(key3)
    var_list.append(key2)
    var_list.append(key1)
    #key1=str(key)
    print(key1)
    print(key2)
    print(key3)

    data = "select * from commonpasses where aadhar=%s and tdate=%s"
    cursor.execute(data,(key3, key2))
    records = cursor.fetchall()
    print("Total number of rows in table: ", cursor.rowcount)

    print("\nPrinting each row")
    if key1=="ONE MONTH":
        amt="750"
    else:
        amt="50"
    global payment, name
    name = request.form.get('username')

    import razorpay
    client = razorpay.Client(auth=("rzp_test_DFph5mnoblMl15", "R8bE0UhDRvgrIwegFCm2ZjBC"))
    ammt=int(amt)
    DATA = {
        "amount": ammt*100,
        "currency": "INR",
        "receipt": "receipt#1",
    }
    payment = client.order.create(data=DATA)
    return render_template('details3.html',value=records,amt=amt,payment=payment)


#*************************************************************************************************************************************************
@app.route('/generatepdf',methods=['GET','POST'])
def generatepdf():
    connection = pymysql.connect(host='localhost',
                                 database='passsys',
                                 user='root',
                                 password='mysql')

    sql_select_Query = "select * from commonpasses"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    # get all records
    # records = cursor.fetchall()
    key1 = var_list2.pop()
    key2 = var_list2.pop()
    key3 = var_list2.pop()

    var_list2.append(key3)
    var_list2.append(key2)
    var_list2.append(key1)

    # key1=str(key)
    print(key1)
    print(key2)
    print(key3)

    data = "select * from commonpasses where aadhar=%s and tdate=%s"
    cursor.execute(data, (key3, key2))
    records = cursor.fetchall()
    if key1=="ONE MONTH":
        amt="750"
    else:
        amt="50"
    return render_template('downloadPDF.html', value=records, amt=amt,)

if __name__ == '__main__':
    app.run(debug=True)