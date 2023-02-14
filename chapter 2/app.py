from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL, MySQLdb
import bcrypt 
import werkzeug
import pickle
import numpy as np
import datetime


model = pickle.load(open('Boo1.pkl','rb'))


app = Flask(__name__)
app.secret_key = "membuatLOginFlask1"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yunita123'
app.config['MYSQL_DB'] = 'flaskdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def home() :
    return redirect(url_for('list_report'))
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT  * FROM kepenuhan")
    # data = cur.fetchall()
    # cur.close()
    # return render_template("home.html", kepenuhan=data)

@app.route('/list_report')
def list_report() :
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM report")
    data = cur.fetchall()
    cur.close()
    return render_template("list_report.html", report=data)

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if user is not None and len(user) > 0 :
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['name'] = user ['name']
                session['email'] = user['email']
                return redirect(url_for('home'))
            else :
                flash("Gagal, Email dan Password Tidak Cocok")
                return redirect(url_for('login'))
        else :
            flash("Gagal, User Tidak Ditemukan")
            return redirect(url_for('login'))
    else: 
        return render_template("login.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else :
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)" ,(name, email, hash_password)) 
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))
@app.route('/about')
def about():
    if 'email' in session:
        return render_template("form.html")
    else:
        return redirect(url_for('home'))

@app.route('/predict', methods=['POST'])
def predict():
     if request.method == 'POST':
            
        Namamaskapai = request.form['Namamaskapai']
        Asal_Bandara = request.form['Asal_Bandara']
        Tujuan_Bandara = request.form['Tujuan_Bandara']
        Hari = request.form['Hari']
        Bulan = request.form['Bulan']
        Waktu_Keberangkatan = request.form['Waktu_Keberangkatan']
        Kapasitas_maksimal_pesawat = request.form['Kapasitas_maksimal_pesawat']
        Jumlah_Penumpang = request.form['Jumlah_Penumpang']
        
        data = np.array([[Namamaskapai,Asal_Bandara,Tujuan_Bandara,Hari,Bulan,Waktu_Keberangkatan,Kapasitas_maksimal_pesawat,Jumlah_Penumpang]])
        my_prediction = model.predict(data)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO kepenuhan (namamaskapai, asal_bandara , tujuan_bandara , hari , bulan , waktu_keberangkatan , kapasitas_maksimal_pesawat , jumlah_penumpang) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (Namamaskapai, Asal_Bandara, Tujuan_Bandara, Hari, Bulan, Waktu_Keberangkatan, Kapasitas_maksimal_pesawat, Jumlah_Penumpang))
        mysql.connection.commit()
        # cur.execute("SELECT  * FROM kepenuhan")
        # data = cur.fetchall()
        cur.close()
        return render_template('analysis.html', prediction_text =  my_prediction, Namamaskapai=Namamaskapai, Asal_Bandara=Asal_Bandara, Tujuan_Bandara=Tujuan_Bandara, Hari=Hari, Bulan=Bulan, Waktu_Keberangkatan=Waktu_Keberangkatan, Kapasitas_maksimal_pesawat=Kapasitas_maksimal_pesawat, Jumlah_Penumpang=Jumlah_Penumpang)
        

@app.route('/tambah',  methods=['POST', 'GET'])
def tambah():
    if request.method == 'GET':
        return render_template("tambah.html")
    else:
        namamaskapai = request.form['Namamaskapai']
        asal_Bandara = request.form['Asal_Bandara']
        tujuan_Bandara = request.form['Tujuan_Bandara']
        hari = request.form['Hari']
        bulan = request.form['Bulan']
        waktu_Keberangkatan = request.form['Waktu_Keberangkatan']
        kapasitas_maksimal_pesawat = request.form['Kapasitas_maksimal_pesawat']
        jumlah_Penumpang = request.form['Jumlah_Penumpang']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO kepenuhan (namamaskapai, asal_bandara , tujuan_bandara , hari , bulan , waktu_keberangkatan , kapasitas_maksimal_pesawat , jumlah_penumpang) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (namamaskapai, asal_Bandara, tujuan_Bandara, hari, bulan, waktu_Keberangkatan, kapasitas_maksimal_pesawat, jumlah_Penumpang))
        mysql.connection.commit()
        # cur.execute("SELECT  * FROM kepenuhan")
        # data = cur.fetchall()
        cur.close()
        return redirect(url_for('home'))

@app.route('/report',  methods=['POST', 'GET'])
def report():
    if request.method == 'GET':
        return render_template("report.html")
    else:
        namamaskapai = request.form['Namamaskapai']
        asal_Bandara = request.form['Asal_Bandara']
        tujuan_Bandara = request.form['Tujuan_Bandara']
        hari = request.form['Hari']
        tanggal = request.form['tanggal']
        bulan = request.form['Bulan']
        waktu_Keberangkatan = request.form['Waktu_Keberangkatan']
        kapasitas_maksimal_pesawat = request.form['Kapasitas_maksimal_pesawat']
        jumlah_Penumpang = request.form['Jumlah_Penumpang']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO report (namamaskapai, asal_bandara , tujuan_bandara , hari , tanggal, bulan , waktu_keberangkatan , kapasitas_maksimal_pesawat , jumlah_penumpang) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (namamaskapai, asal_Bandara, tujuan_Bandara, hari, tanggal, bulan, waktu_Keberangkatan, kapasitas_maksimal_pesawat, jumlah_Penumpang))
        mysql.connection.commit()
        # cur.execute("SELECT  * FROM kepenuhan")
        # data = cur.fetchall()
        cur.close()
        return redirect(url_for('list_report'))


@app.route('/cek_prediksi',  methods=['POST', 'GET'])
def cek_prediksi():
    if request.method == 'GET':
        return render_template("cek_prediksi.html")
    else:
        namamaskapai = request.form['Namamaskapai']
        asal_Bandara = request.form['Asal_Bandara']
        tujuan_Bandara = request.form['Tujuan_Bandara']
        hari = request.form['Hari']
        tanggal = request.form['tanggal']
        # bulan = request.form['Bulan']
        waktu_Keberangkatan = request.form['Waktu_Keberangkatan']
        tanggal1 = datetime.datetime.strptime(tanggal, '%Y-%m-%d')
        today = tanggal1.date()
        yesterday = today - datetime.timedelta(days=7)

        data_sebelumnya = yesterday.strftime("%Y-%m-%d")
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM report WHERE tanggal =%s AND namamaskapai =%s AND asal_bandara =%s AND tujuan_bandara =%s AND hari =%s AND waktu_keberangkatan =%s",(data_sebelumnya,namamaskapai,asal_Bandara,tujuan_Bandara,hari,waktu_Keberangkatan))
        data2 = cur.fetchone()
        cur.close()
        if data2 is not None and len(data2) > 0 :
            data = np.array([[data2['namamaskapai'],data2['asal_bandara'],data2['tujuan_bandara'],data2['hari'],data2['bulan'],data2['waktu_keberangkatan'],data2['kapasitas_maksimal_pesawat'],data2['jumlah_penumpang']]])
            my_prediction = model.predict(data)
        else :
            my_prediction = 10
        # return my_prediction
        return render_template('analisis.html', prediction_text =  my_prediction, Namamaskapai=namamaskapai, Asal_Bandara=asal_Bandara, Tujuan_Bandara=tujuan_Bandara, Hari=hari, tanggal=tanggal, Waktu_Keberangkatan=waktu_Keberangkatan)
        

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
# @app.route('/portofolio')
# def portofolio():
#     if 'email' in session:
#         return render_template("portofolio.html")
#     else:
#         return redirect(url_for('home')) 
# @app.route('/contact')
# def contact():
#     if 'email' in session:
#         return render_template("tambah.html")
#     else:
#         return redirect(url_for('home')) 
 

if __name__ == '__main__':
    app.run(debug=True)

    