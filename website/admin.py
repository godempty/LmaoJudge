from flask import Blueprint, render_template, request, redirect
from .db import db

admin = Blueprint('admin', __name__)

@admin.route('/')
def home():
    return render_template("admin.html")