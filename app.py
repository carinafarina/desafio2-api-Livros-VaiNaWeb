from flask import Flask, request, jsonify 
# flask importa o microframework 
# request permite pegar os dados
# jsonify transformar os dados no formato json

import sqlite3

app = Flask(__name__) # dandername - Serve para setar ou referenciar o arquivo principal app.py

def init_db():
    with sqlite3.connect('database.db') as conn:

        conn.execute("""CREATE TABLE IF NOT EXISTS livros(
                     id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     titulo TEXT NOT NULL,
                     categoria TEXT NOT NULL, 
                     autor TEXT NOT NULL,
                     imagem_url TEXT NOT NULL
                     )""")
        print("Banco de Dados criando!")

init_db()        

# nome do @ é decorador
@app.route('/')   # para criar a estrutura da rota mais simples. rota é uma porta de acesso.
def home_page():
    return "<h2>Minha pagina com flask</h2>"


@app.route('/doar', methods=['POST'])
def doar():  
    dados = request.get_json() 

    titulo = dados.get('titulo')
    categoria = dados.get('categoria')
    autor = dados.get('autor')
    imagem_url = dados.get('imagem_url')

    if not titulo or not categoria or not autor or not imagem_url:
        return jsonify({"erro":"Todos os campos sâo obrigatorios"}),400
    
    with sqlite3.connect('database.db') as conn:
        conn.execute(f"""INSERT INTO livros (titulo,categoria,autor,imagem_url)VALUES('{titulo}','{categoria}','{autor}','{imagem_url}')""")
        conn.commit()

        return jsonify({"mensagem":" Livros cadastrados com sucesso"}),201


if __name__ == '__main__': #__name__ precisa ser o principai como __main__
    app.run(debug=True) # debug=True é para rodar o codigo automatico.