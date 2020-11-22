from flask import Flask,render_template,request
from flask import Flask, render_template, redirect, url_for, request
import sqlite3
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/employee', methods=['POST','GET'])
def saveDetails():
    #msg = 'msg'
    if request.method == 'POST':
        try:
            name = request.form['name']
            empid = request.form['empid']
            location = request.form['location']
            phone_number = request.form['phone_number']
            email = request.form['email']
            joining_date = request.form['joining_date']
            last_date = request.form['last_date']
            with sqlite3.connect('employee.db') as con:
                cur = con.cursor()
                cur.execute("INSERT into Employees (name,empid,location,phone_number,email,joining_date,last_date) values (?,?,?,?,?,?,?)",(name,empid,location,phone_number,email,joining_date,last_date))
                con.commit()
                msg="Employee ADDED Successfully"
        except:
            con.rollback()
            msg="cant add the employee to the list"
        finally:
            return render_template('success.html',msg=msg)
            con.close()

@app.route('/employee_details')
def view():
    con=sqlite3.connect('employee.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employees order by name ASC")
    rows = cur.fetchall()
    print("rows: ",rows)
    return render_template('view.html',rows=rows)

@app.route('/employee_details/<emp_id>')
def one_view(emp_id):
    con=sqlite3.connect('employee.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employees where empid=?",[emp_id])
    rows = cur.fetchall()
    print(rows)
    return render_template('edit.html',rows=rows)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('delete'))
    return render_template('login1.html', error=error)



@app.route("/login/delete")
def delete():
    con = sqlite3.connect('employee.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employees order by name ASC")
    rowss = cur.fetchall()
    print(rowss)
    return render_template("delete.html",rowss = rowss)

@app.route("/deleterecord",methods=['POST'])
def deleterecord():

    empid=request.form['empid']
    with sqlite3.connect("employee.db") as con:
        # cur = con.cursor()
        # # cur.execute("select * from Employees")
        # # rows = cur.fetchall()
        # # return str(rows)
        # cur.execute("delete from Employees where empid = ?",[empid])
        # ms = cur.fetchall()
        # msg = "record Added"
        # return str(ms)
        try:
            cur = con.cursor()
            cur.execute("delete from Employees where empid = ?",[empid])
            msg = "record Deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_records.html",msg=msg)
if __name__ == '__main__':
    app.run(debug=True)
