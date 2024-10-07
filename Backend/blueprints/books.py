import base64
from flask import Blueprint, jsonify, request
from models import *
from flask_jwt_extended import jwt_required, current_user
from extensions import cache
import os


book_bprint = Blueprint('book_bprint', __name__)



@book_bprint.route('', methods=['GET'])
@jwt_required()
@cache.cached()
def get_books():
    all_books = {}
    books = Book.query.all() 
    j=0 
    for book in books:
        bk={}
        d_fb = {}
        i,k=0,0
        aut={}
        pdf_file = open('./static/book_content_pdf/'+book.content,'rb')
        pdf_bytes = pdf_file.read() 
        content = base64.b64encode(pdf_bytes).decode('utf-8')
        jsonify(content=content)
        
        bk['book_id'] = book.book_id
        bk['book_name'] = book.book_name
        bk['book_description'] = book.book_description
        bk['book_content_base64_encoded'] = content
        bk['book_section'] ={"section_id": book.section_id, "section_name": db.session.get(Section, book.section_id).section_name}
        bk['book_price'] = book.price
        l = []
        for author in book.author:
            i+=1
            l.append(author.author_name)
            aut['author_names'] = l
            bk['book_authors'] = aut
        fb = db.session.execute(select(feedback)).all()
        for f in fb:
            if f[0] == book.book_id:
                k+=1
                d_fb[f'feedback{k}'] = f[2]
                bk['book_feedbacks'] = d_fb
        j+=1
        all_books[j] = bk
    return all_books

@book_bprint.post('/book')
@jwt_required()
def get_book():
    book_id = request.get_json()['book_id']
    book = db.session.get(Book, book_id)
    pdf_file = open('./static/book_content_pdf/'+book.content,'rb')
    pdf_bytes = pdf_file.read() 
    content = base64.b64encode(pdf_bytes).decode('utf-8')
    jsonify(content=content)
    bk,i,d_fb={},0,{}
    aut = {}
    bk['book_id'] = book.book_id
    bk['book_name'] = book.book_name
    bk['book_description'] = book.book_description
    bk['book_content_base64_encoded'] = content
    bk['book_section'] = {"section_id": book.section_id, "section_name": db.session.get(Section, book.section_id).section_name}
    bk['book_price'] = book.price
    for author in book.author:
        i+=1
        aut[i] = {}
        aut[i]['author_name'] = author.author_name
        aut[i]['author_id'] = author.author_id
        aut[i]['author_description'] = author.author_description
        bk[f'book_authors'] = aut
    fb_list = db.session.execute(select(feedback)).all()
    j=0
    l_fb=[]
    for fb in fb_list:
        if fb[0] == book_id:
            l_fb.append((db.session.get(User, fb[1]).f_name + " " + db.session.get(User, fb[1]).l_name,fb[2],fb[1]))
            bk['book_feedbacks'] = l_fb
    return jsonify(bk)

@book_bprint.post('/add_book')
@jwt_required()
def add_book():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    book_name = request.get_json()['book_name']
    book_description = request.get_json()['book_description']
    section_id = request.get_json()['section_id']
    price = request.get_json()['price']
    book_content = request.get_json()['content']
    base64.b64encode(base64.b64decode(book_content))
    b = book_content
    bytes = base64.b64decode(b, validate=True)
    content = f'{book_name}.pdf'
    with open(f'./static/book_content_pdf/{book_name}.pdf', 'wb') as f:
        f.write(bytes)
    authors = request.get_json()['authors']
    book = Book.query.filter_by(book_name=book_name).first()
    if book:
        return jsonify({"message": "Book already exists"}), 400
    book = Book(book_name=book_name, book_description=book_description, section_id=section_id, price=price, content=content)
    db.session.add(book)
    for author in authors:
        author = Author.query.filter_by(author_id=author).first()
        if not author:
            return jsonify({"message": "Author does not exist"}), 400
        book.author.append(author)
    db.session.commit()
    return jsonify({"message": "Book added successfully"}), 200

@book_bprint.post('/delete_book')
@jwt_required()
def delete_book():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    book_id = request.get_json()['book_id']
    book = db.session.get(Book, book_id)
    os.remove('./static/book_content_pdf/'+book.content)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200

@book_bprint.post('/update_book')
@jwt_required()
def update_book():
    if current_user.role != 'librarian':
        return jsonify({"message": "Unauthorized"}), 401
    book_id = request.get_json()['book_id']
    book = db.session.get(Book, book_id)
    book_name = request.get_json()['book_name']
    book_description = request.get_json()['book_description']
    book_section_id = request.get_json()['section_id']
    book_price = request.get_json()['price']
    book_author_ids = request.get_json()['authors']
    book_content = request.get_json()['content']
    if book_name:
        book.book_name = book_name
        db.session.commit()
    if book_description:
        book.book_description = book_description
        db.session.commit()
    if book_section_id:
        book_section_id = int(book_section_id)
        book.section_id = book_section_id
        db.session.commit()
    if book_price:
        book.price = int(book_price)
        db.session.commit()
    if book_author_ids:
        auths = [db.session.get(Author, aut_id) for aut_id in book_author_ids]
        book.author = auths
        db.session.commit()
    if book_content:
        try:
            base64.b64encode(base64.b64decode(book_content))
            os.remove(f'./static/book_content_pdf/{book.content}')
            b = book_content
            bytes = base64.b64decode(b, validate=True)
            book_name = db.session.get(Book, book_id).book_name
            book.content = f'{book_name}.pdf'
            db.session.commit()
            with open(f'./static/book_content_pdf/{book_name}.pdf', 'wb') as f:
                f.write(bytes)
        except Exception:
            return "Wrong encoding format, Check again !!!",500
    return jsonify({"message": "Book updated successfully"}), 200