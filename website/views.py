from re import search
from flask import Blueprint, render_template, request, redirect, session, url_for, jsonify, flash
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
def show_problems():
    problem_counts = db['count'].find_one({"name": "problem"})['count']
    page = int(request.args.get("page",0))
    max_problem_page = int(problem_counts/20)
    if(page > max_problem_page):
        return redirect(f'/problems?page={max_problem_page}')

    problems = db['problems'].find({"pid" : { "$gt" : page*20, "$lt": (page+1)*20 }},{'_id':0,'pid': 1, 'name': 1, 'topcoder': 1, 'ac_user': 1, 'ac_submission': 1})
    # while problems.alive:
    #     print(problems.next()['pid'])
    return render_template("problems.html", problems = problems, page = page, max_problem_page = max_problem_page)

@views.route('/problems/<pid>')
def problem_page(pid):
    
    problem = db['problems'].find_one({"pid": int(pid)})
    if not problem:
        return render_template("/error/problem_not_exist.html")
    lens = len(problem['i_sample'])
    return render_template("problem_page.html", problem = problem, lens=lens)

@views.route('/contests')
def contests():
    return render_template("contests.html")

@views.route('/submissions_list/')
def submissions_list():
    per_page = 10
    all_cnt = db['count'].find_one({"name": "submission"})['count']
    page = int(request.args.get("page",0))
    max_page = int(all_cnt/per_page)
    if(page > max_page):
        return redirect(f'/submissions_list?page={max_page}')

    data = db['submission_data'].find({'_id': {
        '$gte': max(1, all_cnt-(page+1)*per_page+1),
        '$lte': all_cnt-page*per_page}},
        {'verdict': 1, 'lang': 1, 'prob': 1, 'subtime': 1, 'userid': 1}).sort("_id", -1)

    return render_template("submissions.html", data = data)

@views.route('/submit/<id>', methods = ['POST', 'GET'])
def submit(id):
    if(not session.get('user')):
        flash('You Have To Login', category='error')
        return redirect(url_for('views.problem_page', pid=id))

    if(request.method == 'POST'):
        code = request.form['code']
        lang = request.form['lang']

        # create submission
        subid = new_submission(code, lang, id, session['user']['name'])

        #judge in another thread
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
    if not get:
        return render_template('/error/submission_not_exist.html')
    return render_template("single_submission.html", id=id, user=get['userid'], subtime=get['subtime'],
            lang=get['lang'], pid=get['prob'], code=get['code'].splitlines(), task=get['subtask'])

# to respond to frontend ajax
@views.route('/submissions/<id>/get_data')
def get_submission_data(id):
    get = db['submission_data'].find_one({'_id': int(id)})
    return jsonify({'done': get['done'], 'subtask': get['subtask'], 'verdict': get['verdict'], 'err': get['error_msg']})

@views.route('/user/<username>')
def show_user(username):
    userTOshow = db['account'].find_one({'name': username}, {'password': 0})
    if not userTOshow:
        return render_template("error/user_not_found.html")
    return render_template("user_page.html", show = userTOshow)
