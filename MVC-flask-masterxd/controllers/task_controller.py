from flask import render_template, request, redirect, url_for
from models import db
from models.task import Task
from models.user import User
from flasgger import swag_from

class TaskController:

    @staticmethod
    @swag_from({'tags': ['Tarefas'], 'description': 'Lista todas as tarefas'})
    def list_tasks():
        tasks = Task.query.all()
        return render_template('tasks.html', tasks=tasks)

    @staticmethod
    @swag_from({'tags': ['Tarefas'], 'description': 'Cria uma tarefa'})
    def add_task():
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            user_id = request.form['user_id']
            new_task = Task(title=title, description=description, user_id=user_id)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('list_tasks'))
        users = User.query.all()
        return render_template('create_task.html', users=users)

    @staticmethod
    @swag_from({'tags': ['Tarefas'], 'description': 'Atualiza status da tarefa'})
    def update_task_status(task_id):
        task = Task.query.get(task_id)
        if task.status != "Concluída":
            task.status = "Concluída"
        else:
            task.status = "Pendente"
        db.session.commit()
        return redirect(url_for('list_tasks'))

    @staticmethod
    @swag_from({'tags': ['Tarefas'], 'description': 'Deleta uma tarefa'})
    def delete_task(task_id):
        task = Task.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('list_tasks'))
