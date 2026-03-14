from flask import Flask, request, render_template
import sqlite3
import hashlib

app = Flask(__name__)

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]


        senha_hash = hashlib.sha256(senha.encode()).hexdigest()


        conexao = sqlite3.connect("banco.db")
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha)
            VALUES (?, ?, ?)
        """, (nome, email, senha_hash))
        conexao.commit()
        conexao.close()

        

        return "Cadastrado com sucesso!"

    
    return render_template("cadastro.html")
    

@app.route("/usuarios")
def listar():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conexao.close()
    return render_template("index.html", usuarios=usuarios)



@app.route("/deletar/<id>")
def deletar_cadastro(id):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()


    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()
    
    return "Deletado com sucesso!"
    

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL
        )
    """)
conexao.commit()
conexao.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        conexao = sqlite3.connect("banco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha_hash))
        usuario = cursor.fetchone()
        conexao.close()

        if usuario:
            return f"Bem vindo, {usuario[1]}!"
        else:
            return "Email ou senha incorretos!"
    
    return render_template("login.html")


if __name__== "__main__":
    app.run(debug=True)



