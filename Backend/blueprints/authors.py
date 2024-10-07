from flask import Blueprint, jsonify, request
from models import *
from flask_jwt_extended import jwt_required,current_user
from extensions import cache

author_bprint = Blueprint('author_bp', __name__)

@author_bprint.get('/get_names')
@jwt_required()
def get_author_names():
    authors = Author.query.all()
    d = {}
    for author in authors:
        d[author.author_id] = author.author_name
    return jsonify(d)

@author_bprint.get('')
@jwt_required()
@cache.cached()
def get_authors():
    authors = Author.query.all()
    d_aut,i = {},0
    for author in authors:
        i+=1
        d_in,j = {},0
        d_in['author_id']  = author.author_id
        d_in['author_name'] = author.author_name
        d_in['author_description'] = author.author_description
        d_aut[i] = d_in
    return d_aut


@author_bprint.post('/delete_author')
@jwt_required()
def delete_author():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    author_id = request.get_json()['author_id']
    author = db.session.get(Author, author_id)
    db.session.delete(author)
    db.session.commit()
    return jsonify({"message": "author deleted"})

@author_bprint.post('/update_author')
@jwt_required()
def update_author():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    author_id = request.get_json()['author_id']
    author = db.session.get(Author, author_id)
    aut_name = request.get_json()['author_name']
    aut_desc = request.get_json()['author_description']
    if aut_name:
        author.author_name = aut_name
        db.session.commit()
    if aut_desc:
        author.author_description = aut_desc
        db.session.commit()
    return jsonify({"message": "author updated"}), 200

@author_bprint.post('/add_author')
@jwt_required()
def add_author():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    author_name = request.get_json()['author_name']
    author_description = request.get_json()['author_description']
    author = Author.query.filter_by(author_name=author_name).first()
    if author:
        return jsonify({"message": "author already exists"}), 400
    author = Author(author_name=author_name, author_description=author_description)
    db.session.add(author)
    db.session.commit()
    return jsonify({"message": "author added"}), 200