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


def menu_clientes():                        #   Função Menu Clientes;
    system('cls')
    while True:
        
        print('''
        =====================================
                    MENU CLIENTES            
        =====================================

        [1] - Lista de Clientes
        [2] - Cadastrar Novo Cliente
        [3] - Atualizar Cliente
        [4] - Remover Cliente
        [5] - Lista de Clientes Inativos
        [0] - Voltar ao menu principal
        
        ''')
        
        opcao = input("Escolha a opção que deseja acessar: ")
        
        match opcao:
            case "1":
                mostrar_clientes()
            case "2":
                cadastrar_cliente()
            case "3":
                atualizar_cliente()
            case "4":
                remover_cliente()
            case "5":
                mostrar_clientes_inativos()
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

def mostrar_clientes():                     #   Função que lista os clientes cadastrados;
    system('cls')
    cur.execute('''
    SELECT * FROM "Clientes"
    WHERE "Status" = 'Ativo'
    ORDER BY "ID_Cliente"
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    tabela = PrettyTable(colunas)
    for linha in linhas:
        tabela.add_row(linha)

    print(''' 
                                    - Lista de Clientes - 
    ''')
    print(tabela)


def mostrar_clientes_inativos():            #   Função que lista os clientes removidos;
    system('cls')
    cur.execute('''
    SELECT * FROM "Clientes"
    WHERE "Status" = 'Inativo'
    ORDER BY "ID_Cliente"
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    tabela = PrettyTable(colunas)
    for linha in linhas:
        tabela.add_row(linha)

    print(''' 
                            - Lista de Clientes Inativos - 
    ''')
    print(tabela)

    #   Opção para recadastrar Clientes que foram removidos;
    
    recadastrar = input("Deseja recadastrar cliente? (S/N) ").upper()

    match recadastrar:
        case "S":
           id_cliente = input("Digite o ID do Cliente que deseja recadastrar: ")
           recadastrar_cliente(id_cliente)

        case "N":
            print('-'*60)
            print("Voltando ao menu principal.")
            print('-'*60)

        case _:
            print('-'*60)
            print("Opção inválida. Voltando ao menu.")
            print('-'*60)


def recadastrar_cliente(id_cliente):        #   Função para recadastrar clientes removidos;
        cur.execute(f'''
        UPDATE "Clientes"
        SET "Status" = 'Ativo'
        WHERE "ID_Cliente" = {id_cliente}
        ''')
        conn.commit()

        print('-'*60)
        print("Cliente recadastrado com sucesso.")
        print('-'*60)


def cadastrar_cliente():                    #   Função para cadastrar novo cliente;
    system('cls')
    print(''' 
    - Cadastro de Cliente: 
    ''')

    nome = input("Digite o nome do cliente: ")
    cpfValido = False

    while cpfValido == False:
        cpf = input("Digite o CPF do cliente (somente números): ")

        try:
            if len(cpf) == 11 and cpf.isnumeric():
                cpfValido = True
            else:
                print("CPF inválido, digite novamente. (O CPF deve conter 11 dígitos e ter somente números).")
                cpfValido = False
        except:
            print("Ocorreu um erro, digite novamente.")
            cpfValido = False

    email = input("Digite o email do cliente (ou Enter para vazio): ")
    telefone = input("Digite o telefone do cliente (ou Enter para vazio): ")

    if email == "" and telefone == "":
        cur.execute(f'''
        INSERT INTO "Clientes"
        VALUES(DEFAULT, '{nome}', '{cpf}', DEFAULT, DEFAULT)
        ''')
        conn.commit()
    else:
        cur.execute(f'''
        INSERT INTO "Clientes"
        VALUES(DEFAULT, '{nome}', '{cpf}', '{email}', '{telefone}')
        ''')
        conn.commit()
    
    print('-'*60)
    print(f"O cliente {nome} foi cadastrado com sucesso.")
    print('-'*60)


def atualizar_cliente():                    #   Função para atualizar dados de Cliente cadastrado;
    system('cls')
    print(''' 
    - Atualizar Cliente:
    ''')
    
    mostrar_clientes()
    print()
    cliente_escolhido = input("Digite o ID do cliente que deseja atualizar: ")

    ver_cliente_especifico(cliente_escolhido)
    print()
    novo_nome = input("Digite o novo nome (digite Enter para não alterar): ")
    novo_cpf = input("Digite o novo CPF (digite Enter para não alterar): ")
    novo_email = input("Digite o novo email (digite Enter para não alterar): ")
    novo_telefone = input("Digite o novo telefone (digite Enter para não alterar): ")

    if novo_nome:
        cur.execute(f'''
        UPDATE "Clientes"
        SET "Nome_Cliente" = '{novo_nome}'
        WHERE "ID_Cliente" = {cliente_escolhido}
        ''')
        conn.commit()
    
    if novo_cpf:
        cur.execute(f'''
        UPDATE "Clientes"
        SET "CPF" = '{novo_cpf}'
        WHERE "ID_Cliente" = {cliente_escolhido}
        ''')
        conn.commit()
    
    if novo_email:
        cur.execute(f'''
        UPDATE "Clientes"
        SET "Email" = '{novo_email}'
        WHERE "ID_Cliente" = {cliente_escolhido}
        ''')
        conn.commit()
    
    if novo_telefone:
        cur.execute(f'''
        UPDATE "Clientes"
        SET "Telefone" = '{novo_telefone}'
        WHERE "ID_Cliente" = {cliente_escolhido}
        ''')
        conn.commit()

    print('-'*60)
    print("Alteração realizada com sucesso!")
    print('-'*60)


def ver_cliente_especifico(id_cliente):     #   Função para visualizar Cliente específico;

    cur.execute(f'''SELECT * FROM "Clientes"
    WHERE "ID_Cliente" = {id_cliente}
    ORDER BY "ID_Cliente"
    ''')

    print('''
    Cliente Escolhido: 
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    tabela = PrettyTable(colunas)
    for linha in linhas:
        tabela.add_row(linha)

    print(tabela)

#   Função para visualizar Cliente específico ao remover, também mostra as compras do Cliente escolhido;

def ver_cliente_espec_remover(id_cliente):

    cur.execute(f'''SELECT * FROM "Clientes"
    WHERE "ID_Cliente" = {id_cliente}
    ORDER BY "ID_Cliente"
    ''')

    print('''
    Cliente Escolhido: 
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    tabela = PrettyTable(colunas)
    for linha in linhas:
        tabela.add_row(linha)

    print(tabela)

    cur.execute(f'''SELECT * FROM "Compras"
    WHERE "ID_Cliente" = {id_cliente}
    ORDER BY "ID_Compra"
    ''')

    print('''
    Compras do Cliente Escolhido: 
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    tabela = PrettyTable(colunas)
    for linha in linhas:
        tabela.add_row(linha)

    print(tabela)

#   Função para remover Cliente cadastrado (não é removido do BD, somente altera o Status para 'Inativo');

def remover_cliente():
    system('cls')
    print('''
      - Remover Cliente: 
      ''')
    
    mostrar_clientes()
    print()
    cliente_escolhido = input("Digite o ID do cliente que deseja remover: ")

    ver_cliente_espec_remover(cliente_escolhido)
    print()
    confirmar = input("Deseja remover este cliente? (S/N) ").upper()

    match confirmar:
        case "S":
            cur.execute(f'''
            UPDATE "Clientes"
            SET "Status" = 'Inativo'
            WHERE "ID_Cliente" = '{cliente_escolhido}'
            ''')
            conn.commit()

            print('-'*60)
            print("Cliente removido com sucesso.")
            print('-'*60)

        case "N":
            print('-'*60)
            print("Voltando ao menu.")
            print('-'*60)

        case _:
            print('-'*60)
            print("Opção inválida. Voltando ao menu.")
            print('-'*60)
