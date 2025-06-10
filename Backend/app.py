from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db, jwt, cache, mail
from models import *
from celery_code import workers


app = Flask(__name__)
app.config.from_pyfile('config.py')

cache.init_app(app)
mail.init_app(app)
CORS(app)
db.init_app(app)
jwt.init_app(app)
celery = workers.celery
celery.conf.update(
    broker_url= app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND'],
    timezone = app.config['CELERY_TIMEZONE'],
)

celery.Task = workers.ContextTask

app.app_context().push()

from blueprints.auth import auth_bprint
from blueprints.user import user_bprint
from blueprints.sections import section_bprint
from blueprints.books import book_bprint
from blueprints.authors import author_bprint
from blueprints.librarian import lib_bprint

app.register_blueprint(auth_bprint,url_prefix='/auth')
app.register_blueprint(user_bprint,url_prefix='/user')
app.register_blueprint(section_bprint,url_prefix='/sections')
app.register_blueprint(book_bprint,url_prefix='/books')
app.register_blueprint(lib_bprint,url_prefix='/lib')
app.register_blueprint(author_bprint,url_prefix='/authors')

@jwt.user_lookup_loader
def user_lkup_handler(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = User.query.filter_by(email=identity).one_or_none()
    return user

@jwt.expired_token_loader
def exp_token_handler(jwt_header, jwt_body):
    return jsonify({"message": "token expired","error" : "token expired"}),401

@jwt.invalid_token_loader
def invalid_token_handler(error):
    return jsonify({"message": "Invalid Signature","error" : "invalid token"}),498

@jwt.unauthorized_loader
def missing_token_handler(error):
    return jsonify({"message": "Missing Authorization Header","error" : "missing token"}),401

@jwt.token_in_blocklist_loader
def tkn_in_blocklist(jwt_header, jwt_data):
    jti = jwt_data["jti"]
    blocked_tkn = TknBlockList.query.filter_by(jti=jti).one_or_none()
    if blocked_tkn:
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
    