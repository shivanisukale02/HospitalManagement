import flask
from flask import Flask,request,render_template,redirect
import sqlite3

con=sqlite3.connect("Hospital.db",check_same_thread=False)
cursor=con.cursor()

listOfTables=con.execute("SELECT name from sqlite_master WHERE type='table' AND name='PATIENT' ").fetchall()

if listOfTables!=[]:
    print("Table already Exists! ")
else:
    con.execute('''CREATE TABLE PATIENT(ID INTEGER PRIMARY KEY AUTOINCREMENT,NAME TEXT,MOBILENUMBER INTEGER,AGE INTEGER,ADDRESS TEXT,
    DOB TEXT,PLACE TEXT,PINCODE INTEGER);''')
print("Table has created successfully")

app=Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        getusername = request.form["username"]
        getpass = request.form["pass"]
    try:
        if getusername == 'admin' and getpass == "12345":
            return redirect("/dashboard")
        else:
            print("Invalid username and password")
    except Exception as e:
        print(e)

    return render_template("/login.html")
@app.route("/dashboard",methods=["GET","POST"])
def dash():
    if request.method == "POST":
        getName = request.form["Name"]
        getMob = request.form["Mobile Number"]
        getAge = request.form["Age"]
        getAddress = request.form["Address"]
        getDOB = request.form["DOB"]
        getPlace = request.form["Place"]

        print(getName)
        print(getMob)
        print(getAge)
        print(getAddress)
        print(getDOB)
        print(getPlace)

        try:
            con.execute("INSERT INTO PATIENT(NAME,MOBILENUMBER,AGE,ADDRESS,DOB,PLACE,PINCODE) VALUES('" + getName + "'," + getMob + "," + getAge + ",'" + getAddress + "','" + getAge + "','" + getDOB + "','" + getPlace + "')")
            print("Successfully Inserted! ")
            con.commit()
            return redirect("/viewall")
        except Exception as e:
            print(e)

    return render_template("dashboard.html")

@app.route("/search",methods =['GET','POST'])
def search():
    if request.method == "POST":
        getMob = request.form["Mobile Number"]
        print(getMob)
        try:
            query = "SELECT * FROM PATIENT WHERE MOBILENUMBER="+getMob
            print(query)
            cursor.execute(query)
            print("SUCCESSFULLY SELECTED!")
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid Mobile number")
            else:
                print(len(result))
                return render_template("search.html", patients=result, status = True)

        except Exception as e:
            print(e)
    return render_template("search.html",patients=[],status = False)

@app.route("/delete", methods =['GET','POST'])
def delete():
    if request.method == "POST":
        getMob = request.form["Mobile Number"]
        print(getMob)
        try:
            con.execute("DELETE FROM PATIENT WHERE MOBILENUMBER="+getMob)
            print("SUCCESSFULLY DELETED!")
            result = cursor.fetchall()

        except Exception as e:
            print(e)
    return render_template("delete.html")

@app.route("/viewall")
def view():
    cursor = con.cursor()
    cursor.execute("SELECT * FROM PATIENT")
    result = cursor.fetchall()
    return render_template("viewall.html", patients=result)

@app.route("/update", methods = ['GET','POST'])
def update():
    if request.method == "POST":
        getMob = request.form["Mobile Number"]
        print(getMob)
        try:
            cursor.execute("SELECT * FROM PATIENT WHERE MOBILENUMBER="+getMob)
            result = cursor.fetchall()
            print("SUCCESSFULLY SELECTED!")
            result=cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid Admission number")
            else:
                print(len(result))
                return render_template("update.html", patients=result)
            return redirect("/viewupdate")
        except Exception as e:
            print(e)
    return render_template("update.html")

@app.route("/viewupdate",methods=["GET","POST"])
def viewupdate():
    if request.method == "POST":
        getName = request.form["Name"]
        getMob = request.form["Mobile Number"]
        getAge = request.form["Age"]
        getAddress = request.form["Address"]
        getDOB = request.form["DOB"]
        getPlace = request.form["Place"]

        print(getName)
        print(getMob)
        print(getAge)
        print(getAddress)
        print(getDOB)
        print(getPlace)

    try:
        cursor.execute("UPDATE PATIENT SET Name='" + getName + "',Mobile Number=" + getMob + ",AGE=" + getAge + ",Address='" + getAddress + "',DOB='" + getDOB + "',Place='" + getPlace + "'")
        con.commit()
        return redirect("/viewall")
    except Exception as e:
        print(e)
    return render_template("/viewupdate.html")

if(__name__) == "__main__":
    app.run(debug=True)