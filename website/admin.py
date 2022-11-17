from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, session, url_for
from bson.objectid import ObjectId
from os import path
from zipfile import ZipFile
from .model import new_problem
from .db import db

admin = Blueprint('admin', __name__)

@admin.route('/')
def home():
    return render_template("admin/control_list.html")

@admin.route('/addannounce', methods=['POST','GET'])
def addannounce():
    announce = db['announcements'].find()
    if request.method == 'POST':
        today =datetime.now()
        announcement = {
            'title': request.form.get('title'),
            'context': request.form.get('context'),
            'time': f"{today.year}/{today.month}/{today.day}",
            'author': session['user']['name'],
        }

        db['announcements'].insert_one(announcement)
    return render_template("admin/announcescontrol.html", announce = announce)

@admin.route('/addproblems/', methods=['POST','GET'])
def addproblems():
    type = str(request.args.get('sol'))
    if request.method == 'POST':
        problem = new_problem(request)
        zip_data = request.files['test_data']
        zip_obj_data = zip_data.stream._file
        datas = ZipFile(zip_obj_data)
        filenames = datas.namelist()
        filenames = [f_name for f_name in filenames if f_name.endswith('.in')] 
        datas.extractall(path=f"D:/coding/LmaoJudge/test_data/{problem['pid']}", members=filenames)
        #print(test_data.read())
        db['problems'].insert_one(problem)

    return render_template("admin/problemscontrol.html", type = type)

@admin.route('/announcedelete/<id1>')
def delete(id1):
    db['announcements'].delete_one({"_id": ObjectId(id1)})
    return redirect('/admin/addannounce')