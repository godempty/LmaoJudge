from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, session
from bson.objectid import ObjectId
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

@admin.route('/addproblems')
def addproblems():
    return render_template("admin/problemscontrol.html")

@admin.route('/announcedelete/<id1>')
def delete(id1):
    db['announcements'].delete_one({"_id": ObjectId(id1)})
    return redirect('/admin/addannounce')