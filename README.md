# Bookit
## A minimalistic e-library application
The project discussed below aims to provide an interface for an e-library (i.e. a Library Management System). This application can be used by both users and librarians.
Most of the functionalities remain the same as the previous version wherein the user can request, read and return a book (a book can be accessed for a maximum of 7 days after which access will be revoked),
buy an e-book for a price, cart functionality etc.In the case of a librarian, they can create (add), read, update, or delete books, sections, authors, etc. They can also view book-related statistics,
approve or reject book requests, and revoke access to issued books. Functionality such as monthly report, on demand csv report for librarian and daily report for user have been added in this version.
This version provides a better UX because of the javascript used. The app security is also improved with the usage of JWT tokens (Flask-JWT extended).In terms of code the new code has been split up into
two different parts: backend and frontend. Backend is developed using Vue.js while the backend part still uses flask, the only difference is that now it uses flask blueprints which makes it easy to organize the code.
  
### Technology Stack:  
[![My Skills](https://skillicons.dev/icons?i=html,css,js,vue,bootstrap,flask,sqlite,redis)](https://skillicons.dev)  
- Backend
  - Flask: An python library for developing backend of the web applications Flask-SQLAlchemy: Flask extension used to integrate SQLAlchemy Flask-Cache: Flask extension that adds caching support
  - Flask-JWT-Extended: Flask extension that allows token-based authentication
  - SQLite: It is a database engine
  - Celery: It is a distributed task queue for Python applications
  - Redis: Redis is an in-memory database used for caching and celery tasks/results

- Frontend
  - HTML: Used for creating templates
  - CSS: Used for styling web pages
  - Bootstrap: A simple yet powerful framework used for styling web pages
  - Vue.js: An open-source front end JavaScript framework for building user interfaces
  - SweetAlert: A JavaScript library that allows developers to create beautiful alerts

### Author: Soham S. Kulkarni 
### Contact: sohamkulkarni709@gmail.com
