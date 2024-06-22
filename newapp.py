from flask import Flask,request,session,redirect,url_for,render_template
import psycopg2
import psycopg2.extras


app=Flask(__name__)
app.secret_key="one_of_all"

hostname='localhost'
database='Fest_Management'
username='postgres'
pwd='Yash@1234'
port_id=5432

conn=psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return render_template('home.html')

@app.route('/login',methods=['POST','GET'])
def login():
    cur= conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        print(password)
        print(username)
        query='SELECT * FROM users WHERE username = %s and password=%s;'
        val=(username,password)
        cur.execute(query,val)
        account=cur.fetchone()
        print(account)
        # cur.close()
        if account:
            session['username']=account[1]
            print("successfully loged in")
            query1='select role_id from users where username=%s and password=%s;'
            values=(username,password)
            cur.execute(query1,values)
            account_needed=cur.fetchone()
            cur.close()
            role_id=account_needed['role_id']
            print(role_id)
            return redirect(url_for('which_role',role=role_id,user=username))
        else:
            print("incorect username/password")
            return render_template('login.html',error='invalid username or password')
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    cur1 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST'and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # role_id=request.form['role_id']
        profession=request.form['profession']
        print(profession)
        email=request.form['email']
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        phone_number=request.form['phone_number']
        bio=request.form['bio']
        q1="select role_id from role where name=%s"
        cur1.execute(q1,(profession,))
        acc=cur1.fetchone()
        role_id=acc["role_id"]
        query1='SELECT * FROM users WHERE username = %s'
        query2='SELECT * FROM users WHERE password = %s'
        cur1.execute(query1,(username,))
        account1=cur1.fetchone()
        print(account1)
        cur2.execute(query2,(password,))
        account2=cur2.fetchone()
        print(account2)
        cur1.close
        cur2.close
        if account2 or account1:
            return 'Account already exits'
        else:
            query11="INSERT INTO users (username, email, password,first_name,last_name,phone_number,bio,role_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val=(username,email,password,first_name,last_name,phone_number,bio,role_id)
            cur1.execute(query11,val)
            conn.commit()
            print('You have successfully registered !')
            return redirect(url_for('login'))
    elif request.method=='POST':
        return "plz fill the form"
    return render_template('register.html')



@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))

# @app.route('/which_function/<name>')
# def which_function(name):
#     if name=='first function':
#         return render_template('function1.html')
#     elif name=='second function':
#         return render_template('function2.html')
#     elif name=='third function':
#         return render_template('funtion3.html')
#     elif name=='fourth function':
#         return render_template('funtion4.html')
#     elif name=='fifth function':
#         return render_template('function5.html')
#     return render_template

@app.route('/which role/<int:role>/<user>')
def which_role(role,user):
    # for fest_organizer
    if role==4:
        return render_template('role_4.html',user=user)
    elif role==5:
        return render_template('role_5.html',user=user)
    elif role==3:
        return render_template('role_3.html',user=user)
    elif role==1:
        return render_template('role_1.html',user=user)
    elif role==2:
        return render_template('role_2.html',user=user)

@app.route('/participant',methods=['POST',"GET"])
def participant():
    if request.method=="POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        username=request.form['user_name']
        eventname=request.form['event_name']
        paymentmethod=request.form['payment_method']
        paymentstaus=request.form['payment_status']
        Registration_date=request.form['registration_date']
        q1="select user_id from users where username=%s"
        cur.execute(q1,(username,))
        acc1=cur.fetchone()
        if acc1:
            user_id=acc1['user_id']
        else:
            return "NOT VALID USERNAME"   
        q2="select participant_id from participant where user_id=%s"
        cur.execute(q2,(user_id,))
        acc2=cur.fetchone()
        participant_id=acc2["participant_id"]
        q3="select event_id from event where name=%s"
        cur.execute(q3,(eventname,))
        acc3=cur.fetchone()
        if acc3:
            eventid=acc3["event_id"]
        else:
            return "NOT VALID EVENT_NAME"
        query2="INSERT INTO registration (participant_id, event_id, payment_method,payment_status,registration_date) VALUES (%s,%s,%s,%s,%s)"
        val=(participant_id,eventid,paymentmethod,paymentstaus,Registration_date)
        cur.execute(query2,val)
        conn.commit()
        print("participant Registartion successful")
        return render_template('role_1.html')
    return render_template('participant.html')

@app.route('/event',methods=["POST","GET"])
def event():
    if request.method=="POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        eventname=request.form["eventname"]
        performer=request.form["performer"]
        stime=request.form["stime"]
        etime=request.form["etime"]
        cost=request.form["cost"]
        q1="select performer_id from performer where stage_name=%s"
        cur.execute(q1,(performer,))
        acc=cur.fetchone()
        if acc:
            performer_id=acc["performer_id"]
        else:
            return "NOT A VALID PERFORMER"
        q2="select event_id from event where name=%s"
        cur.execute(q2,(eventname,))
        acc1=cur.fetchone()
        if acc1:
            event_id=acc1["event_id"]
        else:
            return "NOT A VALID EVENT"
        q3="INSERT INTO  performance( event_id, performer_id,start_time,end_time,cost) VALUES (%s,%s,%s,%s,%s)"
        val=(event_id,performer_id,stime,etime,cost)
        cur.execute(q3,val)
        conn.commit()
        print("succesfully inserted in performance")
        return render_template("role_3.html")
    return render_template('event.html')

            



    


@app.route('/role1',methods=["POST","GET"])
def role1():
    if request.method=="POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        username=request.form["user"]
        username2=request.form["user2"]
        q1="select user_id from users where username=%s"
        cur.execute(q1,(username2,))
        acc=cur.fetchone()
        user_id=acc["user_id"]
        s1="participant_"+username2
        s2="registration_"+username2
        q2="select registered_events(%s,%s,%s)"
        val=(user_id,s1,s2)
        cur.execute(q2,val)
        rows=cur.fetchall()
        cur.close()
        return render_template('r1_function_r.html',rows=rows)

@app.route('/role2',methods=["POST","GET"])
def role2():
    if request.method=="POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        username=request.form["user"]
        q1="select user_id from users where username=%s"
        cur.execute(q1,(username,))
        acc=cur.fetchone()
        user_id=acc["user_id"]
        s1="sponsorship_"+username
        q2="select fest_sponsored(%s,%s)"
        val=(user_id,s1)
        cur.execute(q2,val)
        rows=cur.fetchall()
        cur.close()
        return render_template('r2_function_r.html',rows=rows)
    
@app.route('/role3',methods=["POST","GET"])
def role3():
    if request.method=="POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        username=request.form["user"]
        username2=request.form["user2"]
        q1="select user_id from users where username=%s"
        cur.execute(q1,(username2,))
        acc=cur.fetchone()
        user_id=acc["user_id"]
        s1="event_"+username2
        s2="eventperformance_"+username2
        q2="select performers_performing(%s,%s,%s)"
        val=(user_id,s1,s2)
        cur.execute(q2,val)
        rows=cur.fetchall()
        cur.close()
        return render_template('r3_function_r.html',rows=rows)







@app.route('/role4',methods=["POST","GET"])
def role4():
    if request.method== "POST":
        which_function=request.form["function"]
        print(which_function)
        username=request.form['user']
        print(username)
        if which_function=="function1":
            return render_template("r4_function1.html",user=username)
        if which_function=="function2":
            return render_template("r4_function2.html",user=username)
        if which_function=="function3":
            return render_template("r4_function3.html",user=username)
        if which_function=="function4":
            return render_template("r4_function4.html",user=username)
        if which_function=="function5":
            return render_template("r4_function5.html",user=username)
        if which_function=="function6":
            return render_template("r4_function6.html",user=username)
        if which_function=="function7":
            return render_template("r4_function7.html",user=username)



@app.route('/role4_f1',methods=["POST","GET"])
def role4_f1():
    if request.method== "POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        fest_name=request.form["fest_name"]
        print((fest_name))
        q1='select fest_id from fest where name=%s'
        cur.execute(q1,(fest_name,))
        account_need=cur.fetchone()
        fest_id=account_need["fest_id"]
        username=request.form['user']
        print(username)
        print(fest_id)
        s1='festevent_'+username
        s2='festsponsors_'+username
        query="select total_profit_from_fest(%s,%s,%s)"
        cur.execute(query,(s1,s2,fest_id))
        rows=cur.fetchall()
        cur.close()
        return render_template('r4_function1_r.html',rows=rows)
    

@app.route('/role4_f2',methods=["POST","GET"])
def role4_f2():
    if request.method== "POST":
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        fest_name=request.form["fest_name"]
        print((fest_name))
        q1='select fest_id from fest where name=%s'
        cur.execute(q1,(fest_name,))
        account_need=cur.fetchone()
        fest_id=account_need["fest_id"]
        username=request.form['user']
        s1='festevent_'+username
        query="select total_amount_from_ticket(%s,%s)"
        cur.execute(query,(s1,fest_id))
        rows=cur.fetchall()
        cur.close()
        return render_template('r4_function2_r.html',rows=rows)
    
@app.route('/role4_f3',methods=["POST","GET"])
def role4_f3():
    if request.method== "POST":
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        fest_name=request.form["fest_name"]
        print((fest_name))
        q11='select fest_id from fest where name=%s'
        cur.execute(q11,(fest_name,))
        account_need=cur.fetchone()
        fest_id=account_need["fest_id"]
        print(fest_id)
        username=request.form['user']
        print(username)
        s1='festsponsors_'+username
        query="select total_amount_from_sponsors(%s,%s)"
        cur.execute(query,(s1,fest_id))
        rows=cur.fetchall()
        cur.close()
        return render_template('r4_function1_r.html',rows=rows)
    
@app.route('/role4_f4',methods=["POST","GET"])
def role4_f4():
    if request.method== "POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        fest_name=request.form["fest_name"]
        print((fest_name))
        q1='select fest_id from fest where name=%s'
        cur.execute(q1,(fest_name,))
        account_need=cur.fetchone()
        fest_id=account_need["fest_id"]
        username=request.form['user']
        print(username)
        print(fest_id)
        s1='festevent_'+username
        s2='festsponsors_'+username
        query="select perct_ticket_sponsors(%s,%s,%s)"
        cur.execute(query,(s1,s2,fest_id))
        rows=cur.fetchall()
        cur.close()
        return render_template('r4_function1_r.html',rows=rows)
    
@app.route('/role4_f5',methods=["POST","GET"])
def role4_f5():
    if request.method== "POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        fest_name=request.form["fest_name"]
        print((fest_name))
        q1='select fest_id from fest where name=%s'
        cur.execute(q1,(fest_name,))
        account_need=cur.fetchone()
        fest_id=account_need["fest_id"]
        username=request.form['user']
        print(username)
        print(fest_id)
        s1='festevent_'+username
        query="select total_cost_performance(%s,%s)"
        cur.execute(query,(s1,fest_id))
        rows=cur.fetchall()
        cur.close()
        return render_template('r4_function1_r.html',rows=rows)
    
@app.route('/role4_f6',methods=["POST","GET"])
def role4_f6():
    if request.method== "POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        fest_name=request.form["fest_name"]
        print((fest_name))
        q1='select fest_id from fest where name=%s'
        cur.execute(q1,(fest_name,))
        account_need=cur.fetchone()
        fest_id=account_need["fest_id"]
        username=request.form['user']
        print(username)
        print(fest_id)
        s1='festsponsors_'+username
        query="select top_sponsor(%s,%s)"
        cur.execute(query,(s1,fest_id))
        rows=cur.fetchall()
        cur.close()
        return render_template('r4_function1_r.html',rows=rows)
    
@app.route('/role4_f7',methods=["POST","GET"])
def role4_f7():
    if request.method== "POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        fest_name=request.form["fest_name"]
        print((fest_name))
        q1='select fest_id from fest where name=%s'
        cur.execute(q1,(fest_name,))
        account_need=cur.fetchone()
        fest_id=account_need["fest_id"]
        username=request.form['user']
        print(username)
        print(fest_id)
        s1='festevent_'+username
        query="select top_event(%s,%s)"
        cur.execute(query,(s1,fest_id))
        rows=cur.fetchall()
        cur.close()
        return render_template('r4_function1_r.html',rows=rows)
    
@app.route('/role5',methods=["POST","GET"])
def role5():
    if request.method== "POST":
        which_function=request.form["function"]
        print(which_function)
        username=request.form['user']
        print(username)
        if which_function=="function1":
            return render_template("r5_function1.html",user=username)
        elif which_function=="function2":
            return render_template("r5_function2.html",user=username)

@app.route('/role5_f1',methods=["POST","GET"])
def role5_f1():
    if request.method== "POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sdate=request.form["sdate"]
        edate=request.form["edate"]
        username=request.form["user"]
        s1='performance_'+username
        s2='performer_'+username
        print(sdate)
        print(edate)
        q1='select user_id from users where username=%s'
        cur.execute(q1,(username,))
        account_need=cur.fetchone()
        user_id=account_need["user_id"]
        query="select events_to_perform(%s,%s,%s,%s,%s)"
        val=(user_id,sdate,edate,s1,s2)
        cur.execute(query,val)
        rows=cur.fetchall()
        cur.close()
        return render_template('r5_function_r.html',rows=rows)
    
@app.route('/role5_f2',methods=["POST","GET"])
def role5_f2():
    if request.method=="POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        username=request.form['user']
        q1='select user_id from users where username=%s'
        cur.execute(q1,(username,))
        account_need=cur.fetchone()
        user_id=account_need["user_id"]
        q2="select stage_name from performer where user_id=%s"
        cur.execute(q2,(user_id,))
        rows=cur.fetchall()
        cur.close()
        return render_template('r5_function2_r.html',rows=rows,user=username)

@app.route('/role5_f2_final',methods=['POST',"GET"])
def role5_f2_final():
    if request.method=="POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        stage_name=request.form["stagename"]
        username=request.form['user']
        print(stage_name)
        q1="select performer_id from performer where stage_name=%s"
        cur.execute(q1,(stage_name,))
        account=cur.fetchone()
        performer_id=account["performer_id"]
        s1="performance_"+username
        q2="select locations_performance(%s,%s)"
        val=(performer_id,s1)
        cur.execute(q2,val)
        rows=cur.fetchall()
        cur.close()
        return render_template('r5_function2_rfinal.html',rows=rows)










        
    




        





if __name__=="__main__":
    app.run(debug=True)





