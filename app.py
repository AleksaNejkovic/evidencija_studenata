from flask import Flask, render_template, url_for, request,redirect, session,Response
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

konekcija=mysql.connector.connect(
		host='localhost',
		port='3306',
		user='root',
		passwd='',
		database='evidencija_studenata'
	)

kursor=konekcija.cursor(dictionary=True);

app=Flask(__name__)

app.secret_key='nasTajniKljuc'

def ulogovan():
 if 'ulogovani_korisnik' in session:
 	return True
 else:
 	return False


@app.route('/')
def index():
	return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method=='GET':
		return render_template('login.html')
	elif request.method=='POST':
		forma=request.form
		upit="SELECT * FROM korisnici WHERE email=%s"
		vrednost=(forma['email'],)
		kursor.execute(upit, vrednost)
		korisnik=kursor.fetchone()
		if check_password_hash(korisnik['lozinka'], forma['lozinka']):
			session['ulogovani_korisnik']=str(korisnik)
			return redirect(url_for('studenti'))
		else:
			return render_template('login.html')

@app.route('/logout', methods=['GET','SET'])
def logout():
	if ulogovan():
		session.pop('ulogovani_korisnik', None)
		return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))

@app.route('/studenti', methods=['GET','POST'])
def studenti():
	if ulogovan():
		upit="SELECT * FROM studenti"
		kursor.execute(upit)
		data=kursor.fetchall()
		return render_template('studenti.html',studenti=data)
	else:
		return redirect(url_for('login'))


@app.route('/novi_student', methods=['GET','POST'])
def novi_student():
	if ulogovan():
		if(request.method=='GET'):
			return render_template('novi_student.html')
		elif request.method=='POST':
			forma=request.form
			upit=""" INSERT INTO studenti(broj_indexa,ime, ime_roditelja, prezime,email,broj_telefona,godina_studija,datum_rodjenja,JMBG)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) """
			vrednosti=(forma['brIndex'],forma['ime'],forma['imeRoditelja'],forma['prezime'],forma['email'],forma['brojTelefona'],forma['godStud'],forma['datRodjenja'],forma['jmbg'])
			kursor.execute(upit,vrednosti)
			konekcija.commit()
			return redirect(url_for('studenti'))
	else:
		return redirect(url_for('login'))

@app.route('/studenti_brisanje/<id>', methods=['GET','POST'])
def studenti_brisanje(id):
	if ulogovan():
	    upit = """ DELETE FROM studenti WHERE id=%s """
	    vrednost = (id,)
	    kursor.execute(upit, vrednost)
	    konekcija.commit()
	    return redirect(url_for('studenti'))
	else:
		return redirect(url_for('login'))

@app.route('/student/<id>', methods=['GET', 'POST'])
def student(id):
    if ulogovan():
        upit = "SELECT * FROM studenti WHERE id=%s"
        vrednost = (id,)
        kursor.execute(upit, vrednost)
        student = kursor.fetchone()
        upit = "SELECT * FROM predmeti"
        kursor.execute(upit)
        predmeti = kursor.fetchall()
        upit = """
            SELECT *
            FROM predmeti
            JOIN ocene 
            ON predmeti.id=ocene.predmet_id
            WHERE ocene.student_id=%s
        """
        vrednost = (id,)
        kursor.execute(upit, vrednost)
        ocene = kursor.fetchall()
        return render_template("student.html", studenti=student, predmeti=predmeti, ocene=ocene)
    else:
        return redirect(url_for('login'))

@app.route('/student_izmena/<id>', methods=['GET','POST'])
def student_izmena(id):
	if ulogovan():
	    if request.method == 'GET':
	        upit = "SELECT * FROM studenti WHERE id=%s"
	        vrednost = (id,)
	        kursor.execute(upit, vrednost)
	        studenti = kursor.fetchone()
	        return render_template('student_izmena.html', studenti=studenti)
	    elif request.method == 'POST':
	        upit = """UPDATE studenti SET 
	        	    	broj_indexa=%s,
	                    ime=%s,
	                    ime_roditelja=%s,
	                    prezime=%s,
	  		    		email=%s,
	  		    		broj_telefona=%s,
	                    godina_studija=%s,
	                    datum_rodjenja=%s,
	                    JMBG=%s
	                    WHERE id=%s    
	                """
	        forma = request.form
	        vrednosti=(forma['brIndex'],forma['ime'],forma['imeRoditelja'],forma['prezime'],forma['email'],forma['brojTelefona'],forma['godStud'],forma['datRodjenja'],forma['jmbg'],id)
	        kursor.execute(upit, vrednosti)
	        konekcija.commit()
	        return redirect(url_for('studenti'))
	else:
		return redirect(url_for('login'))

@app.route('/predmeti', methods=['GET', 'POST'])
def predmeti():
	if ulogovan():
		upit="SELECT * FROM predmeti"
		kursor.execute(upit)
		data=kursor.fetchall()
		return render_template('predmeti.html',predmeti=data)
	else:
		return redirect(url_for('login'))
@app.route('/novi_predmet', methods=['GET', 'POST'])
def novi_predmet():
	if ulogovan():
		if(request.method=='GET'):
			return render_template('novi_predmet.html')
		elif request.method=='POST':
			forma=request.form
			upit=""" INSERT INTO predmeti(sifra, naziv, godina_studija, ESPB, obavezni_izborni)VALUES(%s,%s,%s,%s,%s) """
			vrednosti=(forma['sifra'],forma['naziv'],forma['godstud'],forma['espb'],forma['obvIzb'])
			kursor.execute(upit,vrednosti)
			konekcija.commit()
			return redirect(url_for('predmeti'))
	else:
		return redirect(url_for('login'))

@app.route('/predmet_izmena/<id>', methods=['GET', 'POST'])
def predmet_izmena(id):
	if ulogovan():
	    if request.method == 'GET':
	        upit = "SELECT * FROM predmeti WHERE id=%s"
	        vrednost = (id,)
	        kursor.execute(upit, vrednost)
	        predmet = kursor.fetchone()
	        return render_template('predmet_izmena.html', predmeti=predmet)
	    elif request.method == 'POST':
	        upit = """UPDATE predmeti SET 
	                    sifra=%s,
	                    naziv=%s,
	                    godina_studija=%s,
	                    ESPB=%s,
	                    obavezni_izborni=%s
	                    WHERE id=%s    
	                """
	        forma = request.form
	        vrednosti=(forma['sifra'],forma['naziv'],forma['godStud'],forma['espb'],forma['obvIzb'],id)
	        kursor.execute(upit, vrednosti)
	        konekcija.commit()
	        return redirect(url_for('predmeti'))
	else:
		return redirect(url_for('login'))

@app.route('/predmet_brisanje/<id>', methods=['GET','POST'])
def predmet_brisanje(id):
	if ulogovan():

	    upit = """ DELETE FROM predmeti WHERE id=%s """
	    vrednost = (id,)
	    kursor.execute(upit, vrednost)
	    konekcija.commit()
	    return redirect(url_for('predmeti'))
	else:
		return redirect(url_for('login'))


@app.route('/korisnici')
def korisnici():
	if ulogovan():
		upit="SELECT * FROM korisnici"
		kursor.execute(upit)
		data=kursor.fetchall()
		return render_template('korisnici.html', korisnici=data)
	else:
		return redirect(url_for('login'))

@app.route('/novi_korisnik', methods=['GET', 'POST'])
def novi_korisnik():
	if ulogovan():

		if(request.method=='GET'):
			return render_template('novi_korisnik.html')
		elif request.method=='POST':
			forma=request.form
			upit=""" INSERT INTO korisnici(ime, prezime, email, lozinka)VALUES(%s, %s, %s, %s) """
			hesovana_lozinka=generate_password_hash(forma['sifra'])
			vrednosti=(forma['ime'],forma['prezime'],forma['email_nk'],hesovana_lozinka)
			kursor.execute(upit, vrednosti)
			konekcija.commit()
			return redirect(url_for('korisnici'))
	else:
		return redirect(url_for('login'))


@app.route('/korisnik_izmena/<id>', methods=['GET', 'POST'])
def korisnik_izmena(id):
	if ulogovan():

	    if request.method == 'GET':
	        upit = "SELECT * FROM korisnici WHERE id=%s"
	        vrednost = (id,)
	        kursor.execute(upit, vrednost)
	        korisnik = kursor.fetchone()
	        return render_template('korisnik_izmena.html', korisnik=korisnik)
	    elif request.method == 'POST':
	        upit = """UPDATE korisnici SET 
	                    ime=%s,
	                    prezime=%s,
	                    email=%s,
	                    lozinka=%s
	                    WHERE id=%s    
	                """
	        forma = request.form
	        hesovana_lozinka=generate_password_hash(forma['lozinka'])
	        vrednosti = (forma['ime'],forma['prezime'],forma['email'],hesovana_lozinka, id)
	        kursor.execute(upit, vrednosti)
	        konekcija.commit()
	        return redirect(url_for('korisnici'))  
	else:
		return redirect(url_for('login'))

@app.route('/korisnik_brisanje/<id>', methods=['GET','POST'])
def korisnik_brisanje(id):
	if ulogovan():

	    upit = """ DELETE FROM korisnici WHERE id=%s """
	    vrednost = (id,)
	    kursor.execute(upit, vrednost)
	    konekcija.commit()
	    return redirect(url_for('korisnici'))
	else:
		return redirect(url_for('login'))

@app.route("/ocena_nova/<id>", methods=["POST"])
def ocena_nova(id):
    if ulogovan():
        # Dodavanje ocene u tabelu ocene
        upit = """
            INSERT INTO ocene(student_id, predmet_id, ocena, datum)
            VALUES(%s, %s, %s, %s)
        """
        forma = request.form
        vrednosti = (id, forma['predmet_id'], forma['ocena'], forma['datum'])
        kursor.execute(upit, vrednosti)
        konekcija.commit()
        # Racunanje proseka ocena
        upit = "SELECT AVG(ocena) AS rezultat FROM ocene WHERE student_id=%s"
        vrednost = (id,)
        kursor.execute(upit, vrednost)
        prosek_ocena = kursor.fetchone()
        # Racunanje ukupno espb
        upit = "SELECT SUM(espb) AS rezultat FROM predmeti WHERE id IN (SELECT predmet_id FROM ocene WHERE student_id=%s)"
        vrednost = (id,)
        kursor.execute(upit, vrednost)
        espb = kursor.fetchone()
        # Update tabele student
        upit = "UPDATE studenti SET espb=%s, prosek_ocena=%s WHERE id=%s"
        vrednosti = (espb['rezultat'], prosek_ocena['rezultat'], id)
        kursor.execute(upit, vrednosti)
        konekcija.commit()
        return redirect(url_for('student', id=id))
    else:
        return redirect(url_for('login'))


@app.route('/ocena_brisanje/<student_id>/<ocena_id>')
def ocena_brisanje(student_id, ocena_id):
    if ulogovan():
        upit = "DELETE FROM ocene WHERE id=%s"
        vrednost=(ocena_id,)
        kursor.execute(upit, vrednost)
        konekcija.commit()
        # Racunanje proseka ocena
        upit = "SELECT AVG(ocena) AS rezultat FROM ocene WHERE student_id=%s"
        vrednost = (student_id,)
        kursor.execute(upit, vrednost)
        prosek_ocena = kursor.fetchone()
        # Racunanje ukupno espb
        upit = "SELECT SUM(espb) AS rezultat FROM predmeti WHERE id IN (SELECT predmet_id FROM ocene WHERE student_id=%s)"
        vrednost = (student_id,)
        kursor.execute(upit, vrednost)
        espb = kursor.fetchone()
        # Update tabele student
        upit = "UPDATE studenti SET espb=%s, prosek_ocena=%s WHERE id=%s"
        vrednosti = (espb['rezultat'], prosek_ocena['rezultat'], student_id)
        kursor.execute(upit, vrednosti)
        konekcija.commit()
        return redirect(url_for('student', id=student_id))
    else:
        return redirect(url_for('login'))

app.run(debug=True)

