import sqlite3
import random

# ======================
# CONEXÃO
# ======================
def conectar():
    return sqlite3.connect("database.db")


# ======================
# LER PREÇO
# ======================
def ler_preco(txt):
    valor = input(txt)
    valor = valor.replace(",", ".")
    return float(valor)


# ======================
# CRIAR TABELAS
# ======================
def criar_tabelas():

    con = conectar()
    cursor = con.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        senha TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comidas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        preco REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drinks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        preco REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        comida TEXT,
        drink TEXT,
        preco_total REAL,
        tipo TEXT,
        rua TEXT,
        numero TEXT,
        bairro TEXT,
        complemento TEXT,
        codigo_retirada TEXT,
        status TEXT
    )
    """)

    con.commit()
    con.close()


# ======================
# COMIDAS PADRÃO
# ======================
def comidas_padrao():

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT COUNT(*) FROM comidas")

    if cursor.fetchone()[0] == 0:

        comidas = [
            ("Pizza",49.90),
            ("Lagosta ao Molho Branco",89.90),
            ("Rondelle Romeu e Julieta",39.90),
            ("Kebab",34.90),
            ("Shawarma",32.90),
            ("Lasanha",44.90),
            ("Hamburger",29.90),
            ("Macarrão ao Molho Branco",41.90)
        ]

        cursor.executemany(
            "INSERT INTO comidas(nome,preco) VALUES(?,?)",
            comidas
        )

    cursor.execute("SELECT COUNT(*) FROM drinks")

    if cursor.fetchone()[0] == 0:

        drinks = [
            ("Coca-Cola",6.00),
            ("Guaraná",6.00),
            ("Fanta Laranja",6.00),
            ("Suco Natural",8.00),
            ("Água",4.00),
            ("Água com Gás",5.00),
            ("Milkshake Chocolate",12.00),
            ("Milkshake Morango",12.00),
            ("Milkshake Baunilha",12.00),
            ("Red Bull",15.00)
        ]

        cursor.executemany(
            "INSERT INTO drinks(nome,preco) VALUES(?,?)",
            drinks
        )

    con.commit()
    con.close()


# ======================
# CADASTRO
# ======================
def cadastrar():

    nome = input("Novo usuário: ").strip()
    senha = input("Senha: ").strip()

    if nome.lower() == "admin":
        print("❌ Nome reservado")
        return

    con = conectar()
    cursor = con.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios(nome,senha) VALUES(?,?)",
            (nome, senha)
        )
        con.commit()
        print("✅ Cadastro realizado!")
    except:
        print("❌ Usuário já existe")

    con.close()


# ======================
# LOGIN
# ======================
def login():

    user = input("Usuário: ").strip().lower()
    senha = input("Senha: ").strip()

    if user == "admin" and senha == "123":
        print("✅ ADMIN LOGADO")
        painel_admin()
        return

    con = conectar()
    cursor = con.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE LOWER(nome)=? AND senha=?",
        (user, senha)
    )

    usuario = cursor.fetchone()
    con.close()

    if usuario:
        painel_cliente(usuario[1])
    else:
        print("❌ Login inválido")


# ======================
# CARDÁPIO
# ======================
def cardapio():

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM comidas")
    comidas = cursor.fetchall()

    print("\n===== COMIDAS =====")
    for c in comidas:
        print(f"{c[0]} - {c[1]} | R${c[2]}")

    con.close()
    return comidas


def menu_drinks():

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM drinks")
    drinks = cursor.fetchall()

    print("\n===== DRINKS =====")
    print("0 - Sem drink")

    for d in drinks:
        print(f"{d[0]} - {d[1]} | R${d[2]}")

    con.close()
    return drinks


# ======================
# FAZER PEDIDO (PRO)
# ======================
def fazer_pedido(cliente):

    total = 0
    pedidos_comida = []
    pedidos_drink = []

    while True:

        comidas = cardapio()
        escolha = input("Escolha comida: ")

        comida=None
        preco_comida=0

        for c in comidas:
            if str(c[0]) == escolha:
                comida=c[1]
                preco_comida=c[2]

        if not comida:
            print("❌ inválido")
            continue

        drinks = menu_drinks()
        escolha_d=input("Escolha drink: ")

        drink="Sem drink"
        preco_drink=0

        for d in drinks:
            if str(d[0]) == escolha_d:
                drink=d[1]
                preco_drink=d[2]

        pedidos_comida.append(comida)
        pedidos_drink.append(drink)

        total += preco_comida + preco_drink

        print(f"\n🧾 Total parcial: R${total:.2f}")

        print("""
Deseja pedir mais?
1 Sim
2 Finalizar pedido
""")

        if input("Escolha: ") != "1":
            break

    comida_final=", ".join(pedidos_comida)
    drink_final=", ".join(pedidos_drink)

    print("\n1 Entrega")
    print("2 Retirada")

    tipo_op=input("Escolha: ")

    rua=numero=bairro=complemento=""
    codigo=""

    if tipo_op=="1":
        tipo="Entrega"
        rua=input("Rua: ")
        numero=input("Número: ")
        bairro=input("Bairro: ")
        complemento=input("Complemento: ")
    else:
        tipo="Retirada"
        codigo=str(random.randint(1000,9999))
        print("Código retirada:",codigo)

    con=conectar()
    cursor=con.cursor()

    cursor.execute("""
    INSERT INTO pedidos
    (cliente,comida,drink,preco_total,tipo,
     rua,numero,bairro,complemento,codigo_retirada,status)
    VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """,(cliente,comida_final,drink_final,total,tipo,
         rua,numero,bairro,complemento,
         codigo,"Preparando"))

    con.commit()
    con.close()

    print(f"\n✅ Pedido feito! Total R${total:.2f}")

    # ======================
    # PAGAMENTO
    # ======================
    print("\n💰 PAGAR AGORA?")
    print("1 Sim")
    print("2 Depois")

    if input("Escolha: ")=="1":

        print("""
1 Cartão
2 Dinheiro
3 PIX
""")

        forma=input("Forma: ")

        if forma=="1":

            print("""
💳 Tipo do cartão
1 Débito
2 Crédito
""")

            cartao=input("Escolha: ")

            if cartao=="1":
                print("💳 Pago no DÉBITO!")
            elif cartao=="2":
                print("💳 Pago no CRÉDITO!")

        elif forma=="2":
            valor=float(input("Valor entregue: R$"))
            print(f"💰 Troco R${valor-total:.2f}")

        elif forma=="3":
            print("""
PIX: restaurante@sisvenda.com
""")
            input("Pressione ENTER após pagar")
            print("✅ PIX confirmado")

        print("✅ Pedido pago!")

    else:
        print("Pagamento na entrega.")


# ======================
# CLIENTE
# ======================
def painel_cliente(nome):

    while True:

        print("""
1 Fazer pedido
0 Sair
""")

        if input("Escolha: ")=="1":
            fazer_pedido(nome)
        else:
            break


# ======================
# ADMIN
# ======================
def painel_admin():

    con=conectar()
    cursor=con.cursor()

    while True:

        print("""
===== ADMIN =====
1 Ver pedidos
2 Marcar entregue
3 Adicionar comida
4 Adicionar drink
0 Sair
""")

        op=input("Escolha: ")

        if op=="1":
            cursor.execute("SELECT * FROM pedidos")
            for p in cursor.fetchall():
                print(p)

        elif op=="2":
            idp=input("ID pedido: ")
            cursor.execute(
                "UPDATE pedidos SET status='Entregue' WHERE id=?",
                (idp,))
            con.commit()

        elif op=="3":
            nome=input("Nome comida: ")
            preco=ler_preco("Preço: ")
            cursor.execute(
                "INSERT INTO comidas(nome,preco) VALUES(?,?)",
                (nome,preco))
            con.commit()

        elif op=="4":
            nome=input("Nome drink: ")
            preco=ler_preco("Preço: ")
            cursor.execute(
                "INSERT INTO drinks(nome,preco) VALUES(?,?)",
                (nome,preco))
            con.commit()

        elif op=="0":
            con.close()
            break


# ======================
# MENU
# ======================
def menu():

    criar_tabelas()
    comidas_padrao()

    while True:

        print("""
===== SISVENDA =====
1 Cadastrar
2 Login
0 Sair
""")

        op=input("Escolha: ")

        if op=="1":
            cadastrar()
        elif op=="2":
            login()
        else:
            break


menu()
