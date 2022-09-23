from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect
from bson.objectid import ObjectId
from .db import db

admin = Blueprint('admin', __name__)

@admin.route('/')
def home():
    return render_template("admin.html")

@admin.route('/addannounce', methods=['POST','GET'])
def addannounce():
    announce = db['announcements'].find()
    if request.method == 'POST':
        today =datetime.now()
        announcement = {
            'title': request.form.get('title'),
            'context': request.form.get('context'),
            'time': f"{today.year}/{today.month}/{today.day}",
            'author': request.form.get('author')
        }

        db['announcements'].insert_one(announcement)
    return render_template("announcescontrol.html", announce = announce)

@admin.route('/addproblems')
def addproblems():
    return render_template("addproblems.html")

@admin.route('/announcedelete/<id1>')
def delete(id1):
    db['announcements'].delete_one({"_id": ObjectId(id1)})
    return redirect('/admin/addannounce')