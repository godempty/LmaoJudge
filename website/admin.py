from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, session, url_for
import hashlib
from bson.objectid import ObjectId
import os
from zipfile import ZipFile
from .model import new_problem
from .db import db

admin = Blueprint('admin', __name__)

@admin.route('/')
def home():
    if(session['user']):
        return render_template("admin/control_list.html")
    else:
        return redirect('/')

@admin.route('/addannounce', methods=['POST','GET'])
def addannounce():
    if(session['user']):
        announce = db['announcements'].find()
        if request.method == 'POST':
            today =datetime.now()
            n_id = hashlib.sha256(str(today).encode()).hexdigest()
            announcement = {
                'title': request.form.get('title'),
                'context': request.form.get('context'),
                'time': f"{today.year}/{today.month}/{today.day}",
                'author': session['user']['name'],
                'id': n_id,
            }

            db['announcements'].insert_one(announcement)
        return render_template("admin/announcescontrol.html", announce = announce)
    else:
        return redirect('/')

@admin.route('/addproblems/', methods=['POST','GET'])
def addproblems():
    if(session['user']):
        type = str(request.args.get('sol'))
        if request.method == 'POST':
            problem = new_problem(request)
            zip_data = request.files['test_data']
            zip_obj_data = zip_data.stream._file
            datas = ZipFile(zip_obj_data)
            # filenames = [f_name for f_name in filenames if f_name.endswith('.in')] 
            os.makedirs(f"test_data/{problem['pid']}")
            datas.extractall(path=f"test_data/{problem['pid']}")
            #print(test_data.read())
            db['problems'].insert_one(problem)

        return render_template("admin/problemscontrol.html", type = type)
    else:
        return redirect('/')

@admin.route('/announcedelete/<id1>')
def delete(id1):
    if(not session['user'] or not session['user']['admin']):
        return redirect('/')
    else:
        db['announcements'].delete_one({"_id": ObjectId(id1)})
        return redirect('/admin/addannounce')
