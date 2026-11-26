from app.db import DatabaseConnection
from werkzeug.security import generate_password_hash

class Usuario:

    def __init__(self, username, password, email=None, data_nascimento=None, foto=None, criado_em=None, id=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.data_nascimento = data_nascimento
        self.foto = foto
        self.criado_em = criado_em

    @classmethod
    def get_by_username(cls, username):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
            row = db.cursor.fetchone()
            if row:
                return cls(
                    username=row["username"],
                    password=row["password"],
                    email=row["email"],
                    data_nascimento=row["data_nascimento"],
                    foto=row["foto"],
                    criado_em=row["criado_em"],
                    id=row["id"]
                )
            return None

    @classmethod
    def get_by_email(cls, email):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            row = db.cursor.fetchone()
            if row:
                return cls(
                    username=row["username"],
                    password=row["password"],
                    email=row["email"],
                    data_nascimento=row["data_nascimento"],
                    foto=row["foto"],
                    criado_em=row["criado_em"],
                    id=row["id"]
                )
            return None

    @classmethod
    def get_by_id(cls, user_id):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
            row = db.cursor.fetchone()
            if row:
                return cls(
                    username=row["username"],
                    password=row["password"],
                    email=row["email"],
                    data_nascimento=row["data_nascimento"],
                    foto=row["foto"],
                    criado_em=row["criado_em"],
                    id=row["id"]
                )
            return None

    @classmethod
    def get_all(cls):
        with DatabaseConnection() as db:
            # Seleciona todas as colunas necessárias para a listagem ou painel
            db.cursor.execute("SELECT id, username, email, data_nascimento, foto, criado_em FROM usuarios")
            rows = db.cursor.fetchall()
            return [
                {
                    "id": row["id"], 
                    "username": row["username"],
                    "email": row["email"],
                    "data_nascimento": row["data_nascimento"],
                    "foto": row["foto"],
                    "criado_em": row["criado_em"]
                } for row in rows
            ]

    def save(self):
        senha_final = self.password if self.password.startswith(("pbkdf2:", "scrypt:")) else generate_password_hash(self.password)
        
        with DatabaseConnection() as db:
            db.cursor.execute(
                "INSERT INTO usuarios (username, password, email, data_nascimento, foto, criado_em) VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'))",
                (self.username, senha_final, self.email, self.data_nascimento, self.foto)
            )

    def atualizar_perfil(self):
        with DatabaseConnection() as db:
            db.cursor.execute(
                """
                UPDATE usuarios 
                SET email = ?, data_nascimento = ?, foto = ? 
                WHERE id = ?
                """,
                (self.email, self.data_nascimento, self.foto, self.id)
            )