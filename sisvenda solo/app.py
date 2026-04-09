import sqlite3

# ---------- CONECTAR DATABASE ----------
con = sqlite3.connect("ifome.db")
cursor = con.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comida TEXT NOT NULL,
    cliente TEXT NOT NULL
)
""")
con.commit()

# ---------- COMIDAS ----------
comidas = [
    "Pizza",
    "Lagosta ao Molho Branco",
    "Rondele de Romeu e Julieta",
    "Kebapi",
    "Shawarma",
    "Lasanha",
    "Hamburger",
    "Macarrão ao Molho Branco"
]

# ---------- MENU ----------
def menu():
    print("\n===== I FOME =====")
    print("1 - Ver comidas")
    print("2 - Fazer pedido")
    print("3 - Ver pedidos")
    print("4 - Sair")


# ---------- LISTAR COMIDAS ----------
def listar_comidas():
    print("\n--- CARDÁPIO ---")
    for i in range(len(comidas)):
        print(i + 1, "-", comidas[i])


# ---------- FAZER PEDIDO ----------
def fazer_pedido():
    listar_comidas()

    escolha = input("Número da comida: ")

    if not escolha.isdigit():
        print("❌ Digite apenas número")
        return

    escolha = int(escolha)

    if escolha < 1 or escolha > len(comidas):
        print("❌ Comida inválida")
        return

    comida = comidas[escolha - 1]

    cliente = input("Nome do cliente: ").strip()

    if cliente == "":
        print("❌ Nome vazio")
        return

    try:
        cursor.execute(
            "INSERT INTO pedidos (comida, cliente) VALUES (?, ?)",
            (comida, cliente)
        )
        con.commit()
        print("✅ Pedido cadastrado com sucesso!")

    except Exception as e:
        print("ERRO:", e)


# ---------- VER PEDIDOS ----------
def ver_pedidos():
    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()

    print("\n--- PEDIDOS ---")

    if not pedidos:
        print("Nenhum pedido ainda.")
        return

    for p in pedidos:
        print(f"ID {p[0]} | {p[2]} pediu {p[1]}")


# ---------- LOOP ----------
while True:
    menu()
    op = input("Escolha: ")

    if op == "1":
        listar_comidas()

    elif op == "2":
        fazer_pedido()

    elif op == "3":
        ver_pedidos()

    elif op == "4":
        print("Saindo...")
        break

    else:
        print("Opção inválida")

con.close()