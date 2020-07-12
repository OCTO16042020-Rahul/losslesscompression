from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
import pymysql


app = Flask(__name__)
app.secret_key = 'random string'


app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploaded_images'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


#Database Connection
def dbConnection():
    connection = pymysql.connect(host="localhost", user="root", password="root", database="retinopathy16")
    return connection


#close DB connection
def dbClose():
    dbConnection().close()
    return


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    if 'user' in session:

        return render_template('home.html', user=session['user'])
    return redirect(url_for('index'))


@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        mobno = request.form.get("mobno")
        password = request.form.get("pas")
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM userdetails WHERE mobile = %s AND password = %s',(mobno, password))
        res = cursor.fetchone()
        print(res)
        if result_count > 0:
            print(result_count)
            session['user'] = mobno
            return redirect(url_for('home'))
        else:
            print(result_count)
            msg = 'Incorrect username/password!'
            return render_template('login.html')
    return render_template('/')


@app.route('/register', methods=["GET","POST"])
def register():
    print("register")
    if request.method == "POST":
        try:
            name = request.form.get("name")
            address = request.form.get("address")
            mailid = request.form.get("mailid")
            mobile = request.form.get("mobile")
            pass1 = request.form.get("pass1")
            con = dbConnection()
            cursor = con.cursor()
            cursor.execute('SELECT * FROM userdetails WHERE mobile = %s', (mobile))
            res = cursor.fetchone()
            if not res:
                sql = "INSERT INTO userdetails (name, address, email, mobile, password) VALUES (%s, %s, %s, %s, %s)"
                val = (name, address, mailid, mobile, pass1)
                cursor.execute(sql, val)
                con.commit()
                status= "success"
                return redirect(url_for('index'))
            else:
                status = "Already available"
            return status
        except:
            print("Exception occured at user registration")
            return redirect(url_for('index'))
        finally:
            dbClose()
    return render_template('/')






@app.route('/imageupload', methods=["GET","POST"])
def imageupload():
    if 'user' in session:
        if request.method == "POST":
            #aa = request.form.get("aa")
            #print(aa)
            file = request.files['imagefile']
            pic = file.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "_")
            save_photo = photos.save(file)
            print('Uploaded')

        return render_template('imageupload.html', user=session['user'])
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug="True")
    #app.run()
