from flask import Blueprint, render_template, request, redirect
from .db import db

views = Blueprint('views', __name__)

# @ is the way to create(define) blueprint
@views.route('/')
def home():
    announce = db['announcements'].find()
    return render_template("home.html", announce = announce)
@views.route('/problems')
def problems():
    return render_template("problems.html")
@views.route('/problems/<id>')
def problem_page(id):
    return render_template("problem_page.html", pid=id)
@views.route('/contests')
def contests():
    return render_template("contests.html")
@views.route('/submissions')
def submissions():
    return render_template("submissions.html")
@views.route('/submit/<id>')
def submit(id):
    return render_template("submit.html", id=id)
@views.route('/submit', methods = ['POST', 'GET'])
def getcode():
    if(request.method == 'POST'):
        code = request.form['code']
        print(code)
        return render_template("submissions.html")
    else:
        return 'error'
