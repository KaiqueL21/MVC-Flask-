from models import db

# Cada classe que herda de db.Model se torna uma tabela no banco de dados.
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # 1:N → Um usuário pode ter muitas tarefas
    tasks = db.relationship("Task", back_populates="user")

    def __repr__(self):
        return f"<User {self.name}>"

