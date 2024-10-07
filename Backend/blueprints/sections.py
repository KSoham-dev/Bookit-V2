from flask import Blueprint, jsonify, request
from models import *
from flask_jwt_extended import jwt_required, current_user
from extensions import cache

section_bprint = Blueprint('section_bp', __name__)


@section_bprint.get('')
@cache.cached()
@jwt_required()
def get_sections():
    sections = Section.query.all()
    d_sec,i = {},0
    for section in sections:
        i+=1
        d_in,books_in_sec,j = {},{},0
        d_in['section_id']  = section.section_id
        d_in['section_name'] = section.section_name
        d_in['section_description'] = section.section_description
        d_in['section_date_created'] = str(section.date_created.date())
        for bk in section.books:
            j+=1
            books_in_sec[bk.book_id] = bk.book_name
        d_in['section_books'] = books_in_sec
        d_sec[i] = d_in
    return d_sec

@section_bprint.post('/section')
@jwt_required()
def get_section():
    section_id = request.get_json()['section_id']
    section = db.session.get(Section, section_id)
    d_in,books_in_sec,j = {},{},0
    d_in['section_id']  = section.section_id
    d_in['section_name'] = section.section_name
    d_in['section_description'] = section.section_description
    d_in['section_date_created'] = str(section.date_created.date())
    for bk in section.books:
        j+=1
        books_in_sec[bk.book_id] = bk.book_name
    d_in['section_books'] = books_in_sec
    return d_in

@section_bprint.get('/get_names')
@jwt_required()
def get_section_names():
    sections = Section.query.all()
    d = {}
    for section in sections:
        d[section.section_id] = section.section_name
    return jsonify(d)

@section_bprint.post('/delete_section')
@jwt_required()
def delete_section():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    section_id = request.get_json()['section_id']
    section = db.session.get(Section, section_id)
    db.session.delete(section)
    db.session.commit()
    return jsonify({"message": "Section deleted"})

@section_bprint.post('/update_section')
@jwt_required()
def update_section():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    section_id = request.get_json()['section_id']
    section = db.session.get(Section, section_id)
    sec_name = request.get_json()['section_name']
    sec_desc = request.get_json()['section_description']
    if sec_name:
        section.section_name = sec_name
        db.session.commit()
    if sec_desc:
        section.section_description = sec_desc
        db.session.commit()
    return jsonify({"message": "Section updated"}), 200

@section_bprint.post('/add_section')
@jwt_required()
def add_section():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    section_name = request.get_json()['section_name']
    section_description = request.get_json()['section_description']
    section = Section.query.filter_by(section_name=section_name).first()
    if section:
        return jsonify({"message": "Section already exists"}), 400
    section = Section(section_name=section_name, section_description=section_description)
    db.session.add(section)
    db.session.commit()
    return jsonify({"message": "Section added"}), 200