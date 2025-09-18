import os
from flask import Flask
from flasgger import Swagger
from config import Config
from controllers.user_controller import UserController
from controllers.task_controller import TaskController
from models import db

app = Flask(__name__, template_folder=os.path.join('view', 'templates'))
app.config.from_object(Config)

Swagger(app)

db.init_app(app)

with app.app_context():
    db.create_all()


app.add_url_rule('/', view_func=UserController.list_users, endpoint='list_users')
app.add_url_rule('/create_user', view_func=UserController.add_user, methods=['GET', 'POST'], endpoint='add_user')
app.add_url_rule('/delete_user/<int:user_id>', view_func=UserController.delete_user, methods=['POST'], endpoint='delete_user')

app.add_url_rule('/tasks', view_func=TaskController.list_tasks, endpoint='list_tasks')
app.add_url_rule('/tasks/new', view_func=TaskController.add_task, methods=['GET', 'POST'], endpoint='add_task')
app.add_url_rule('/tasks/delete/<int:task_id>', view_func=TaskController.delete_task, methods=['POST'], endpoint='delete_task')
app.add_url_rule('/tasks/update/<int:task_id>', view_func=TaskController.update_task_status, methods=['POST'], endpoint='update_task_status')

if __name__ == '__main__':
    print("Servidor rodando em http://127.0.0.1:5002")
    app.run(debug=True, port=5002)
