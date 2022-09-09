from flask import Flask
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client.LmaoJudge


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'momoeqw i0305 woiuqwhogfw'
    app.config['TEMPLATES_AUTO_RELOAD'] = True      
    app.jinja_env.auto_reload = True
    
    from .views import views
    from .auth import auth
    # prefix = h => /h/something in the bludprint
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

