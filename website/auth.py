import re
from flask import Blueprint, render_template, request, flash, session, redirect
from .db import db 
from bson import json_util
import json
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if len(email) < 4 :
            flash('請輸入正確的email', category='error')
        elif len(password) < 7 : 
            flash('密碼必須至少有7個字', category='error')
        else:
            allaccount = db['account']
            account = allaccount.find_one({'email': email})
            if account['password'] != password:
                flash('密碼錯誤!', category='error')
            else:
                session['logged']=True
                session['user'] = json.loads(json_util.dumps(account))
                flash('登入成功!',category='success')
                return redirect('/')
    return render_template("login.html")

@auth.route('/log-out')
def logout():
    session['user'] = False
    session['logged'] = False
    return redirect('/')

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    allaccount = db['account']
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        exist = allaccount.find_one({'email': email})
        if password1!=password2 :
            flash('驗證密碼必須與密碼相同', category='error')
        elif len(name) < 2:
            flash('名稱需要至少2個字', category='error')
        elif len(email) < 4 :
            flash('請輸入正確的email', category='error')
        elif len(password1) < 7 : 
            flash('密碼必須至少有7個字', category='error')
        elif exist:
            flash('此email已被註冊過', category='error')
        else:
            newaccount = {
                'name': name,
                'email': email,
                'password': password1,
                'admin': False,
            }
            allaccount.insert_one(newaccount)
            flash('註冊成功!',category='success')
            redirect('/')
        
    return render_template("sign_up.html", logged = session['logged'])
