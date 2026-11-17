# Conecta — Mini Rede Social com Flask

Projeto desenvolvido com base na atividade de Programação Web 3.

## Funcionalidades
- Cadastro, login e logout de usuários.
- Senhas armazenadas com hash `scrypt`.
- Bloqueio das páginas internas para visitantes não autenticados.
- Upload de imagens PNG, JPG, JPEG e GIF com nome único UUID.
- Feed em ordem da publicação mais recente para a mais antiga.
- Chat coletivo em tempo real com Flask-SocketIO.
- Interface responsiva com Bootstrap.

## 1. Requisitos
- Python 3.10 ou superior
- VS Code (recomendado)

## 2. Abrir o projeto
Extraia o arquivo ZIP e abra a pasta `mini_rede_social` no VS Code.

## 3. Criar ambiente virtual (recomendado)
No terminal integrado do VS Code:

### Windows
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, use o Prompt de Comando:
```bat
venv\Scripts\activate.bat
```

### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

## 4. Instalar dependências
```bash
pip install -r requirements.txt
```

## 5. Executar
```bash
python app.py
```

Abra no navegador: http://127.0.0.1:5000

## 6. Testar
1. Clique em **Criar conta** e cadastre nome, e-mail e senha.
2. Faça login.
3. No feed, selecione uma imagem, escreva uma legenda e clique em **Publicar**.
4. Abra o chat em duas janelas ou navegadores diferentes para testar as mensagens em tempo real.
5. Clique em **Sair** para encerrar a sessão.

## Estrutura
```text
mini_rede_social/
├── app.py
├── requirements.txt
├── README.md
├── models/
│   ├── __init__.py
│   └── database.py
├── controllers/
│   ├── __init__.py
│   ├── routes.py
│   └── chat.py
├── static/
│   ├── css/style.css
│   └── uploads/
└── views/
    ├── base.html
    ├── cadastro.html
    ├── login.html
    ├── feed.html
    └── chat.html
```

## Observações
- O banco SQLite `models/rede_social.sqlite3` é criado automaticamente na primeira execução.
- As imagens ficam em `static/uploads/`.
- Para uso real na internet, troque a `SECRET_KEY`, desative `debug=True`, use HTTPS e acrescente proteções como CSRF e validação de conteúdo dos arquivos.
- O chat transmite mensagens enquanto os usuários estão conectados; o histórico não é salvo no banco, pois isso não é exigido na atividade.
