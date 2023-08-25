from flask import *
import ibm_db


conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud; PORT=32536; SECURITY=SSL; SSLServerCertificate=DigiCertGlobalRootCA.crt; UID=jbw20899; PWD=fAQLQIVGqkVipQKY",'','')
print(conn)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('logout.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/adminprofile')
def aprofile():
    return render_template('adminprofile.html')

@app.route('/studentprofile')
def sprofile():
    return render_template('studentprofile.html')

@app.route('/facultyprofile')
def fprofile():
    return render_template('facultyprofile.html')

@app.route('/login1',methods=['POST'])
def login1():
    global Userid
    global Username
    msg=''
    EMAIL = request.form['EMAIL']
    PASSWORD = request.form['PASSWORD']
    sql = "SELECT * FROM ADMINREGISTER WHERE EMAIL =? AND PASSWORD=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,EMAIL)
    ibm_db.bind_param(stmt,2,PASSWORD)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print (account)
    print(EMAIL, PASSWORD)
    if account:
            session['Loggedin']=True
            session['id'] =account['EMAIL']
            Userid=account['EMAIL']
            session['EMAIL']=account['EMAIL']
            Username=account['USERNAME']
            Name=account['Name']
            msg="Logged in Successfully"
            sql = "SELECT ROLE FROM ADMINREGISTER WHERE EMAIL =?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,EMAIL)
            ibm_db.execute(stmt)
            rol = ibm_db.fetch_assoc(stmt)
            print(rol)
            if rol['ROLE']==1:
                 print("STUDENT")
                 return render_template("studentprofile.html", msg=msg, user=email, name= Name, role="STUDENT", username=Username, email=email)
            elif rol['ROLE']==2:
                 print("FACULTY")
                 return render_template("facultyprofile.html", msg=msg, user=email, name= Name, role="FACULTY", username=Username, email=email)
            else:
                print("STUDENT")
                return render_template("adminprofile.html", msg=msg, user=email, name= Name, role="ADMIN", username=Username, email=email)
    else:
        msg="Incorrect Email/Password"
    
    return render_template("login.html", msg=msg)

   

@app.route('/register1',methods=['POST'])
def register1():
    x = [x for x in request.form.values()]
    print(x)
    NAME=x[0]
    EMAIL=x[1]
    USERNAME=x[2]
    PASSWORD=x[3]
    ROLE=x[4]
    sql = "SELECT * FROM ADMINREGISTER WHERE EMAIL =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,EMAIL)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        msg="Already Registered"
        return render_template('adminregister.html', error= True, msg=msg)
    else:
        insert_sql = "INSERT INTO  REGISTER VALUES (?, ?, ?, ?, ? )"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, NAME)
        ibm_db.bind_param(prep_stmt, 2, EMAIL)
        ibm_db.bind_param(prep_stmt, 3, USERNAME)
        ibm_db.bind_param(prep_stmt, 4, PASSWORD)
        ibm_db.bind_param(prep_stmt, 5, ROLE)
        ibm_db.execute(prep_stmt)
        msg="Registration Successful"
    return render_template('adminregister.html', msg=msg)


if __name__ == "__main__":
    app.run(debug=True,port = 5000)
