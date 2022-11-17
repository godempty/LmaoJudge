from bson.objectid import ObjectId
from datetime import datetime
from flask import session
from .db import db
def new_problem(request):
    cnt = db['count'].find_one({"name": "problem"})
    count = cnt['count']+1
    db['count'].update_one({"name": "problem"}, {"$set":{"count": count}})
    solution_answer = request.form.get('solution-answer')
    if not solution_answer:
        sol_code = request.form.get('solution-code')
        #run solution code
        # get_answer(sol_code)
    problem = {
        "pid": count,
        "tag": request.form.get('tags'),
        "topcoder": "none", 
        "record": 0, #to check topcoder
        "ac_user": 0.0, #acrate user
        "ac_submission": 0.0, #acrate submission
        "name": request.form.get('name'),
        "statement": request.form.get('statement'),
        "i_format": request.form.get('i_format'), #input format
        "o_format": request.form.get('o_format'), #output format
        "i_sample": request.form.getlist('i_sample[]'),
        "o_sample": request.form.getlist('o_sample[]'),
        "subtask_description": request.form.getlist('subtask_description[]'),
        "subtask_range": request.form.getlist('subtask_range[]'),
        "checker": request.form.get('checker'),
        "solution-answer": solution_answer,
        "notes": request.form.get('notes'),
        "time_limit": request.form.get('time-limit'), #time limit
        "memory_limit": request.form.get('memory-limit'), #memory limit
        "Author": session['user']['name']
    }
    return problem

def new_submission(code, lang, pid, user): 
    subid = db['count'].find_one({"name": 'submission'})['count']+1
    db['count'].update_one({"name": 'submission'}, {'$set': {'count': subid}})

    data = db['problem_test_data'].find_one({'_id': int(pid)})
    today = datetime.now()
    ret = {'_id': subid, 'done': 0, 'code': code, 'lang': lang, 'prob': pid, 'subtask': list(),
            'verdict': '', 'exetime': 0, 'exemem': 0,
            'subtime': f"{today.year}/{today.month}/{today.day}", 'userid': 0}
    for i in data['subtasks']:
        ret['subtask'].append(list())
        for j in range(i['total']):
            ret['subtask'][-1].append(['', 0, 0]) #verdict time memory

    db['submission_data'].insert_one(ret)

    return subid
