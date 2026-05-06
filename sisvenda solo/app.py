from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import random
import os

app = Flask(__name__)
app.secret_key = "sisvenda"

# ================= CAMINHO BANCO =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "database.db")


# ================= CONEXÃO =================
def conectar():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


# ================= CRIAR BANCO =================
def criar():

    con = conectar()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        senha TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pedidos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        comida TEXT,
        codigo INTEGER
    )
    """)

    con.commit()
    con.close()


criar()

# ================= CARDÁPIO =================
comidas = [
    ("Pizza",45),
    ("Lagosta ao Molho Branco",80),
    ("Rondelli Romeu e Julieta",35),
    ("Kebab",30),
    ("Shawarma",28),
    ("Lasanha",40),
    ("Hamburger",25),
    ("Macarrão ao Molho Branco",32)
]


# ================= HOME =================
@app.route("/")
def index():

    pedidos = []

    if "user" in session:
        con = conectar()
        cur = con.cursor()

        pedidos = cur.execute(
            "SELECT comida,codigo FROM pedidos WHERE usuario=?",
            (session["user"],)
        ).fetchall()

        con.close()

    return render_template(
        "index.html",
        usuario=session.get("user"),
        comidas=comidas,
        pedidos=pedidos
    )


# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():

    user = request.form.get("usuario")
    senha = request.form.get("senha")

    con = conectar()
    cur = con.cursor()

    usuario = cur.execute(
        "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
        (user, senha)
    ).fetchone()

    con.close()

    if usuario:
        session["user"] = user

    return redirect(url_for("index"))


# ================= CADASTRO =================
@app.route("/cadastro", methods=["POST"])
def cadastro():

    user = request.form.get("usuario")
    senha = request.form.get("senha")

    con = conectar()
    cur = con.cursor()

    try:
        cur.execute(
            "INSERT INTO usuarios(usuario,senha) VALUES(?,?)",
            (user, senha)
        )
        con.commit()
        session["user"] = user
    except sqlite3.IntegrityError:
        pass

    con.close()

    return redirect(url_for("index"))


# ================= PEDIR =================
@app.route("/pedir/<comida>")
def pedir(comida):

    if "user" not in session:
        return redirect(url_for("index"))

    codigo = random.randint(1000, 9999)

    con = conectar()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO pedidos(usuario,comida,codigo) VALUES(?,?,?)",
        (session["user"], comida, codigo)
    )

    con.commit()
    con.close()

    return redirect(url_for("index"))


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)