import psycopg2                             #   Importando biblioteca para conexão com o Banco de Dados;
from prettytable import PrettyTable         #   Importando biblioteca que imprime tabelas;
                                            #   Criando conexão com o Banco de Dados;
conn = psycopg2.connect(
    host = "localhost",
    database = "Farmacia",
    user = "postgres",
    password = "postgres"
)

cur = conn.cursor()                         #   Criando cursor;

def menu_clientes():                        #   Menu Clientes;

    while True:
        
        print('''
        
        Menu Clientes:
        
        1. Ver lista de Clientes
        2. Cadastrar Novo Cliente
        3. Atualizar Cliente
        4. Remover Cliente
        5. Ver Clientes Inativos
        0. Voltar ao menu principal
        
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
                print("Voltando ao menu principal...")
                print('-'*60)
                break
            case _:
                print("Opção inválida! Escolha uma opção válida.")
                print('-'*60)

        input("Digite Enter para continuar...")

                                            #   Função mostrar clientes;

def mostrar_clientes():
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

                                            #   Função mostrar clientes removidos;

def mostrar_clientes_inativos():
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
            print("Voltando ao menu principal.")
            print('-'*60)

        case _:
            print("Opção inválida. Voltando ao menu.")
            print('-'*60)

                                            #   Função para recadastrar clientes removidos;

def recadastrar_cliente(id_cliente):
        cur.execute(f'''
        UPDATE "Clientes"
        SET "Status" = 'Ativo'
        WHERE "ID_Cliente" = {id_cliente}
        ''')
        conn.commit()

        print("Cliente recadastrado com sucesso.")
        print('-'*60)

                                            #   Função para cadastrar novo cliente;

def cadastrar_cliente():
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
    
    print(f"O cliente {nome} foi cadastrado com sucesso.")
    print('-'*60)

                                            #   Função para cadastrar Cliente cadastrado;

def atualizar_cliente():

    print(''' 
    - Atualizar Cliente:
    ''')
    
    mostrar_clientes()

    cliente_escolhido = input("Digite o ID do cliente: ")

    ver_cliente_especifico(cliente_escolhido)

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

    print("Alteração realizada com sucesso!")
    print('-'*60)

                                            #   Função para ver Cliente específico;

def ver_cliente_especifico(id_cliente):

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

                                            #   Função para ver Cliente específico ao remover, também mostra as compras do Cliente escolhido;

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

                                            #   Função para remover Cliente (não é removido do BD, somente altera o Status para 'Inativo');

def remover_cliente():

    print('''
      - Remover Cliente: 
      ''')
    
    mostrar_clientes()

    cliente_escolhido = input("Digite o ID do cliente escolhido: ")

    ver_cliente_espec_remover(cliente_escolhido)

    confirmar = input("Deseja remover este cliente? (S/N) ").upper()

    match confirmar:
        case "S":
           cur.execute(f'''
           UPDATE "Clientes"
           SET "Status" = 'Inativo'
           WHERE "ID_Cliente" = '{cliente_escolhido}'
           ''')
           conn.commit()

           print("Cliente removido com sucesso.")
           print('-'*60)

        case "N":
            print("Voltando ao menu principal.")
            print('-'*60)

        case _:
            print("Opção inválida. Voltando ao menu.")
            print('-'*60)

                                            #   Menu Produtos;

def menu_produtos():

    while True:
        
        print('''
        
        Menu Produtos:
        
        1. Ver lista de Produtos
        2. Cadastrar Novo Produto
        3. Atualizar Produto
        4. Remover Produto
        0. Voltar ao menu principal
        
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
                print("Voltando ao menu principal...")
                print('-'*60)
                break
            case _:
                print("Opção inválida. Escolha uma opção válida.")
                print('-'*60)

        input("Digite Enter para continuar...")

                                            #   Função mostrar Produtos;

def mostrar_produtos():

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

                                            #   Função para cadastrar novo Produto;

def cadastrar_produto():
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

    print(f"O produto {nome} foi cadastrado com sucesso.")
    print('-'*60)

                                            #   Função para atualizar produto cadastrado;

def atualizar_produto():
    print(''' 
    - Atualizar Produto: 
    ''')
    
    mostrar_produtos()

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

    print("Alteração realizada com sucesso!")
    print('-'*60)

                                            #   Função para remover Produto;

def remover_produto():
    print(''' 
    - Remover Produto: 
    ''')
    
    mostrar_produtos()

    produto_escolhido = input("Digite o ID do produto: ")

    confirmar = input("Deseja mesmo remover este produto? (S/N) ").upper()

    match confirmar:
        case "S":
            remocao = cur.execute(f'''
            DELETE FROM "Produtos"
            WHERE "ID_Produto" = '{produto_escolhido}'
            ''')
            conn.commit()
           
            print("Produto removido com sucesso.")
            print('-'*60)

        case "N":
            print("Voltando ao menu principal.")
            print('-'*60)

        case _:
            print("Opção inválida. Voltando ao menu.")
            print('-'*60)

                                            #   Menu Compras;

def menu_compras():
    while True:
        
        print('''
        
        Menu Compras:
        
        1. Ver lista de Compras
        2. Cadastrar Nova Compra
        3. Atualizar Compra
        4. Remover Compra
        0. Voltar ao menu principal
        
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
                print("Voltando ao menu principal...")
                print('-'*60)
                break
            case _:
                print("Opção inválida! Escolha uma opção válida.")
                print('-'*60)

        input("Digite Enter para continuar...")

                                            #   Função mostrar Compras;

def mostrar_compras():

    cur.execute('''
    SELECT * FROM "Compras"
    ORDER BY "ID_Compra"
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    tabela = PrettyTable(colunas)
    for linha in linhas:
        tabela.add_row(linha)

    print(''' 
                            - Lista de Compras - 
    ''')
    print(tabela)

                                            #   Função para cadastrar nova Compra;

def cadastrar_compra(cur):
    print(''' 
    - Cadastro de Compra: 
    ''')

    mostrar_clientes()
    cliente = input("Digite o ID do cliente: ")

    mostrar_produtos()
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
    
    valor_total = valor_produto * quantidade

    cur.execute(f'''
    INSERT INTO "Compras"
    VALUES(DEFAULT, '{cliente}', '{produto}', '{quantidade}', '{valor_total}', DEFAULT)
    ''')
    conn.commit()

    print(f"Compra realizada com sucesso. Valor total da compra: {valor_total}")

                                            #   Função para atualizar Compra cadastrada;

def atualizar_compra():
    print(''' 
    - Atualizar Compra: 
    ''')
    
    mostrar_compras()

    compra_escolhida = input("Digite o ID da compra: ")

    novo_id_cliente = input("Digite o novo ID do cliente na compra (digite Enter para não alterar): ")
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

    print("Alteração realizada com sucesso!")
    print('-'*60)

                                            #   Função para remover Compra;

def remover_compra():
    print(''' 
    - Remover Compra: 
    ''')
    
    mostrar_compras()

    compra_escolhida = input("Digite o ID da compra: ")

    confirmar = input("Deseja mesmo remover essa compra? (S/N) ").upper()

    match confirmar:
        case "S":
            cur.execute(f'''
            DELETE FROM "Compras"
            WHERE "ID_Compra" = '{compra_escolhida}'
            ''')
            conn.commit()
           
            print("Compra removida com sucesso.")
            print('-'*60)

        case "N":
            print("Voltando ao menu principal.")
            print('-'*60)

        case _:
            print("Opção inválida. Voltando ao menu.")

                                            #   Função main;

def main():
    while True:

        print('''
    
    Bem vindo a Farmácia XYZ
    
    1. Menu Clientes
    2. Menu Produtos
    3. Menu Compras
    0. Sair
    
    ''')

        opcao = input("Escolha o menu que deseja acessar: ")

        match opcao:
            case "1":
                menu_clientes()
            case "2":
                menu_produtos()
            case "3":
                menu_compras()
            case "0":
                print("Saindo da aplicação...")
                cur.close()
                conn.close()
                break
            case _:
                print("Opção inválida! Escolha uma opção válida.")

                                            #   Chamando a função main para rodar o programa.

if __name__ == "__main__":
    main()
