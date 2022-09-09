from .__init__ import db
from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
import uuid
class User:
    def signup(self):
        
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password1'),
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        db.users.insert_one(user)

        return jsonify(user), 200 