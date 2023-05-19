import psycopg2                             #   Importando biblioteca para conexão com o Banco de Dados;
from prettytable import PrettyTable         #   Importando biblioteca que imprime tabelas;
import clientes                             #   Importando arquivo clientes;
import produtos                             #   Importando arquivo produtos;
from os import system                       #   Importando biblioteca que permite limpar o terminal a cada função executada;

conn = psycopg2.connect(                    #   Criando conexão com o Banco de Dados;
    host = "localhost",
    database = "Farmacia",
    user = "postgres",
    password = "postgres"
)

cur = conn.cursor()                         #   Criando cursor;


def menu_compras():                        #   Função Menu Compras;
    system('cls')
    while True:
        
        print('''
        ====================================
                    MENU COMPRAS            
        ====================================

        [1] - Lista de Compras
        [2] - Cadastrar Nova Compra
        [3] - Atualizar Compra
        [4] - Remover Compra
        [0] - Voltar ao menu principal
        
        ''')
        
        opcao = input("Escolha a opção que deseja acessar: ")
        
        match opcao:
            case "1":
                mostrar_compras()
            case "2":
                cadastrar_compra(cur)
            case "3":
                atualizar_compra()
            case "4":
                remover_compra()
            case "0":
                system('cls')
                print('-'*60)
                print("Voltando ao menu principal...")
                print('-'*60)
                break
            case _:
                print('-'*60)
                print("Opção inválida! Escolha uma opção válida.")
                print('-'*60)

        input("Digite Enter para continuar...")
        system('cls')


def mostrar_compras():
    system('cls')
    cur.execute('''
    SELECT * FROM "Compras"
    ORDER BY "ID_Compra"
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    tabela = PrettyTable(colunas)
    for linha in linhas:
        id_cliente = linha[1]
        id_produto = linha[2]

        # Consultar o nome do cliente com base no ID do cliente
        cur.execute(f'''
        SELECT "Nome_Cliente" FROM "Clientes"
        WHERE "ID_Cliente" = {id_cliente}
        ''')
        nome_cliente = cur.fetchone()[0]

        # Consultar o nome do produto com base no ID do produto
        cur.execute(f'''
        SELECT "Nome_Produto" FROM "Produtos"
        WHERE "ID_Produto" = {id_produto}
        ''')
        nome_produto = cur.fetchone()[0]

        # Substituir o ID pelo nome do cliente e do produto
        linha = list(linha)
        linha[1] = nome_cliente
        linha[2] = nome_produto

        tabela.add_row(linha)

    print('''
                            - Lista de Compras - 
    ''')
    print(tabela)


def cadastrar_compra(cur):                  #   Função para cadastrar nova compra;
    system('cls')
    print(''' 
    - Cadastro de Compra: 
    ''')

    clientes.mostrar_clientes()
    print()
    cliente = input("Digite o ID do cliente: ")

    produtos.mostrar_produtos()
    print()
    produto = input("Digite o ID do produto: ")

    quantidade = int(input("Digite a quantidade a ser comprada: "))

    cur.execute(f'''
    SELECT "Valor_Produto", "Estoque_Produto" FROM "Produtos"
    WHERE "ID_Produto" = {produto}
    ''')
    
    result = cur.fetchone()
    valor_produto, estoque_produto = result[0], result[1]

    if quantidade > estoque_produto:
        print("Produto sem estoque.")
    else:
        estoque_produto -= quantidade
        cur.execute(f'''
        UPDATE "Produtos"
        SET "Estoque_Produto" = {estoque_produto}
        WHERE "ID_Produto" = {produto}
        ''')
        conn.commit()
    
    valor_total = valor_produto * quantidade

    cur.execute(f'''
    INSERT INTO "Compras"
    VALUES(DEFAULT, '{cliente}', '{produto}', '{quantidade}', '{valor_total}', DEFAULT)
    ''')
    conn.commit()
    
    print('-'*60)
    print(f"Compra realizada com sucesso. Valor total da compra: R${valor_total}")
    print('-'*60)


def atualizar_compra():                     #   Função para atualizar compra cadastrada;
    system('cls')
    print(''' 
    - Atualizar Compra: 
    ''')
    
    mostrar_compras()
    print()

    compra_escolhida = input("Digite o ID da compra: ")
    clientes.mostrar_clientes()
    novo_id_cliente = input("Digite o novo ID do cliente na compra (digite Enter para não alterar): ")
    produtos.mostrar_produtos()
    novo_id_produto = input("Digite o novo ID do produto na compra (digite Enter para não alterar): ")
    nova_quantidade = input("Digite o nova quantidade do produto na compra (digite Enter para não alterar): ")
    novo_valor_total = input("Digite o novo valor total do produto na compra (digite Enter para não alterar): ")

    if novo_id_cliente:
        cur.execute(f'''
        UPDATE "Compras"
        SET "ID_Cliente" = {novo_id_cliente}
        WHERE "ID_Compra" = {compra_escolhida}
        ''')
        conn.commit()

    if novo_id_produto:
        cur.execute(f'''
        UPDATE "Compras"
        SET "ID_Produto" = {novo_id_produto}
        WHERE "ID_Compra" = {compra_escolhida}
        ''')
        conn.commit()

    if nova_quantidade:
        cur.execute(f'''
        UPDATE "Compras"
        SET "Quantidade" = {nova_quantidade}
        WHERE "ID_Compra" = {compra_escolhida}
        ''')
        conn.commit()

    if novo_valor_total:
        cur.execute(f'''
        UPDATE "Compras"
        SET "Valor_Total" = {novo_valor_total}
        WHERE "ID_Compra" = {compra_escolhida}
        ''')
        conn.commit()

    print('-'*60)
    print("Alteração realizada com sucesso!")
    print('-'*60)


def remover_compra():                       #   Função para remover compra cadastrada;
    system('cls')
    print(''' 
    - Remover Compra: 
    ''')
    
    mostrar_compras()
    print()

    compra_escolhida = input("Digite o ID da compra: ")

    confirmar = input("Deseja mesmo remover essa compra? (S/N) ").upper()

    match confirmar:
        case "S":
            cur.execute(f'''
            DELETE FROM "Compras"
            WHERE "ID_Compra" = '{compra_escolhida}'
            ''')
            conn.commit()
           
            print('-'*60)
            print("Compra removida com sucesso.")
            print('-'*60)

        case "N":
            print('-'*60)
            print("Voltando ao menu.")
            print('-'*60)

        case _:
            print('-'*60)
            print("Opção inválida. Voltando ao menu.")
            print('-'*60)
