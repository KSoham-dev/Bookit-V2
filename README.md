# Bookit V2

A minimalistic e-library application designed to function as a comprehensive Library Management System.

## About The Project

Bookit V2 is an e-library application that serves both users and librarians. It provides an interface for managing a digital library, from book cataloging to user access and reporting. This second version introduces significant improvements in user experience, security, and code organization.

The application is architecturally split into a frontend developed with Vue.js and a backend powered by Flask. The backend now uses Flask Blueprints for a more organized and scalable structure.

### Key Features

**For Users:**
*   **Book Management:** Request, read, and return e-books.
*   **Timed Access:** Borrowed books can be accessed for a maximum of 7 days before access is automatically revoked.
*   **Purchase Options:** Users can buy e-books and use a cart for managing their purchases.
*   **Reporting:** Receive daily reports on personal activity.

**For Librarians:**
*   **Content Management:** Perform full CRUD (Create, Read, Update, Delete) operations on books, library sections, authors, and more.
*   **Request Handling:** Approve or reject book requests from users and manually revoke access to issued books.
*   **Analytics & Reporting:** View statistics related to the book catalog and generate monthly or on-demand CSV reports.

### Improvements in V2
*   **Enhanced User Experience:** The interface has been rebuilt using JavaScript frameworks to provide a smoother and more intuitive user experience.
*   **Improved Security:** Security is strengthened through the implementation of JWT (JSON Web Tokens) for authentication, managed by the Flask-JWT-Extended library.

## Technology Stack

[![My Skills](https://skillicons.dev/icons?i=html,css,js,vue,bootstrap,flask,sqlite,redis)](https://skillicons.dev)

### Backend
*   **Framework:** Flask
*   **ORM:** Flask-SQLAlchemy
*   **Authentication:** Flask-JWT-Extended
*   **Caching:** Flask-Cache, Redis
*   **Database:** SQLite
*   **Task Queue:** Celery

### Frontend
*   **Framework:** Vue.js
*   **Styling:** CSS, Bootstrap
*   **Structure:** HTML
*   **Alerts:** SweetAlert

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

*   Python & Pip
*   Node.js & npm
*   **Redis:** This project uses Redis as a message broker for Celery and for caching. You need to have a Redis server installed and running. You can download it from the official [Redis website](https://redis.io/download).

### Installation & Setup

1.  **Clone the Repo:**
    ```
    git clone https://github.com/KSoham-dev/Bookit-V2.git
    cd Bookit-V2
    ```

2.  **Backend Setup:**
    Navigate to the backend directory and install the required Python packages.
    ```
    cd Backend
    python3 -m venv .env
    source ./env/bin/activate
    pip install -r requirements.txt
    ```

3.  **Frontend Setup:**
    In a new terminal, navigate to the frontend directory and install the npm packages.
    ```
    cd Frontend
    npm install
    ```

### Running the Application

For the application to be fully functional, you need to run the backend server, the frontend server, the Redis server, and the Celery workers.

1.  **Start the Redis Server:**
    Open a new terminal and start your Redis instance. If you installed it via a package manager, it might already be running as a service. Otherwise, run:
    ```
    redis-server
    ```

2.  **Run the Celery Workers:**
    Celery handles background tasks like sending daily reports. In the `backend` directory, open two separate terminals to run the Celery worker and the scheduler (beat).

    *   In the first terminal, start the Celery worker:
        ```
        celery -A main.celery worker --loglevel=info
        ```
    *   In the second terminal, start the Celery beat scheduler:
        ```
        celery -A main.celery beat --loglevel=info
        ```

3.  **Run the Backend Server:**
    In the `backend` directory, start the Flask development server.
    ```
    python main.py
    ```

4.  **Run the Frontend Server:**
    In the `frontend` directory, start the Vue.js development server.
    ```
    npm run dev
    ```

After completing these steps, the application should be accessible at `http://localhost:8080` (or the port specified by the Vue development server).

