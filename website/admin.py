from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect
from .db import db

admin = Blueprint('admin', __name__)

@admin.route('/')
def home():
    return render_template("admin.html")

@admin.route('/addannounce', methods=['POST','GET'])
def addannounce():
    if request.method == 'POST':
        today =datetime.utcnow()
        announcement = {
            'title': request.form.get('title'),
            'context': request.form.get('context'),
            'time': today,
            'author': request.form.get('author')
        }
        result = db['announcements'].insert_one(announcement)
    return render_template("addannounce.html")
@admin.route('/addproblems')
def addproblems():
    return render_template("addproblems.html")