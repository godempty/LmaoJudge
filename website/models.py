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

        return jsonify(user), 200 
class Announcement:
    def add(self):
        announce= {
            "author": {
                'type': 'string',
                'minlength': 1,
                'required': True,
            },
            "title": {
                'type': 'string',
                'minlength': 1,
                'required': True,
            },
            "content": {
                'type': 'string',
                'minlength': 1,
                'required': True,
            },
            "time": {
                'type': 'time',
                'required': True,
            }
        }
