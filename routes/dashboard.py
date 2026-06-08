from flask import Blueprint, request, redirect, render_template, flash
from routes.auth import token_required
from models import Task

dash_bp = Blueprint("dash", __name__)

@dash_bp.route("/addtask", methods = ['GET', 'POST'])
@token_required
def addtask(current_user):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        new_task = Task(user_id = current_user.id, title = title, description = description)
        new_task.save()
        flash('Task added successfully', 'success')
        return redirect('/dashboard')
    return render_template('task.html')

@dash_bp.route("/deletetask/<int:task_id>", methods = ['POST'])
@token_required
def deletetask(current_user, task_id):
    task = Task.get_task_by_id(task_id)
    if(task and current_user.id == task.user_id):
        flash('Task deleted','warning')
        task.delete()
    else:
        flash('Please login', 'error')
        return redirect('/login')
    return redirect('/dashboard')


@dash_bp.route('/dashboard')
@token_required
def dashboard(current_user):
    tasks = current_user.get_tasks()
    isadmin = (current_user.role == "admin")
    return render_template("dashboard.html",isadmin=isadmin, tasks = tasks)

@dash_bp.route('/edittask/<int:task_id>', methods = ['GET','POST'])
@token_required
def edit_task(current_user, task_id):
    task = Task.get_task_by_id(id = task_id)
    if current_user.id == task.user_id:
        if request.method == 'POST':
            new_title = request.form['title']
            new_description = request.form['description']
            task.modify(new_title, new_description)
            return redirect('/dashboard')
        isadmin = (current_user.role == "admin")
        flash('Task edited successfully', 'success')
        return render_template('edittask.html',isadmin = isadmin, task=task)

