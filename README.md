# Flask Task Management Application

A simple Task Management web application built using **Flask**, **MySQL**, **SQLAlchemy**, and **JWT Authentication**.

## Features

- User Registration and Login
- Role-Based Access Control (Admin/User)
- Task Creation and Management
- MySQL Database Integration
- JWT Authentication
- Flask-SQLAlchemy ORM

---

## Prerequisites

- Python 3.10+
- MySQL Server
- Git

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Update the database credentials and secret keys in `config.py`.

```python
class Config:
    SECRET_KEY = "your-secret-key"
    JWT_SECRET_KEY = "your-jwt-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://username:password@localhost:3306/taskdb"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

---

## Database Setup

Start the Flask shell:

```bash
flask shell
```

Create the database tables:

```python
from app import db
from models import User, Task

db.create_all()
```

Exit the shell:

```python
exit()
```

---

## Create the First Admin User

Open Flask shell:

```bash
flask shell
```

Run:

```python
import uuid
from app import db
from models import User

admin = User(
    name="admin_name",
    role="admin",
    email="admin@email.com",
    password="adminpassword",
    public_id=str(uuid.uuid4())
)

db.session.add(admin)
db.session.commit()
```

---

## Running the Application

```bash
flask run
```

The application will be available at:

```text
http://127.0.0.1:5000
```

---

## Project Structure

```text
project/
│
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── templates/
├── static/
└── README.md
```

---

## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- MySQL
- PyMySQL
- HTML
- CSS
- JavaScript

---

## License

This project is intended for educational and learning purposes.
