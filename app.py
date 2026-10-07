from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key ="chave-secreta"

def conectar_banco():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    return conexao, cursor

def criar_tabela():
    conexao, cursor = conectar_banco()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

    criar_tabela()

@app.route("/cadastro", methods = ["GET", "POST"])
def cadastro():

    if request.methods == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        banco = conectar_banco()

        banco.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES(?, ?, ?)", 
            (nome, email, senha)
        )

        banco.commit()
        banco.close()

        return "Cadastro realizado"
        return render_template("cadastro.html")


@app.route("/Login", methods = ["GET", "POST"])
def Login():

    if request.methods == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        banco = conectar_banco()

        banco.execute(
            "SELECT * FROM usuarios WHERE email = ? AND senha = ?", 
            (email, senha)
        ).fetchone

        banco.close()

        if usuario: 
            session["usuario_id"] = usuario[0]
            return redirect("/area")

        return "email ou senha incorreta"
        return render_template("login.html")

@app.route("/area")
def area():
    if "usuario_id" not in session:
        return redirect("/login")

    return "Voce esta logado0"

@app.route("/logout")
def logout():

    session.pop("usuario_id", none)

    return redirect("/login")

@app.route("/usuarios")
def usuarios():
    banco = conectar_banco()

    dados = banco_execute(" SELECT * FROM usuarios"). fetchall()

    banco.close()

    return render_template("usuarios.html", usuarios = dados)

@app.route("/excluir/int:id")
def excluir(id):

    banco = conectar_banco

    banco_execute(
        "DELETE FROM usuarios WHERE id = ?", (id,)
    )

    banco.commit()
    banco.close()

    return redirect("/usuarios")

@app.route("/editar/<int:id> methods = ["GET", "POST"})
def editar():

    banco= conectar_banco()

    usuario = banco.execute(
        "SELECT * FROM usuarios WHERE id = ?", (id,)
    ).fetchone()

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        banco = conectar_banco()

        banco.execute(
            """UPDATE usuarios SET nome = ?, email = ?, senha = ? WHERE id = ?""", 
            (nome, email, senha, id)
        )

        banco.commit()
        banco.close()

        return redirect("/usuarios")
        return render_template("editar.html", usuario = usuario)

if __name__ == "__main__":
    app.run(debug = True)
