from bson.objectid import ObjectId
from datetime import datetime
from flask import session
from .db import db
def new_problem(request):
    cnt = db['count'].find_one({"name": "problem"})
    count = cnt['count']+1
    db['count'].update_one({"name": "problem"}, {"$set":{"count": count}})
    problem = {
        "id": count,
        "tag": request.form.get('tag'),
        "topcoder": "none", #
        "record": 0, #to check topcoder
        "ac_user": 0, #acrate user
        "ac_submission": 0, #acrate submission
        "name": request.form.get('name'),
        "description": request.form.get('description'),
        "i_format": request.form.get('i_format'), #input format
        "o_format": request.form.get('o_format'), #output format
        "sample": request.form.getlist('sample[]'),
        "hint": request.form.get('hint'),
        "t_limit": request.form.get('t_limit'), #time limit
        "m_limit": request.form.get('m_limit'), #memory limit
        "Author": session['user']['name']
    }
    return problem

def new_submission(code, lang, pid): 
    subid = db['count'].find_one({"name": 'submission'})['count']+1
    db['count'].update_one({"name": 'submission'}, {'$set': {'count': subid}})

    data = db['problem_test_data'].find_one({'_id': int(pid)})
    today = datetime.now()
    ret = {'_id': subid, 'done': 0, 'code': code, 'lang': lang, 'prob': pid, 'subtask': list(),
            'verdict': '', 'subtime': f"{today.year}/{today.month}/{today.day}", 'userid': 0}
    for i in data['subtasks']:
        ret['subtask'].append(list())
        for j in range(i['total']):
            ret['subtask'][-1].append(['', 0, 0]) #verdict time memory

    db['submission_data'].insert_one(ret)

    return subid
