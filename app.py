from flask import Flask, render_template, url_for,request, redirect, session
import cgpacal
import sqlite3


app = Flask(__name__)

app.secret_key = '123321'

global cur
con = sqlite3.connect("cgpa.db", check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()
print(cur)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/check',methods=['GET','POST'])
def check():
    if(request.method == "POST"):
        email = request.form.get('email')
        password = request.form.get('password')
        cur.execute("SELECT * FROM users WHERE email='%s' and password='%s'"%(email, password))
        x=cur.fetchone()
        if(x != None ):
            session['loggedin'] = True
            session['username'] = x['username']
            return redirect('/question')
        else:
            return render_template('index.html', msg="Account does not exist!")
        print(email)
        print(password)
        return redirect('/')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if(request.method == "POST"):
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if(password == password2):
            cur.execute("INSERT INTO users VALUES('%s','%s','%s')"%(username, email, password))    #inserting to user
            con.commit()    # executing the above code in mysql workbench
            x=cur.fetchone()
        else:
            return render_template('signup.html', output="Password Missmatch")
        print(x)
        print(email, username)
        print(password)
        return redirect('/')
    return render_template('signup.html')

@app.route('/gpa',methods=['GET','POST'])
def gpa():
    if 'loggedin' in session:
        if(request.method == "POST"):
            dept = request.form.get('dept')
            sem = request.form.get('sem')
            sub1 = request.form.get('sub1')
            sub2 = request.form.get('sub2')
            sub3 = request.form.get('sub3')
            sub4 = request.form.get('sub4')
            sub5 = request.form.get('sub5')
            sub6 = request.form.get('sub6')
            sub7 = request.form.get('sub7')
            sub8 = request.form.get('sub8')
            sub9 = request.form.get('sub9')
            sub10 = request.form.get('sub10')
            print(dept, sem)
            sub_for = "sem"+sem+"subn"
            sub_for1 = "sem"+sem+"credit"
            d = dept.lower()
            cur.execute("SELECT %s FROM %s" %(sub_for, d))
            x=cur.fetchall()
            print(x)
            y = [item[sub_for] for item in x]
            y = list(filter(("null").__ne__, y))
            print(y)
            cur.execute("SELECT %s FROM %s" %(sub_for1, d))
            con.commit()
            xx=cur.fetchall()
            print(xx)
            yy = [item[sub_for1] for item in xx]
            yy = list(filter((0).__ne__, yy))
            print(yy)

            if(sub1 == None):
                return render_template('gpa.html',out3=sem , out1="yes",out2=d.upper(), name=y, cred=yy, out=len(y))
            else:
                grade = [sub1, sub2, sub3, sub4, sub5, sub6, sub7, sub8, sub9, sub10]
                grade = list(filter(None, grade))
                grade = [int(i) for i in grade]
                print(grade)
                gpa=0
                for i in range(len(grade)):
                    gpa+=grade[i]*yy[i]
                gpa=gpa/sum(yy)
                gpa = "{:.2f}".format(gpa)
                return render_template('gpa.html',out1="null",out2=gpa )


        return render_template('gpa.html', out1="no")

    return redirect('/')

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect('/')

@app.route('/question',methods=['GET','POST'])
def question():
    if(request.method == "POST"):
        option = request.form.get('option')
        print(option)
        if(option == "GPA"):
            return redirect('/gpa')
        else:
            return redirect('/cgpa')
    return render_template('question.html')

@app.route('/cgpa',methods=['GET','POST'])
def cgpa():
    if 'loggedin' in session:
        if(request.method == "POST"):
            dept = request.form.get('dept')
            sem = request.form.get('sem')
            print(dept, sem)
            gpa1 = request.form.get('sem1')
            if(gpa1 == None):
                return render_template('cgpa.html', out=int(sem), out1="yes", out2=dept)
            gpa2 = request.form.get('sem2')
            gpa3 = request.form.get('sem3')
            gpa4 = request.form.get('sem4')
            gpa5 = request.form.get('sem5')
            gpa6 = request.form.get('sem6')
            gpa7 = request.form.get('sem7')
            gpa8 = request.form.get('sem8')
            lis = [gpa1, gpa2, gpa3, gpa4, gpa5, gpa6, gpa7, gpa8]
            print(lis)
            res = list(filter(None, lis))
            res = [float(i) for i in res]
            print(res)
            if(dept == "IT"):
                ccgpa = cgpacal.it(res)
            elif(dept == "CSE"):
                ccgpa = cgpacal.cse(res)
            elif(dept == "MECH"):
                ccgpa = cgpacal.mech(res)
            elif(dept == "EEE"):
                ccgpa = cgpacal.eee(res)
            elif(dept == "EIE"):
                ccgpa = cgpacal.eie(res)
            elif(dept == "BIO-TECH"):
                ccgpa = cgpacal.bio(res)
            elif(dept == "CIVIL"):
                ccgpa = cgpacal.civil(res)
            elif(dept == "ECE"):
                ccgpa = cgpacal.ece(res)
            elif(dept == "CHEMICAL"):
                ccgpa = cgpacal.chem(res)
            else:
                print("ERROR :", dept)

            ccgpa = round(ccgpa, 2)
            return render_template('cgpa.html', out=0, out1="null", out2=ccgpa)
        return render_template('cgpa.html', out=0, out1="no")
    return redirect('/')

if __name__ == "__main__":
    app.run()


#
