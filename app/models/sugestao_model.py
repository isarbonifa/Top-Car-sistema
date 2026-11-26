from datetime import datetime
from app.db import DatabaseConnection

class Sugestao:
    def __init__(self, usuario_id, username, titulo, texto, criado_em=None, id=None):
        self.id = id
        self.usuario_id = usuario_id
        self.username = username
        self.titulo = titulo
        self.texto = texto
        self.criado_em = criado_em or datetime.now().strftime("%d/%m/%Y às %H:%M")

    def save(self):
        with DatabaseConnection() as db:
            db.cursor.execute(
                "INSERT INTO sugestoes (usuario_id, username, titulo, texto, criado_em) VALUES (?, ?, ?, ?, ?)",
                (self.usuario_id, self.username, self.titulo, self.texto, self.criado_em)
            )

    @staticmethod
    def get_all():
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM sugestoes ORDER BY id DESC")
            rows = db.cursor.fetchall()
            return [
                {
                    "id": row["id"],
                    "usuario_id": row["usuario_id"],
                    "username": row["username"],
                    "titulo": row["titulo"],
                    "texto": row["texto"],
                    "criado_em": row["criado_em"]
                } for row in rows
            ]

    @staticmethod
    def get_by_usuario(usuario_id):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM sugestoes WHERE usuario_id = ? ORDER BY id DESC", (usuario_id,))
            rows = db.cursor.fetchall()
            return [
                {
                    "id": row["id"],
                    "usuario_id": row["usuario_id"],
                    "username": row["username"],
                    "titulo": row["titulo"],
                    "texto": row["texto"],
                    "criado_em": row["criado_em"]
                } for row in rows
            ]

    @staticmethod
    def delete(sugestao_id, usuario_id, is_admin=False):
        with DatabaseConnection() as db:
            # Se for admin, pode apagar qualquer uma. Se não, só a própria sugestão.
            if is_admin:
                db.cursor.execute("DELETE FROM sugestoes WHERE id = ?", (sugestao_id,))
            else:
                db.cursor.execute("DELETE FROM sugestoes WHERE id = ? AND usuario_id = ?", (sugestao_id, usuario_id))