from flask import Blueprint, render_template, request, redirect, session
from .db import db
from bson.objectid import ObjectId
from bson import json_util
import json
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
@views.route('/announce/<id>')
def getannounce(id):
    ann = db['announcements'].find_one({"_id": ObjectId(id)})
    session['ann'] = json.loads(json_util.dumps(ann))
    return redirect('/announce')
@views.route('/announce')
def showannounce():
    return render_template('announcement.html')
