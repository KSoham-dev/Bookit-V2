from flask import Blueprint, jsonify, request
from models import *
from flask_jwt_extended import  jwt_required, current_user
import base64
import random
import matplotlib.pyplot as plt
from io import BytesIO
from extensions import cache
from celery_code import tasks
import csv

lib_bprint = Blueprint('lib', __name__)

@lib_bprint.get('/get_all_req_books')
@jwt_required()
def get_all_req_books():
    d,i = {},0
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    for user in User.query.all():
        i += 1
        d_usr,d_in = {},{}
        d_usr['usr_id'] = user.usr_id
        j = 0
        for book in user.books_requested:
            j += 1
            d_book = {}
            d_book['book_id'] = book.book_id
            d_book['book_name'] = book.book_name
            d_in[j] = d_book
            d_usr['Books'] = d_in                                                   
        d[i] = d_usr
    return jsonify(d)

@lib_bprint.post('/approve_request')
@jwt_required()
def approve_request():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    usr = db.session.get(User, request.get_json()['usr_id'])
    book = db.session.get(Book, request.get_json()['book_id'])
    usr.books_owned.append(book)
    usr.books_requested.remove(book)
    db.session.commit()
    return jsonify({"message": "Book request approved"})

@lib_bprint.post('/reject_request')
@jwt_required()
def reject_request():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    usr = db.session.get(User, request.get_json()['usr_id'])
    book = db.session.get(Book, request.get_json()['book_id'])
    usr.books_requested.remove(book)
    db.session.commit()
    return jsonify({"message": "Book request rejected"})

@lib_bprint.get('/get_all_issued_books')
@jwt_required()
@cache.cached()
def get_all_issued_books():
    d,j = {},0
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    isb = db.session.execute(select(issued_books)).all()
    cur_date=datetime.utcnow().date()
    l = [(i[0], i[1], (cur_date-i[2].date()).days) for i in isb]
    for i in l:
        j +=1
        d_in,d_book = {},{}
        d_in['usr_id'] = i[0]
        d_book['book_id'] = i[1]
        d_book['book_name'] = db.session.get(Book, i[1]).book_name
        d_in['days_issued'] = i[2]
        d_in["book"] = d_book
        d[j] = d_in
    return jsonify(d)

@lib_bprint.post('/revoke_issued_book')
@jwt_required()
def revoke_issued_book():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    usr = db.session.get(User, request.get_json()['usr_id'])
    book = db.session.get(Book, request.get_json()['book_id'])
    usr.books_owned.remove(book)
    db.session.commit()
    return jsonify({"message": "Book revoked"})

@lib_bprint.get('/get_stats')
@jwt_required()
@cache.memoize()
def get_stats():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    d1={}
    for section in Section.query.all():
        d1[section.section_name] = 0
    for user in User.query.all():
        for book in user.books_owned:
            sec = db.session.get(Section, book.section_id).section_name
            d1[sec] += 1
    colors = [plt.cm.Dark2(random.random()) for _ in range(len(d1))]
    plt.bar(d1.keys(),d1.values(),color=colors)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    data1 = base64.b64encode(buf.getbuffer()).decode("ascii")

    d1={}
    for section in Section.query.all():
        d1[section.section_name] = len(section.books)
    fig = plt.figure(figsize=(10, 7))
    plt.pie(d1.values(), labels=d1.keys(), radius=1.5, autopct='%1.1f%%')
    plt.pie([1],colors="w")
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return jsonify({"img1_src": f'data:image/png;base64,{data1}', "img2_src": f'data:image/png;base64,{data}'})

@lib_bprint.get("/issued_books_csv")
@jwt_required()
def issued_books_csv():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    books_issued = db.session.execute(select(issued_books)).all()
    data = []
    for i in books_issued:
        data.append({"user_id": i[0], "user_name": f"{db.session.get(User, i[0]).f_name} {db.session.get(User, i[0]).l_name}", "book_id": i[1], "book_name": db.session.get(Book, i[1]).book_name,"issued_date": i[2].date()})
    with open('./static/books_issued.csv', 'w', newline='') as csvfile:
        head = ['user_id', 'user_name', 'book_id', 'book_name', 'issued_date']
        writer = csv.DictWriter(csvfile, fieldnames=head)
        writer.writeheader()
        writer.writerows(data)
    job = tasks.issued_books_csv.apply_async(countdown=(10))
    return jsonify({"msg": "Successful"}),200

@lib_bprint.get("/requested_books_csv")
@jwt_required()
def requested_books_csv():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    books_req = db.session.execute(select(requested_books)).all()
    data = []
    for i in books_req:
        data.append({"user_id": i[0], "user_name": f"{db.session.get(User, i[0]).f_name} {db.session.get(User, i[0]).l_name}", "book_id": i[1], "book_name": db.session.get(Book, i[1]).book_name})
    with open('./static/books_requested.csv', 'w', newline='') as csvfile:
        head = ['user_id', 'user_name', 'book_id', 'book_name']
        writer = csv.DictWriter(csvfile, fieldnames=head)
        writer.writeheader()
        writer.writerows(data)
    job = tasks.requested_books_csv.apply_async(countdown=10)
    return jsonify({"msg": "Successful"}),200