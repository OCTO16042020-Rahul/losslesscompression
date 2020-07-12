import os

import app as app

from lossless1 import encode_image, decode_image
# import magic
import urllib.request



from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

from flask import Flask, render_template, url_for, request, session, flash
import pandas as pd
import pickle


from sklearn.feature_extraction.text import CountVectorizer
import pymysql
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from werkzeug.utils import secure_filename


connection = pymysql.connect(host="localhost", user="root", password="", database="losslesscompression")
cursor = connection.cursor()

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'G:/rahuldata'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index1.html')
@app.route('/data')
def data():
    username = session['user']
    cursor.execute('SELECT * FROM insertdata WHERE username = %s ', (username))


    print(cursor.execute)
    data = cursor.fetchall()  # data from database
    msg = 'Incorrect username/password!'

    return render_template("decodeimage.html",data=data)

@app.route('/decodeimage', methods=["GET","POST"])
def decodeimage():
    if 'user' in session:
        if request.method == "POST":
            username = session['user']
            username1 = request.form.get("text1")
            #aa = request.form.get("aa")
            #print(aa)
            file1 = request.form.get("imagefile1")
            file = request.files['imagefile']
            pic = file.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "_")
            import string
            import random

            # initializing size of string
            N = 7

            # using random.choices()
            # generating random strings
            res = ''.join(random.choices(string.ascii_uppercase +
                                         string.digits, k=N))

            # print result
            print("The generated random string : " + str(res))
            decodeimage2 = str(res) + '.png'
            # aa = request.form.get("aa")

            # generate some integers

            file = request.files['imagefile']
            cursor = connection.cursor()
            query12 = "UPDATE insertdata SET decodedimage ='" + decodeimage2 + "' WHERE   username='" + username + "' and encodeimagename ='" + file1 + "'"
            print(query12)

            cursor.execute(query12)
            connection.commit()

            print(cursor.execute)
            pic = file.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "_")
            decode_image(file, decodeimage2)
        return render_template('decode.html', user=session['user'])
    return redirect(url_for('index'))
@app.route('/imageupload', methods=["GET","POST"])
def imageupload():
    if 'user' in session:
        if request.method == "POST":
            username = session['user']
            username1 = request.form.get("text1")
            #aa = request.form.get("aa")
            import string
            import random

            # initializing size of string
            N = 7

            # using random.choices()
            # generating random strings
            res = ''.join(random.choices(string.ascii_uppercase +
                                         string.digits, k=N))

            #print(aa)
            imgname1 = str(res) + '.png'
            file = request.files['imagefile']
            pic = file.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "_")

            encode_image(username1, file,imgname1)
            print('Uploaded')
            cursor = connection.cursor()
            cursor.execute(
                "insert into insertdata(username, textdata, encodeimagename) values('" + username + "','" + username1 + "','" + imgname1 + "')")
            connection.commit()
            print(cursor.execute)
            msg = 'Successfully upload file'

        return render_template('sendmail.html', msg=msg,username=session['user'])
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        username = session['user']
        username1 = request.form.get("text1")
        if 'file' not in request.files:
            flash('No file part')
            return render_template('index1.html')
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return render_template('index2.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            cursor.execute(
                "insert into files(filename, username ) values('" + filename + "','" + username + "')")
            connection.commit()


            file1=file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            encode_image(username1,file1)
            flash('File successfully uploaded')
            return render_template('sendmail.html')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return render_template('index4.html')


def upload1():
    if request.method == "POST":
        target = os.path.join(APP_ROOT, 'images/')
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)
        username = request.form.get("text1")
        for file in request.files.getlist("fname"):
            print(file)
            filename = file.filename
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)

            return render_template('login.html')
    return render_template('index.html')


@app.route('/sendmail1')
def sendmail1():
    return render_template('sendmail.html', username=session['user'])

@app.route('/decode')
def decode():
    return render_template('decode.html', username=session['user'])
@app.route('/decoded12')
def decoded12():
    return render_template('decodeimage.html', username=session['user'])





@app.route('/sendmail')
def sendmail():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        username = request.form.get("username")

        password = request.form.get("password")

        # print("insert into userdetails(fname, lname, password) values('"+fname+"','"+lname+",'"+password+")")

        # cursor.execute("insert into userdetails(fname, lname, password) values(:fname, :lname, :password)",{"fname":fname,"lname":fname,"password":password})
        cursor.execute(
            "insert into userdetails(name, phone, username ,password) values('" + name + "','" + phone + "','" + username + "','" + password + "')")

        connection.commit()

        return render_template("login.html")
    else:
        return render_template("about.html")

    return render_template('sendmail.html')


@app.route('/logout')
def logout():
    return render_template('index1.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register1', methods=["POST", "GET"])
def register1():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        username = request.form.get("username")

        password = request.form.get("password")
        msg = 'Successfully Register plz login now'
        # print("insert into userdetails(fname, lname, password) values('"+fname+"','"+lname+",'"+password+")")

        # cursor.execute("insert into userdetails(fname, lname, password) values(:fname, :lname, :password)",{"fname":fname,"lname":fname,"password":password})
        cursor.execute(
            "insert into userdetails(name, phone, username ,password) values('" + name + "','" + phone + "','" + username + "','" + password + "')")

        connection.commit()

        return render_template("index1.html", msg=msg)


@app.route('/foo')
def foo():
    username = session['user']
    cursor.execute('SELECT * FROM sendmail WHERE sendermail = %s ', (username))

    print(cursor.execute)
    data = cursor.fetchall()  # data from database
    msg = 'Incorrect username/password!'
    return render_template("alldata.html", value=data)


@app.route('/recieved')
def recieved():
    username = session['user']
    cursor.execute('SELECT * FROM sendmail WHERE recievermail = %s ', (username))

    print(cursor.execute)
    data = cursor.fetchall()  # data from database
    msg = 'Incorrect username/password!'
    return render_template("alldata.html", value=data)


@app.route('/predict', methods=['POST'])
def predict():
    df = pd.read_csv("spam.csv", encoding="latin-1")
    df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
    # Features and Labels
    df['label'] = df['class'].map({'ham': 0, 'spam': 1})
    X = df['message']
    y = df['label']

    # Extract Feature With CountVectorizer
    cv = CountVectorizer()
    X = cv.fit_transform(X)  # Fit the Data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    # Naive Bayes Classifier
    from sklearn.naive_bayes import MultinomialNB

    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    clf.score(X_test, y_test)
    # Alternative Usage of Saved Model
    # joblib.dump(clf, 'NB_spam_model.pkl')
    # NB_spam_model = open('NB_spam_model.pkl','rb')
    # clf = joblib.load(NB_spam_model)

    if request.method == 'POST':
        sendermail = request.form.get("sendermail")

        recievermail = request.form.get("recievermail")

        message = request.form.get("message")
        data = [message]
        vect = cv.transform(data).toarray()
        myprediction = clf.predict(vect)
        if myprediction == [1]:
            checkstatus = "spam"
        elif myprediction == [0]:
            checkstatus = "not spam"
        cursor = connection.cursor()
        cursor.execute(
            "insert into sendmail(sendermail, recievermail, message,myprediction) values('" + sendermail + "','" + recievermail + "','" + message + "','" + checkstatus + "')")
        connection.commit()
        print(cursor.execute)

        return render_template("sendmail.html")


@app.route('/login1', methods=["POST", "GET"])
def login1():
    if request.method == "POST":

        username = request.form.get("username")

        password = request.form.get("password")

        cursor.execute('SELECT * FROM userdetails WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)

        # If account exists in accounts table in out database
        if account:

            session['user'] = account[2]
            msg = 'Logged in successfully'

            return render_template('sendmail.html', username=session['user'])
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
        # Show the login form with message (if any)6
    return render_template('index1.html', msg=msg)


if __name__ == '__main__':
    app.run('0.0.0.0')
