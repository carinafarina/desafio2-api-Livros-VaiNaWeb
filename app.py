from flask import Flask, request, jsonify, render_template
# flask importa o microframework 
# request permite pegar os dados
# jsonify transformar os dados no formato json
from flask_cors import CORS

import sqlite3

app = Flask(__name__) # dandername - Serve para setar ou referenciar o arquivo principal app.py
CORS(app)
def init_db():
   # With ele abre e fecha a conexao com o banco de dados. O .connect, ele cria e abre uma conexao com o mando de dados(FAZ O PAPEL DO CREATE E USE)
    with sqlite3.connect('database.db') as conn: # conn é uma variavel que guarda o with sqlite3.connect('database.db')

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
    return render_template ('index.html')


@app.route('/doar', methods=['POST'])
def doar():  
    dados = request.get_json() 

    titulo = dados.get('titulo')
    categoria = dados.get('categoria')
    autor = dados.get('autor')
    imagem_url = dados.get('imagem_url')

    if not all ([titulo, categoria, autor, imagem_url]):
        return jsonify({"erro":"Todos os campos sâo obrigatorios"}),400
    
    with sqlite3.connect('database.db') as conn:
        conn.execute("""INSERT INTO livros (titulo,categoria,autor,imagem_url)VALUES(?,?,?,?)""",(titulo, categoria, autor, imagem_url))
        conn.commit() # serve para salvar

        return jsonify({"mensagem":" Livros cadastrados com sucesso"}),201

@app.route('/livros', methods=['GET'])
def listar_livro():
    with sqlite3.connect('database.db') as conn:
        livros = conn.execute("SELECT * FROM livros").fetchall() # fetchall, pega tudo que foi insirido no banco de dados.

    livros_formatados = []  # organizar os livros

    for livro in livros:
        dicionario_livro = {
            "id": livro[0],
            "titulo": livro[1],
            "categoria": livro[2],
            "autor": livro[3],
            "imagem_url": livro[4]
        }   
        livros_formatados.append(dicionario_livro) # o append é para add 
    return jsonify(livros_formatados)   

@app.route('/livros/<int:livro_id>', methods=['DELETE'])
def deletar_livro(Livro_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()  # serve para veificar os dados do banco 
        cursor.execute("DELETE FROM livros WHERE id = ?",(Livro_id,))
        conn.commit() # para salvar no banco de dados

        if cursor.rowcount == 0:
            return jsonify({"erro":"Livro nâo encontrado"}), 404
        
        return jsonify({"menssagem":"Livro deletado"}), 200
        

if __name__ == '__main__': #__name__ precisa ser o principai como __main__
    app.run(debug=True) # debug=True é para rodar o codigo automatico.