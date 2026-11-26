from datetime import datetime
from app.db import DatabaseConnection


class Comentario:

  def __init__(self, username, texto, usuario_id, criado_em=None, editado_em=None, id=None):
    self.id = id
    self.username = username
    self.texto = texto
    self.usuario_id = usuario_id
    self.criado_em = criado_em or datetime.now().strftime("%d/%m/%Y às %H:%M")
    self.editado_em = editado_em

  @staticmethod
  def get_all():
    with DatabaseConnection() as db:
      db.cursor.execute(
          "SELECT id, username, texto, usuario_id, criado_em, editado_em FROM comentarios"
          " ORDER BY id DESC"
      )
      rows = db.cursor.fetchall()

      return [
          {
              "id": row["id"],
              "username": row["username"],
              "texto": row["texto"],
              "usuario_id": row["usuario_id"],
              "criado_em": row["criado_em"],
              "editado_em": row["editado_em"],
          }
          for row in rows
      ]

  @staticmethod
  def get_by_id(comment_id):
    with DatabaseConnection() as db:
      db.cursor.execute(
          "SELECT id, username, texto, usuario_id, criado_em, editado_em FROM comentarios"
          " WHERE id = ?",
          (comment_id,),
      )
      row = db.cursor.fetchone()

      if row:
        return Comentario(
            username=row["username"],
            texto=row["texto"],
            usuario_id=row["usuario_id"],
            criado_em=row["criado_em"],
            editado_em=row["editado_em"],
            id=row["id"],
        )
      return None

  def save(self):
    with DatabaseConnection() as db:
      db.cursor.execute(
          "INSERT INTO comentarios (username, texto, usuario_id, criado_em, editado_em)"
          " VALUES (?, ?, ?, ?, ?)",
          (self.username, self.texto, self.usuario_id, self.criado_em, self.editado_em),
      )

  @staticmethod
  def update(comment_id, usuario_id, novo_texto):
    """Só o dono do comentário consegue editar. Retorna True se atualizou."""
    with DatabaseConnection() as db:
      agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
      db.cursor.execute(
          "UPDATE comentarios SET texto = ?, editado_em = ? WHERE id = ? AND usuario_id = ?",
          (novo_texto, agora, comment_id, usuario_id),
      )
      return db.cursor.rowcount > 0

  @staticmethod
  def delete(comment_id, usuario_id, is_admin=False):
    """Admin exclui qualquer comentário; usuário comum só os próprios.
    Retorna True se algum registro foi removido."""
    with DatabaseConnection() as db:
      if is_admin:
        db.cursor.execute("DELETE FROM comentarios WHERE id = ?", (comment_id,))
      else:
        db.cursor.execute(
            "DELETE FROM comentarios WHERE id = ? AND usuario_id = ?",
            (comment_id, usuario_id),
        )
      return db.cursor.rowcount > 0