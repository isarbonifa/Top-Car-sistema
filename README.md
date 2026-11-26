# Top Car

Aplicação web **MPA** (Multi-Page Application) desenvolvida com **Flask**, **Jinja2** e **SQLite3**. O site hospeda o jogo de corrida *Top Car*, cujo motor foi programado em **C** com a biblioteca **raylib** e roda embutido no navegador. Os usuários podem se cadastrar, jogar, comentar sobre o jogo e enviar sugestões.

## Funcionalidades

- Cadastro, login e logout com senhas protegidas por hash (Werkzeug)
- Painel do usuário e listagem de usuários cadastrados
- Perfil editável (e-mail, data de nascimento e foto de perfil) e perfil público de outros usuários
- Preferência de tema (claro/escuro) salva em **cookie**
- Seção de comentários com criar, editar e excluir (apenas o autor)
- Central de sugestões: usuário comum vê e exclui as próprias; o `admin` vê e exclui todas
- Página 404 personalizada
- Jogo embutido via `iframe`, com botão de tela cheia

## Tecnologias

Python 3 · Flask · Jinja2 · SQLite3 · HTML/CSS · C + raylib (jogo)

## Estrutura do projeto

```
.
├── app/
│   ├── controllers/
│   │   ├── __init__.py              # register_blueprints()
│   │   ├── main_controller.py       # home, welcome, jogo
│   │   ├── auth_controller.py       # login, logout, register
│   │   ├── usuario_controller.py    # usuários, perfil, cookie de tema
│   │   ├── comentario_controller.py # comentários
│   │   └── sugestao_controller.py   # sugestões
│   ├── models/                      # Usuario, Comentario, Sugestao
│   ├── utils/                       # auth_middleware (login_required, guest_required)
│   ├── templates/
│   │   ├── base.html
│   │   ├── 404.html
│   │   ├── auth/                    # login, register
│   │   ├── main/                    # home, welcome, jogo
│   │   ├── usuarios/                # listar, perfil, perfil_publico
│   │   ├── comentarios/
│   │   └── sugestoes/
│   ├── static/                      # css, imagens, vídeo, uploads, jogo/
│   └── db.py                        # DatabaseConnection
├── iniciar_db.py                    # cria as tabelas e o usuário admin
├── requirements.txt
└── README.md
```

## Rotas

| Rota | Blueprint | Acesso | Descrição |
|---|---|---|---|
| `/` | main | visitante | Página inicial |
| `/welcome` | main | logado | Painel do usuário |
| `/jogo` | main | logado | Jogo |
| `/login`, `/register` | auth | visitante | Entrar / cadastrar |
| `/logout` | auth | logado | Sair |
| `/usuarios` | usuarios | logado | Lista de usuários |
| `/perfil` | usuarios | logado | Editar o próprio perfil |
| `/perfil/<id>` | usuarios | logado | Perfil público |
| `/mudar-preferencia-cookie` | usuarios | logado | Salva o tema em cookie |
| `/comentarios` | comentarios | logado | Listar, criar e editar |
| `/comentarios/excluir/<id>` | comentarios | logado | Excluir comentário |
| `/sugestoes` | sugestoes | logado | Listar e enviar sugestões |
| `/sugestoes/excluir/<id>` | sugestoes | logado | Excluir sugestão |

## Como executar

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/SEU-REPO.git
cd SEU-REPO

# 2. Crie e ative um ambiente virtual
python -m venv .venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Crie o banco de dados e o usuário administrador
python iniciar_db.py

# 5. Inicie a aplicação
python run.py                   # ajuste para o seu arquivo de entrada
```

Acesse `http://127.0.0.1:5000`.

### Usuário administrador

O `iniciar_db.py` cria o usuário `admin` (senha inicial `admin123`).

## Créditos

- **Áudios:** [Flowerhead](https://flowerheadmusic.itch.io/)
- **Cenário:** [AstroCom](https://astrocom.itch.io/)
- **Carros:** [Pay 'n' Sprite](https://patricio449.itch.io/)

Os recursos acima são livres para uso, mas os criadores aceitam doações.
