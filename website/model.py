from bson.objectid import ObjectId
from flask import session
from .db import db
def new_problem(request):
    cnt = db['count'].find_one({"name": "problem"})
    cnt['count']+=1
    problem = {
        "id": cnt['count'],
        "tag": request.form.get('tag'),
        "topcoder": "none", #
        "record": 0, #to check topcoder
        "ac_user": 0, #acrate user
        "ac_submission": 0, #acrate submission
        "name": request.form.get('name'),
        "description": request.form.get('description'),
        "i_format": request.form.get('i_format'), #input format
        "o_format": request.form.get('o_format'), #output format
        "samples": request.form.get('sample'),
        "hint": request.form.get('hint'),
        "t_limit": request.form.get('t_limit'), #time limit
        "m_limit": request.form.get('m_limit'), #memory limit
        "Author": session['user']['name']
    }
    return problem