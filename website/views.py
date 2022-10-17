from tkinter.tix import Tree
from flask import Blueprint, render_template, request, redirect, session, url_for, jsonify
from .db import db
from .model import new_submission
from .judging import judgement
from bson.objectid import ObjectId
from bson import json_util
import json, threading
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

@views.route('/submissions_list/')
def submissions_list():
    num_per_page = 20
    page = int(request.args.get("page", 0))
    # data = db['submission_data'].find({'_id': {'$gte': cur_num - num_per_page*(page+1), '$lt': cur_num+1 - num_per_page*page}}, {'verdict': 1, 'lang': 1, 'prob': 1, 'subtime': 1, 'userid': 1})
    data = db['submission_data'].find({}, {'verdict': 1, 'lang': 1, 'prob': 1, 'subtime': 1, 'userid': 1}).sort('$natural', -1).limit(num_per_page)
    return render_template("submissions.html", data = data)

@views.route('/submit/<id>', methods = ['POST', 'GET'])
def submit(id):
    if(request.method == 'POST'):
        code = request.form['code']
        lang = request.form['lang']

        # create submission
        subid = new_submission(code, lang, id)

        # #judge in another thread
        td = threading.Thread(target = judgement, args = [id, code, lang, subid])
        td.start()
        return redirect(url_for('views.single_submission', id=subid))

    return render_template("submit.html", id=id)

@views.route('/announce/<id>')
def getannounce(id):
    ann = db['announcements'].find_one({"_id": ObjectId(id)})
    session['ann'] = json.loads(json_util.dumps(ann))
    return redirect('/announce')

@views.route('/announce')
def showannounce():
    return render_template('announcement.html')

@views.route('/submissions/<id>')
def single_submission(id):
    get = db['submission_data'].find_one({'_id': int(id)})
    return render_template("single_submission.html", id=id, user=get['userid'], subtime=get['subtime'],
            lang=get['lang'], pid=get['prob'], code=get['code'].splitlines(), task=get['subtask'])

# to respond to frontend ajax
@views.route('/submissions/<id>/get_data')
def get_submission_data(id):
    get = db['submission_data'].find_one({'_id': int(id)})
    return jsonify({'done': get['done'], 'subtask': get['subtask'], 'verdict': get['verdict']})
