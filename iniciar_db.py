from app.db import DatabaseConnection
from werkzeug.security import generate_password_hash
import sqlite3
from app.models.user_model import Usuario

# O 'with' abre a conexão e já te entrega o cursor automaticamente
with DatabaseConnection() as db:
    # Tabela de usuários
    db.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            data_nascimento TEXT,
            foto TEXT,
            criado_em TEXT
        )
    """)

    # Tabela de comentários
    db.cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            texto TEXT NOT NULL,
            criado_em TEXT NOT NULL,
            editado_em TEXT,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
        )
    """)

    db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sugestoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                titulo TEXT NOT NULL,
                texto TEXT NOT NULL,
                criado_em TEXT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
            )
        """)

    print("Tabelas criadas com sucesso!")

    # 2. Cadastro do admin utilizando o método do Model (conforme regra do professor)
    if not Usuario.get_by_username("admin"):
        senha_hash = generate_password_hash("admin123")
        
        # Instancia o objeto da classe Usuario com os dados do admin
        admin = Usuario(
            username="admin",
            password=senha_hash,
            email="admin@topcar.com",
            data_nascimento=None,
            foto=None
        )
        
        # Chama o método de salvamento da classe (verifique se no seu model o nome é .save() ou .salvar())
        admin.save() 
        print("Usuário administrador inicial criado com sucesso via método do Model!")
    else:
        print("Usuário admin já existe no banco.")