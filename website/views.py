from flask import Blueprint, render_template

views = Blueprint('views', __name__)

# @ is the way to create(define) blueprint
@views.route('/')
def home():
    return render_template("home.html")
@views.route('/problems')
def problems():
    return render_template("problems.html")
@views.route('/problems/<id>')
def problem_page(id):
    return render_template("problem_page.html", id=id)
@views.route('/contests')
def contests():
    return render_template("contests.html")
@views.route('/submissions')
def submissions():
    return render_template("submissions.html")

