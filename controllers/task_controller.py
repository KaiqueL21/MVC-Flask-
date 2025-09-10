from flask import render_template, request, redirect, url_for
from models import db
from models.task import Task
from models.user import User

class TaskController:

    @staticmethod
    def list_tasks():
        # Pega todas as tarefas do banco
        tasks = Task.query.all()
        return render_template("tasks.html", tasks=tasks)

    @staticmethod
    def create_task():
        if request.method == "POST":
            # Pega dados do formulário
            title = request.form.get("title")
            description = request.form.get("description")
            user_id = request.form.get("user_id")

            # Verifica se os campos foram preenchidos
            if not title or not description or not user_id:
                users = User.query.all()
                return render_template("create_task.html",
                                       users=users,
                                       error="Preencha todos os campos!",
                                       title=title,
                                       description=description,
                                       user_id=user_id)

            # Checa se o usuário existe
            user = User.query.get(user_id)
            if not user:
                users = User.query.all()
                return render_template("create_task.html",
                                       users=users,
                                       error="Usuário não encontrado",
                                       title=title,
                                       description=description,
                                       user_id=user_id)

            # Cria e salva a tarefa
            task = Task(title=title, description=description, user_id=user_id, status="Pendente")
            db.session.add(task)
            db.session.commit()

            return redirect(url_for("list_tasks"))

        # GET → mostra o formulário
        users = User.query.all()
        return render_template("create_task.html", users=users)

    @staticmethod
    def update_task_status(task_id):
        task = Task.query.get(task_id)
        if task:
            # Alterna entre Pendente e Concluído
            if task.status == "Pendente":
                task.status = "Concluído"
            else:
                task.status = "Pendente"
            db.session.commit()
        return redirect(url_for("list_tasks"))

    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
        return redirect(url_for("list_tasks"))