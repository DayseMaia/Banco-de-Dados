import PySimpleGUI as sg
import psycopg2
import clientes
import produtos

conn = psycopg2.connect(
    host="localhost",
    database="Farmacia",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

################################### COMPRAS ###################################

def menu_compras():
    layout = [
        [sg.Text("Menu Compras", font=('Arial', 14, 'bold'))],
        [sg.Button('Lista de Compras', size=(20, 2), button_color=('white', '#4e8cff')), sg.Button('Cadastrar Nova Compra', size=(20, 2), button_color=('white', '#4e8cff'))],
        [sg.Button('Atualizar Compra', size=(20, 2), button_color=('white', '#4e8cff')), sg.Button('Remover Compra', size=(20, 2), button_color=('white', '#4e8cff'))],
        [sg.Button('Menu Principal', size=(20, 2), button_color=('white', '#e74c3c'))],
    ]
    
    window = sg.Window('Farmácia NinhoFarma', layout, size=(380, 200))
    
    while True:
        event, _ = window.read()

        if event == 'Lista de Compras':
            mostrar_compras()
        elif event == 'Cadastrar Nova Compra':
            cadastrar_compra(cur)
        elif event == 'Atualizar Compra':
            atualizar_compra(cur)
        elif event == 'Remover Compra':
            remover_compra()
        elif event == 'Menu Principal' or event == sg.WINDOW_CLOSED:
            break
    
    window.close()


def mostrar_compras():
    cur.execute('''
    SELECT * FROM "Compras"
    ORDER BY "ID_Compra"
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    tabela = []
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

        tabela.append(linha)

    layout = [
        [sg.Text('Lista de Compras:', font=('Arial', 14, 'bold'))],
        [sg.Table(values=tabela, headings=colunas, max_col_width=25, auto_size_columns=True,
                  justification='center', key='-TABLE-')],
        [sg.Button('Fechar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Lista de Compras', layout)

    while True:
        event, _ = window.read()

        if event == 'Fechar' or event == sg.WINDOW_CLOSED:
            break

    window.close()


def cadastrar_compra(cur):
    layout = [
        [sg.Text('Cadastro de Compra', font=('Arial', 14, 'bold'))],
        [sg.Text('Cliente:', font=('Arial', 12, 'bold'))],
        [sg.Listbox(values=clientes.get_clientes(cur), size=(30, 4), key='cliente')],
        [sg.Text('Produto:', font=('Arial', 12, 'bold'))],
        [sg.Listbox(values=produtos.get_produtos(cur), size=(30, 4), key='produto')],
        [sg.Text('Quantidade: *', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='quantidade')],
        [sg.Text('Preenchimento obrigatório (*)', font=('Arial', 10, 'bold'))],
        [sg.Button('Cadastrar', button_color=('white', '#4e8cff')), sg.Button('Cancelar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Farmácia NinhoFarma', layout)

    while True:
        event, values = window.read()

        if event == 'Cadastrar':
            cliente = values['cliente'][0].split(' - ')[0]
            produto = values['produto'][0].split(' - ')[0]
            quantidade = int(values['quantidade'])

            cur.execute(f'''
            SELECT "Valor_Produto", "Estoque_Produto" FROM "Produtos"
            WHERE "ID_Produto" = {produto}
            ''')
            
            result = cur.fetchone()
            valor_produto, estoque_produto = result[0], result[1]

            if quantidade > estoque_produto or estoque_produto == 0:
                sg.Popup("Produto sem estoque.\n", font=('Arial', 10, 'bold'), title='!')
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

                sg.Popup(f"Compra realizada com sucesso.\nValor total da compra: {valor_total}", font=('Arial', 10, 'bold'), title="Cadastro de Compra")
                break
        elif event == 'Cancelar' or event == sg.WINDOW_CLOSED:
            break

    window.close()


def atualizar_compra(cur):
    layout = [
        [sg.Text('Atualizar Compra', font=('Arial', 14, 'bold'))],
        [sg.Text('Compras:', font=('Arial', 12, 'bold'))],
        [sg.Listbox(values=get_compras(cur), size=(30,4), key='compras')],
        [sg.Button('Selecionar', button_color=('white', '#4e8cff'))],
        [sg.Text('Novo ID Cliente:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='novo_id_cliente')],
        [sg.Text('Novo ID Produto:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='novo_id_produto')],
        [sg.Text('Nova quantidade:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='nova_quantidade')],
        [sg.Text("Novo valor total:", font=('Arial', 10, 'bold'))], 
        [sg.Input(key='novo_valor_total')],
        [sg.Button('Atualizar', button_color=('white', '#4e8cff')), sg.Button('Cancelar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Farmácia NinhoFarma', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancelar':
            break

        if event == 'Selecionar':
            compra_escolhida = values['compras'][0].split(' - ')[0]
            ver_compra_especifica(compra_escolhida, cur)

        if event == 'Atualizar':
            compra_escolhida = values['compras'][0].split(' - ')[0]
            novo_id_cliente = values['novo_id_cliente']
            novo_id_produto = values['novo_id_produto']
            nova_quantidade = values['nova_quantidade']
            novo_valor_total = values['novo_valor_total']

            if novo_id_cliente:
                cur.execute(f'''
                UPDATE "Compras"
                SET "ID_Cliente" = '{novo_id_cliente}'
                WHERE "ID_Compra" = {compra_escolhida}
                ''')
                conn.commit()

            if novo_id_produto:
                cur.execute(f'''
                UPDATE "Compras"
                SET "ID_Produto" = '{novo_id_produto}'
                WHERE "ID_Compra" = {compra_escolhida}
                ''')
                conn.commit()

            if nova_quantidade:
                cur.execute(f'''
                UPDATE "Compras"
                SET "Quantidade" = '{nova_quantidade}'
                WHERE "ID_Compra" = {compra_escolhida}
                ''')
                conn.commit()

            if novo_valor_total:
                cur.execute(f'''
                UPDATE "Compras"
                SET "Valor_Total" = '{novo_valor_total}'
                WHERE "ID_Compra" = {compra_escolhida}
                ''')
                conn.commit()

            sg.Popup("Alteração realizada com sucesso!\n", font=('Arial', 10, 'bold'))
            break

    window.close()


def ver_compra_especifica(id_compra, cur):
    cur.execute(f'''
    SELECT * FROM "Compras"
    WHERE "ID_Compra" = {id_compra}
    ORDER BY "ID_Compra"
    ''')

    compra = cur.fetchone()

    layout = [
        [sg.Text('Compra:', font=('Arial', 12, 'bold'))],
        [sg.Text(f'ID Compra: {compra[0]}', font=('Arial', 10, 'bold'))],
        [sg.Text(f'ID Cliente: {compra[1]}', font=('Arial', 10, 'bold'))],
        [sg.Text(f'ID Produto: {compra[2]}', font=('Arial', 10, 'bold'))],
        [sg.Text(f'Quantidade: {compra[3]}', font=('Arial', 10, 'bold'))],
        [sg.Text(f'Valor Total: {compra[4]}', font=('Arial', 10, 'bold'))],
        [sg.Text(f'Data da venda: {compra[5]}', font=('Arial', 10, 'bold'))],
        [sg.Button('Fechar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Farmácia NinhoFarma', layout)

    while True:
        event, _ = window.read()

        if event == 'Fechar' or sg.WINDOW_CLOSED:
            break

    window.close()


def remover_compra():
    cur.execute('''
    SELECT * FROM "Compras"
    ORDER BY "ID_Compra"
    ''')
    
    colunas = [desc[0] for desc in cur.description]
    linhas = cur.fetchall()
    tabela_produtos = [[str(cell) for cell in linha] for linha in linhas]

    layout = [
        [sg.Text('Lista de Compras:', font=('Arial', 14, 'bold'))],
        [sg.Table(values=tabela_produtos, headings=colunas, key='tabela_compra', justification='center')],
        [sg.Button('Excluir Compra', button_color=('white', '#4e8cff')), sg.Button('Fechar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Remover Compra', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Fechar':
            break
        elif event == 'Excluir Compra':
            selecionar_linhas = values['tabela_compra']
            if selecionar_linhas:
                compra_escolhida = tabela_produtos[selecionar_linhas[0]][0]

                confirmar = sg.popup_yes_no('Deseja remover esta compra?\n', font=('Arial', 10, 'bold'), title='Remover Compra')

                if confirmar == 'Yes':
                    cur.execute(f'''
                        DELETE FROM "Compras"
                        WHERE "ID_Compra" = '{compra_escolhida}'
                    ''')
                    conn.commit()
                    sg.popup('Compra removida com sucesso.\n', font=('Arial', 10, 'bold'), title='!')
                else:
                    sg.popup('Operação cancelada.\n', font=('Arial', 10, 'bold'), title='!')
            else:
                sg.popup('Nenhuma compra selecionada.\n', font=('Arial', 10, 'bold'), title='Erro!')

    window.close()


def get_compras(cur):
    cur.execute('''
    SELECT "ID_Compra", "ID_Cliente" FROM "Compras"
    ORDER BY "ID_Compra"
    ''')

    compras = cur.fetchall()
    options = [f"{compra[0]} - {compra[1]}" for compra in compras]
    return options
