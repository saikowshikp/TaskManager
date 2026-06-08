from extensions import db, admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from config import Config
import jwt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.Text)
    role = db.Column(db.String(50), default="User")
    tasks = db.relationship("Task", back_populates="user")

    def __str__(self):
        return self.email

    def __repr__(self):
        return f"<User {self.email}>"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_user_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()
    
    def get_tasks(self):
        return Task.get_tasks_of_user(self.id)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete()
        db.session.commit()


class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    user = db.relationship("User", back_populates="tasks")

    @classmethod
    def get_task_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def get_tasks_of_user(cls, user_id):
        return cls.query.filter_by(user_id = user_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def modify(self, new_title, new_description):
        self.title = new_title
        self.description = new_description
        db.session.commit()

class TaskView(ModelView):
    form_columns = ["title", "description", "user"]
    column_list = ["title", "description", "user"]

    def is_accessible(self):
        token = request.cookies.get("jwt_token")
        if not token:
            return False
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user = User.get_user_by_public_id(data['public_id'])
        return user and user.role == 'admin'


class UserView(ModelView):
    form_columns = ["public_id", "name", "email", "role"]
    column_list = ["public_id", "name", "email", "role"]

    def is_accessible(self):
        token = request.cookies.get("jwt_token")
        if not token:
            return False
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user = User.get_user_by_public_id(data['public_id'])
        return user and user.role == 'admin'
    

admin.add_view(UserView(User, db.session))
admin.add_view(TaskView(Task, db.session))

