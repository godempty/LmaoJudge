from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'momoeqw i0305 woiuqwhogfw'
    
    from .views import views
    from .auth import auth
    # prefix = h => /h/something in the bludprint
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app