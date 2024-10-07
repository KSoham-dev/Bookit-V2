from celery_code.workers import celery
from datetime import datetime, timezone
from celery.schedules import crontab
from flask_mail import Message
from extensions import mail
from flask import render_template
from models import *
import os

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(30,18), send_daily_mail.s(), name='Send_daily_mail')
    sender.add_periodic_task(crontab(00,00,day_of_month="1"), send_monthly_mail.s(), name='Send_montly_mail')
    

@celery.task()
def send_daily_mail():
    users = User.query.all()
    cur_date=datetime.now(timezone.utc)
    for user in users:
        if user.role == "user":
            user_id = user.usr_id 
            isb = db.session.execute(select(issued_books)).all()
            books_owned = []          
            for i in isb:
                if user_id == i[0]:
                    books_owned.append((db.session.get(Book, i[1]).book_name, (cur_date.date() - i[2].date()).days))
            msg = Message (
                subject = "Your daily dose of books is waiting for you !",
                sender = "demobookitv2@gmail.com",
                recipients = [user.email]
            )
            msg.html = render_template("daily_mail.html",user=user,books_owned=books_owned)
            mail.send(msg)
    return "Mail sent"

@celery.task()
def send_monthly_mail():
    users = User.query.all()
    sections = Section.query.all()
    books = Book.query.all()
    all_fdbs = db.session.execute(select(feedback)).all()
    latest_sections = []
    latest_books = []
    latest_fdbks = []
    for sec in sections:
        if ((datetime.now(timezone.utc).date() - sec.date_created.date()).days <= 30):
            latest_sections.append(sec)
    for book in books:
        if ((datetime.now(timezone.utc).date() - book.date_added.date()).days <= 30):
            latest_books.append(book)
    for fdb in all_fdbs:
        if ((datetime.now(timezone.utc).date() - fdb[3].date()).days <= 30):
            latest_fdbks.append((f"{db.session.get(User,fdb[0]).f_name} {db.session.get(User,fdb[0]).l_name}", db.session.get(Book,fdb[1]).book_name, fdb[2], fdb[3].date()))
    for user in users:
        if(user.role == "librarian"):
            msg = Message (
            subject = "Your Monthly report is here !",
            sender = "demobookitv2@gmail.com",
            recipients = [user.email]
            )
            msg.html = render_template('monthly_mail.html',users=users,user=user, latest_sections=latest_sections, latest_books=latest_books, latest_fdbks=latest_fdbks)
            mail.send(msg)
    return "Mail sent"

@celery.task()
def issued_books_csv():
    for u in User.query.all():
        if u.role == "librarian":
            user = u
    msg = Message (
            subject = "Your csv report is here !",
            sender = "demobookitv2@gmail.com",
            recipients = [user.email]
            )
    mail.body = "The csv report you requested is attached with the mail ! Thank you !"
    with open("./static/books_issued.csv", "rb") as fp:
        msg.attach("books_issued.csv", "text/csv", fp.read())
    mail.send(msg)
    os.remove("./static/books_issued.csv")
    return "Sucessful"
    
@celery.task()
def requested_books_csv():
    for u in User.query.all():
        if u.role == "librarian":
            user = u
    msg = Message (
            subject = "Your csv report is here !",
            sender = "demobookitv2@gmail.com",
            recipients = [user.email]
            )
    mail.body = "The csv report you requested is attached with the mail ! Thank you !"
    with open("./static/books_requested.csv", "rb") as fp:
        msg.attach("books_requested.csv", "text/csv", fp.read())
    mail.send(msg)
    os.remove("./static/books_requested.csv")
    return "Sucessful"
