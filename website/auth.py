from flask import Blueprint, render_template, request, flash
from .db import db 

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
            allaccount = db['account'].find()
            account = allaccount.find_one({'email': email})
            if account['password'] != password:
                flash('密碼錯誤!', category='error')
            else:
                flash('登入成功!',category='success')
    
    return render_template("login.html", boolean = True)

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

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
                'admin': 0,
            }
            allaccount.insert_one(newaccount)
            flash('註冊成功!',category='success')
        
    return render_template("sign_up.html")
