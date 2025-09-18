from flask import render_template, request, redirect, url_for
from models.user import User
from models import db
from flasgger import swag_from

class UserController:

    @staticmethod
    @swag_from({'tags': ['Usuários']})
    def list_users():
        users = User.query.all()
        return render_template('index.html', users=users)

    @staticmethod
    @swag_from({'tags': ['Usuários']})
    def add_user():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return render_template('create_user.html', error="Usuário já existe", name=name, email=email)
            new_user = User(name=name, email=email)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('list_users'))
        return render_template('create_user.html')

    @staticmethod
    @swag_from({'tags': ['Usuários']})
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return redirect(url_for('list_users'))
