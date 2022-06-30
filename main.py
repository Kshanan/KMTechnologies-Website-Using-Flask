#------------------------------------------xx: Data Base Connection :XX-----------------------------------------------#
import sqlite3
conn = sqlite3.connect('task2', check_same_thread=False)
cur = conn.cursor()

# Tables created :

# 1.register
# 2.projects
# 3.contact_info
# 4.admin_reg

#------------------------------------------xx: Importing Modules Required :XX---------------------------------------------#

import os
from flask import Flask, render_template, request, flash, redirect, url_for, session ,Response 
app = Flask(__name__)

#-------------------------------------------xx: MAIN PAGE :XX-------------------------------------------------------------#

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/project', methods=['POST','GET'])
def project():
    conn = sqlite3.connect('task2', check_same_thread=False)
    cur = conn.cursor()
    cur.execute('select * from projects')
    dis = cur.fetchall()
    return render_template('project.html',dis=dis)

@app.route('/contactus',methods=['POST','GET'])
def contactus():
    if request.method == 'POST':
        print('i was called with post method')
        fname = request.form['fullname']
        email = request.form['email']
        contact = request.form['contactno']
        if len(contact) > 10:
            flash('Enter 10 digit valid contact','warning')
        else:
            pass
        try:
            print('fname = {} email = {} contact = {} '.format(fname, email,contact))
            cur.execute('insert into contact_info (fname,email,contact) values ("{}","{}",{})'.format(fname,email,contact))
            conn.commit()
            flash('You Request  have been Recieved ! You will be reverted back shortly', 'success')
            return redirect(url_for('contactus'))
        except:
            flash('You have already booked ', 'error')
            flash('we will be calling you shortly!!',  'danger')
            pass
    return render_template('contactus.html')

#-----------------------------------------xx: USER :XX--------------------------------------------------------------------#

#function to get the Logged_in User 
def current_user():
    user = None
    if 'user' in session:
        user = session['user']
        conn = sqlite3.connect('task2', check_same_thread=False)
        cur = conn.cursor()
        cur.execute('select * from register where username = ?',[user])
        user_cur = cur.fetchall()
        print(user_cur)
        user = user_cur[0][1]
    return user

@app.route('/login',methods=['GET','POST'])
def login():
    user = current_user()
    if request.method == 'POST':
        print('i was called with post method')                                                     
        email = request.form['email']
        password = request.form['password']
        print('email = {} password = {}'.format(email,password))
        if email == 'root@mail.com' and password == 'root':
            return redirect(url_for('admin_login'))
        elif email == 'root@mail.com' and password == 'register':
            return redirect(url_for('admin_register'))
        else:
            pass
        cur.execute('select * from register where email="%s" and password="%s" '%(email,password))
        di = cur.fetchall()
        if len(di) == 0:
            flash('Wrong Credentials!!', 'warning')
        else:
            cur.execute('select username from register where email="%s"'%(email))
            usr = cur.fetchone() 
            us = usr[0]
            session['user'] = usr[0]       
            flash('{}'.format(us) +' !!'+ ' Welcome to KM Technologies ')
            return redirect(url_for('user_home'))           
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    user = current_user()
    if request.method == 'POST':
        print('i was called with post method')
        user = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cpass = request.form['cpass']
        if password == cpass:
            pass
        else:
            flash('Passwords Do not Match','Warning!')
            return redirect(url_for('register'))
        try:
            print('user = {} email = {} password = {} rpass = {} '.format(user, email, password, cpass))
            cur.execute('insert into register (username,email,password,cpass) values ("{}","{}","{}","{}")'.format(user,email,password,cpass))
            conn.commit()
            flash('You have been Registered!', 'success')
            return redirect(url_for('login'))
        except:
            flash('Data Exists', 'error')
            flash('Registration Unsuccessful. Try again ',  'danger')
            pass        
    return render_template('register.html')


@app.route('/user_home')
def user_home():
    if not session.get('user'):
        return render_template('login.html')
    else:
        user = current_user()
        return render_template('user_home.html', user=user)

@app.route('/user_project')
def user_project():
    user = current_user()
    conn = sqlite3.connect('task2', check_same_thread=False)
    cur = conn.cursor()
    cur.execute('select * from projects')
    dis = cur.fetchall()
    return render_template('user_project.html',dis=dis,user=user)
    
@app.route('/profile',methods=['POST','GET'])
def profile():
    user = current_user()
    conn = sqlite3.connect('task2', check_same_thread=False)
    cur = conn.cursor()
    cur.execute('select * from register where username = "%s"'%(user))
    eml = cur.fetchall()
    email = eml[0][2]
    psw = eml[0][3] 
    if request.method == 'POST':
        nusername = request.form['nusername']
        nemail = request.form['nemail']
        cfpass = request.form['pass']
        if len(nusername) !=0 and len(nemail) !=0:
            flash('Enter Either Username or Email to Update','Success')
            return redirect(url_for('profile'))
        else:
            pass
        if cfpass == psw and cfpass!=0:
            pass
        else :
            flash('Password is Empty or Password Didnt match','Warning')
            return redirect(url_for('profile'))
        if len(nusername) != 0 and len(cfpass) != 0 and len(nemail) == 0 :
            cur.execute('update register set username="{}"'.format(nusername) +'where email="{}"'.format(email))
            conn.commit()
            session['user'] = nusername
            flash('New Username Updated','Success')
            return redirect(url_for('profile'))
        elif len(cfpass) != 0 and len(nemail) != 0 and len(nusername)==0 :
            cur.execute('update register set email="{}"'.format(nemail)+'where username="{}"'.format(user))
            conn.commit()
            flash('New Email Updated','Success')
            return redirect(url_for('profile'))
        else:
            flash('Enter Either Username or Email to update')
            pass
                        

    return render_template('profile.html', user=user,email=email)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return home()
#------------------------------------------xx: ADMIN :XX-----------------------------------------------------------------#

def current_admin():
    user = None
    if 'admin' in session:
        user = session['admin']
        conn = sqlite3.connect('task2', check_same_thread=False)
        cur = conn.cursor()
        cur.execute('select * from admin_reg where username = ?',[user])
        user_cur = cur.fetchall()
        user = user_cur[0][1]
    return user


@app.route('/admin_login',methods=['POST','GET'])
def admin_login():
    user = current_admin()
    if request.method == 'POST':
        print('i was called with post method')                                                     
        email = request.form['email']
        password = request.form['password']
        print('email = {} password = {}'.format(email,password))
        cur.execute('select * from admin_reg where email="%s" and password="%s" '%(email,password))
        dis = cur.fetchall()
        if len(dis) == 0:
            flash('Wrong Credentials!!', 'warning')
        else:
            cur.execute('select username from admin_reg where email="%s"'%(email))
            usr = cur.fetchone() 
            session['admin'] = usr[0]   
            flash('{}'.format(usr) +' !!'+ ' Welcome to Admin Page')
            return redirect(url_for('admin_home',user=user))     
    return render_template('admin_login.html')

@app.route('/admin_register',methods=['POST','GET'])
def admin_register():
    if request.method == 'POST':
        print('i was called with post method')
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cpass = request.form['cpass']
        if password == cpass:
            pass
        else:
            flash('Passwords Do not Match','Warning!')
            return redirect(url_for('admin_register'))
        try:
            print('user = {} email = {} password = {} rpass = {} '.format(username, email, password, cpass))
            cur.execute('insert into admin_reg (username,email,password,cpass) values ("{}","{}","{}","{}")'.format(username,email,password,cpass))
            conn.commit()
            flash('You have been Registered!', 'success')
            return redirect(url_for('admin_login'))
        except:
            flash('Data Exists', 'error')
            flash('Registration Unsuccessful. Try again ',  'danger')
            pass 
    return render_template('admin_register.html')

@app.route('/admin_home')
def admin_home():
    if not session.get('admin'):
        return render_template('home.html')
    else:
        user = current_admin()
    return render_template('admin_home.html',user=user)

@app.route('/user_dash')
def user_dash():
    user = current_admin()
    conn = sqlite3.connect('task2', check_same_thread=False)
    cur = conn.cursor()
    cur.execute('select * from register')
    dis = cur.fetchall()
    return render_template('user_dash.html',dis=dis,user=user)


@app.route('/admin_logout')
def admin_logout():
    session.pop('admin',None)
    return home()

@app.route('/ad_profile')
def ad_profile():
    user = current_admin()
    conn = sqlite3.connect('task2', check_same_thread=False)
    cur = conn.cursor()
    cur.execute('select * from admin_reg where username = "%s"'%(user))
    eml = cur.fetchall()
    email = eml[0][2]
    return render_template('ad_profile.html',user=user,email=email)


@app.route('/add_project',methods=['POST','GET'])
def add_project():
    user = current_admin()
    conn = sqlite3.connect('task2', check_same_thread=False)
    cur = conn.cursor()
    cur.execute('select * from projects')
    dis = cur.fetchall()
    if request.method == 'POST':
        pid = request.form['pid']
        title = request.form['title']
        print(pid)
        if len(pid) == 0:
            pass
        else:
            print('id delete')
            print(dis)
            delt = 'delete from projects where id = {}'.format(pid)
            cur.execute(delt)
            conn.commit()
            flash('Project with id {}'.format(pid)+' deleted','success')
            return redirect(url_for('add_project'))
        if len(title) == 0:
            flash ('Enter title of project ','warning')
        else:
            description = request.form['description']
            if len(description) == 0:
                flash('Enter Description','warning')
            else :
                pass
            link = request.form['link']
            if len(link) == 0:
                flash('Enter Link','Warning')
            else:
                pass
            ins = 'insert into projects ("title","description","link") values ("{}","{}","{}")'.format(title,description,link)
            cur.execute(ins)
            conn.commit()
            flash('Project Added ','success')
            return redirect(url_for('add_project'))        
    return render_template('add_project.html',user=user,dis=dis)

@app.route('/call_req')
def call_req():
    user = current_admin()
    conn = sqlite3.connect('task2', check_same_thread=False)
    cur = conn.cursor()
    cur.execute('select * from contact_info')
    dis = cur.fetchall()
    return render_template('call_req.html',dis=dis,user=user)

# ----------------------------------------------xx: RunServer :XX------------------------------------------------------#

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=5001)
