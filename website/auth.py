from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
    
    return render_template("login.html", boolean = True)

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1!=password2 :
            flash('驗證密碼必須與密碼相同', category='error')
        elif len(email) < 4 :
            flash('請輸入正確的email', category='error')
        elif len(password1) < 7 : 
            flash('密碼必須至少有7個字', category='error')
        else:
            flash('註冊成功!',category='success')
    
    return render_template("sign_up.html")
