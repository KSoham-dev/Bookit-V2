from flask import Blueprint, jsonify, request
from models import *
from flask_jwt_extended import  jwt_required, current_user
import base64

user_bprint = Blueprint('user', __name__)


@user_bprint.get("/books")
@jwt_required()
def user_view_user_books():
    usr = current_user
    user_id = usr.usr_id 
    isb = db.session.execute(select(issued_books)).all()
    cur_date=datetime.utcnow()
    d,k={},0            
    for i in isb:
        if user_id == i[0]:
            d_in = {}
            bk_id = db.session.get(Book, i[1]).book_id
            book = db.session.get(Book, bk_id)
            k+=1
            d_in["days_passed"] = (cur_date.date() - i[2].date()).days
            d_in["book_name"] = book.book_name
            authors = []
            for author in book.author:
                authors.append(author.author_name)
                d_in['authors'] = authors
                d_in['book_id'] = book.book_id
            d[k] = d_in
    return jsonify(d)

@user_bprint.post("/return_book")
@jwt_required()
def user_return_book():
    book_id = request.get_json()['book_id']
    user_id = current_user.usr_id
    user = db.session.get(User, user_id)
    books_owned = user.books_owned
    for book in books_owned:
        if (book.book_id == book_id):
            user.books_owned.remove(book)
            db.session.commit()
            return {"Status":"Successful"}, 200
        
@user_bprint.get("/view_req_books")
@jwt_required()
def user_view_req_books():
    user_id = current_user.usr_id
    user=db.session.get(User, user_id)
    books=user.books_requested
    books_req,k = {},0
    for book in books:
        book_dict = {}
        book_dict['book_name'] = book.book_name
        book_dict['book_id'] = book.book_id
        authors = []
        for author in book.author:
            authors.append(author.author_name)
        book_dict['authors'] = authors  
        k+=1
        books_req[k] = book_dict
    return jsonify(books_req)        
        
@user_bprint.post("/cancel_book_req")
@jwt_required()
def user_cancel_book_req():
    user_id = current_user.usr_id
    user = db.session.get(User, user_id)
    book_id = request.get_json()['book_id']
    books_req = user.books_requested
    for book in books_req:
        if (book.book_id == book_id):
            user.books_requested.remove(book)
            db.session.commit()
            return {"Status":"Successful"}, 200
        
@user_bprint.get("/user_book_info")
@jwt_required()
def user_book_info():
    user_id = current_user.usr_id
    user = db.session.get(User, user_id)
    books_owned = []
    books_req = []
    for book in user.books_owned:
        books_owned.append(int(book.book_id))
    for book in user.books_requested:
        books_req.append(int(book.book_id))
    return {"owned_books":books_owned, "requested_books":books_req}, 200

@user_bprint.post("/create_cart")
@jwt_required()
def create_cart():
    user_id = current_user.usr_id
    cart=Cart(user_id=user_id)
    db.session.add(cart)
    db.session.commit()
    return jsonify({"msg":"Cart Created Successfully"}), 200

@user_bprint.post("/add_to_cart")
@jwt_required()
def add_to_cart():
    user_id = current_user.usr_id
    book_id = request.get_json()['book_id']
    book=db.session.get(Book, book_id)
    cart=Cart.query.filter_by(user_id=user_id).first()
    if book not in cart.book:
            cart.book.append(book)
            db.session.commit()
            return jsonify({"msg": "Book added sucessfully"}), 200
    else:
        return jsonify({"msg": "Book is in the cart already"}), 200
    
@user_bprint.get("/check_cart")
@jwt_required()
def check_cart_status():
    user_id = current_user.usr_id
    cart=Cart.query.filter_by(user_id=user_id).first()
    if cart is None:
        return jsonify({"msg": "Cart is not present"}), 200
    else:
        return jsonify({"msg": "Cart is present"}), 200
    
@user_bprint.get("/get_cart")
@jwt_required()
def user_cart():
    user_id = current_user.usr_id
    cart=Cart.query.filter_by(user_id=user_id).first()
    if cart:
        products=cart.book
        d,i = {},0
        for p in products:
            d_in  = {}
            pdf_file = open('./static/book_content_pdf/'+p.content,'rb')
            pdf_bytes = pdf_file.read() 
            content = base64.b64encode(pdf_bytes).decode('utf-8')
            d_in["book_id"] = p.book_id
            d_in["book_name"] = p.book_name
            d_in["book_price"] = p.price
            d_in["book_content"] = content
            i+=1
            d[i] = d_in
        return jsonify(d), 200
    else:
        return jsonify({"msg": "No cart found"}), 200

@user_bprint.post("/remove_from_cart")
@jwt_required()
def remove_from_cart():
    usr_id = current_user.usr_id
    bk_id = request.get_json()['book_id']
    book=db.session.get(Book, bk_id)
    cart=Cart.query.filter_by(user_id=usr_id).first()
    if book in cart.book:
        cart.book.remove(book)
        db.session.commit()
        return jsonify({"msg": "Book removed sucessfully"}), 200
    else:
        return jsonify({"msg": "Book is not in the cart"}), 200
    
@user_bprint.post("/request_book")
@jwt_required()
def user_req_book():
    book_id = request.get_json()['book_id']
    user = current_user
    book=db.session.get(Book, book_id)
    user.books_requested.append(book)
    db.session.commit()
    return jsonify({"msg": "Book requested sucessfully"}), 200

@user_bprint.post("/remove_feedback")
@jwt_required()
def user_remove_feedback():
    book_id = request.get_json()['book_id']
    user_id = current_user.usr_id
    book = db.session.get(Book, book_id)
    feedbacks = book.feedbacks
    for feedback in feedbacks:
        if (user_id == feedback.usr_id):
            feedbacks.remove(feedback)
            db.session.commit()

@user_bprint.post("/add_feedback")
@jwt_required()
def user_add_feedback():
    fdb = request.form.get("feedback")
    user_id = current_user.usr_id
    book_id = request.get_json()['book_id']
    fdb = request.get_json()['feedback']
    db.session.execute(feedback.insert().values(usr_id=user_id, book_id=book_id, feedback=fdb))
    db.session.commit()
    return jsonify({"msg": "Feedback added successfully"}), 200

@user_bprint.post("/search")
def search_for():
    books = Book.query.all()
    if request.method == "POST":
        item = request.get_json()['item']
        item = "%".join(item.split())
        results = Book.query.filter(db.func.replace(Book.book_name, ' ', '').ilike('%' + bindparam('item') + '%')).params(item=item).all()
        if results==[]:
            results = Section.query.filter(db.func.replace(Section.section_name, ' ', '').ilike('%' + bindparam('item') + '%')).params(item=item).all()
        if results==[]:
            results = Author.query.filter(db.func.replace(Author.author_name, ' ', '').ilike('%' + bindparam('item') + '%')).params(item=item).all()
        flag_books = set(results).issubset(set(books))
        d,j,l_book_ids,l_book_names = {},0,[],[]
        for i in results:
            if i in Section.query.all():
                j +=1
                sec_books = {}
                for book in i.books:
                    sec_books[book.book_id] = book.book_name
                d_sec = {
                    "section_id": i.section_id,
                    "section_name": i.section_name,
                    "section_description": i.section_description,
                    "section_books": sec_books
                }
                d[str(j)] = d_sec
                d["object"] = "section"
            elif i in Author.query.all():
                j +=1
                aut_books = {}
                for book in i.books:
                    aut_books[book.book_id] = book.book_name
                d_aut = {
                    "author_id": i.author_id,
                    "author_name": i.author_name,
                    "author_books": aut_books,
                    "author_description": i.author_description
                }
                d[str(j)] = d_aut
                d["object"] = "author"
            else:
                l_book_ids.append(i.book_id)
                l_book_names.append(i.book_name)
                d = {
                    "book_ids": l_book_ids,
                    "book_names": l_book_names,
                    "object": "book"
                }
        return jsonify({"results": d}), 200
        

    

      