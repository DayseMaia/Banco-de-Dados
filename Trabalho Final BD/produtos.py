import psycopg2                             #   Importando biblioteca para conexão com o Banco de Dados;
from prettytable import PrettyTable         #   Importando biblioteca que imprime tabelas;
from os import system                       #   Importando biblioteca que permite limpar o terminal a cada função executada;

conn = psycopg2.connect(                    #   Criando conexão com o Banco de Dados;
    host = "localhost",
    database = "Farmacia",
    user = "postgres",
    password = "postgres"
)

cur = conn.cursor()                         #   Criando cursor;


def menu_produtos():                        #   Função Menu Produtos;
    system('cls')
    while True:
        
        print('''
        =====================================
                    MENU PRODUTOS            
        =====================================

        [1] - Lista de Produtos
        [2] - Cadastrar Novo Produto
        [3] - Atualizar Produto
        [4] - Remover Produto
        [0] - Voltar ao menu principal
        
        ''')
        
        opcao = input("Escolha a opção que deseja acessar: ")
        
        match opcao:
            case "1":
                mostrar_produtos()
            case "2":
                cadastrar_produto()
            case "3":
                atualizar_produto()
            case "4":
                remover_produto()
            case "0":
                system('cls')
                print('-'*60)
                print("Voltando ao menu principal...")
                print('-'*60)
                break
            case _:
                print('-'*60)
                print("Opção inválida. Escolha uma opção válida.")
                print('-'*60)

        input("Digite Enter para continuar...")
        system('cls')

def mostrar_produtos():                     #   Função que lista os Produtos cadastrados;
    system('cls')
    cur.execute('''
    SELECT * FROM "Produtos"
    ORDER BY "ID_Produto"
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    tabela = PrettyTable(colunas)
    for linha in linhas:
        tabela.add_row(linha)

    print(''' 
                    - Lista de Produtos - 
    ''')
    print(tabela)


def cadastrar_produto():                    #   Função para cadastrar novo produto;
    system('cls')
    print(''' 
    - Cadastro de Produtos: 
    ''')

    nome = input("Digite o nome do Produto: ")
    valor = input("Digite o valor do Produto: ")
    estoque = input("Digite o estoque do Produto: ")

    cur.execute(f'''
    INSERT INTO "Produtos"
    VALUES(DEFAULT, '{nome}', '{valor}', '{estoque}')
    ''')
    conn.commit()

    print('-'*60)
    print(f"O produto {nome} foi cadastrado com sucesso.")
    print('-'*60)


def atualizar_produto():                    #   Função para atualizar produto cadastrado;
    system('cls')
    print(''' 
    - Atualizar Produto: 
    ''')
    
    mostrar_produtos()
    print()
    produto_escolhido = input("Digite o ID do produto: ")
    novo_nome = input("Digite o novo nome do produto (digite Enter para não alterar): ")
    novo_valor = input("Digite o novo valor do produto (digite Enter para não alterar): ")
    novo_estoque = input("Digite o novo estoque do produto (digite Enter para não alterar): ")

    if novo_nome:
        cur.execute(f'''
        UPDATE "Produtos"
        SET "Nome_Produto" = '{novo_nome}'
        WHERE "ID_Produto" = {produto_escolhido}
        ''')
        conn.commit()

    if novo_valor:
        cur.execute(f'''
        UPDATE "Produtos"
        SET "Valor_Produto" = '{novo_valor}'
        WHERE "ID_Produto" = {produto_escolhido}
        ''')
        conn.commit()

    if novo_estoque:
        cur.execute(f'''
        UPDATE "Produtos"
        SET "Estoque_Produto" = '{novo_estoque}'
        WHERE "ID_Produto" = {produto_escolhido}
        ''')
        conn.commit()
    
    print('-'*60)
    print("Alteração realizada com sucesso!")
    print('-'*60)


def remover_produto():                      #   Função para remover Produto cadastrado;
    system('cls')
    print(''' 
    - Remover Produto: 
    ''')
    
    mostrar_produtos()
    print()
    produto_escolhido = input("Digite o ID do produto: ")

    confirmar = input("Deseja mesmo remover este produto? (S/N) ").upper()

    match confirmar:
        case "S":
            cur.execute(f'''
            DELETE FROM "Produtos"
            WHERE "ID_Produto" = '{produto_escolhido}'
            ''')
            conn.commit()
           
            print('-'*60)
            print("Produto removido com sucesso.")
            print('-'*60)

        case "N":
            print('-'*60)
            print("Voltando ao menu.")
            print('-'*60)

        case _:
            print('-'*60)
            print("Opção inválida. Voltando ao menu.")
            print('-'*60)