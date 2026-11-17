from flask import Flask, render_template 
#render_template RENDERIZA AS PÁGINAS HTML


app = Flask(__name__, template_folder='Views')

@app.route('/')
def home():
    return render_template ("index.html")

@app.route('/games')
def games():
    
    # Criando variáveis
    titulo = "Silk Song"
    ano = 2025
    categoria = "Metroid Van"
    
    jogadores = ['Eduardo', 'Ana', 'Guilherme','Victor','William']
    
    # Enviando as variáveis para o HTML
    return render_template(
        "games.html",
        titulo=titulo,
        ano=ano,
        categoria=categoria,
        jogadores=jogadores
    )

@app.route('/consoles')
def consoles():
  # Criando variáveis
    titulo = "Silk Song"
    ano = 2025
    categoria = "Metroid Van"
    
    jogadores = ['Eduardo', 'Ana', 'Guilherme','Victor','William']
    
    
 # Enviando as variáveis para o HTML
    return render_template(
        "console.html",
        titulo=titulo,
        ano=ano,
        categoria=categoria,
        jogadores=jogadores
    )


# INICIANDO O SERVIDOR WEB
if __name__ == '__main__':
    app.run(debug=True)