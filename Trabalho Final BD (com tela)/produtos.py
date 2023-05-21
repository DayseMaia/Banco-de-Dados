import PySimpleGUI as sg
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="Farmacia",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

################################### PRODUTOS ###################################

def menu_produtos():
    layout = [
        [sg.Text("Menu Produtos", font=('Arial', 14, 'bold'))],
        [sg.Button('Lista de Produtos', size=(20, 2), button_color=('white', '#357599')), sg.Button('Cadastrar Novo Produto', size=(20, 2), button_color=('white', '#357599'))],
        [sg.Button('Atualizar Produto', size=(20, 2), button_color=('white', '#357599')), sg.Button('Remover Produto', size=(20, 2), button_color=('white', '#357599'))],
        [sg.Button('Menu Principal', size=(20, 2), button_color=('white', '#e74c3c'))],
    ]
    
    window = sg.Window('Farmácia NinhoFarma', layout, size=(380, 200))
    
    while True:
        event, _ = window.read()

        if event == 'Lista de Produtos':
            mostrar_produtos()
        elif event == 'Cadastrar Novo Produto':
            cadastrar_produto()
        elif event == 'Atualizar Produto':
            atualizar_produto(cur)
        elif event == 'Remover Produto':
            remover_produto()
        elif event == 'Menu Principal' or event == sg.WINDOW_CLOSED:
            break
    
    window.close()

def mostrar_produtos():
    cur.execute('''
    SELECT * FROM "Produtos"
    ORDER BY "ID_Produto"
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    data = []
    for linha in linhas:
        data.append(list(linha))

    layout = [
        [sg.Text('Lista de Produtos', font=('Arial', 14, 'bold'))],
        [sg.Table(values=data, headings=colunas, max_col_width=25, background_color='#F7F3EC', auto_size_columns=True,
                  justification='center', text_color='black')],
        [sg.Button('Voltar ao menu', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Farmácia NinhoFarma', layout)

    while True:
        event, _ = window.read()
        if event == 'Voltar ao menu' or event == sg.WINDOW_CLOSED:
            break

    window.close()


def cadastrar_produto():
    layout = [
        [sg.Text('Cadastro de Produtos', font=('Arial', 14, 'bold'))],
        [sg.Text('Nome: *', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='nome')],
        [sg.Text('Valor: *', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='valor')],
        [sg.Text('Estoque: *', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='estoque')],
        [sg.Text('Preenchimento obrigatório (*)', font=('Arial', 10, 'bold'))],
        [sg.Button('Cadastrar', button_color=('white', '#357599')), sg.Button('Cancelar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Farmácia NinhoFarma', layout)

    while True:
        event, values = window.read()

        if event == 'Cadastrar':
            nome = values['nome']
            valor = values['valor']
            estoque = values['estoque']

            cur.execute(f'''
            INSERT INTO "Produtos"
            VALUES(DEFAULT, '{nome}', '{valor}', '{estoque}')
            ''')
            conn.commit()

            sg.Popup(f"O produto {nome} foi cadastrado com sucesso.\n", font=('Arial', 10, 'bold'), title="Cadastro de Produto")
            break
        elif event == 'Cancelar' or event == sg.WINDOW_CLOSED:
            break

    window.close()


def atualizar_produto(cur):
    layout = [
        [sg.Text('Atualizar Produto', font=('Arial', 14, 'bold'))],
        [sg.Text('Produtos:', font=('Arial', 12, 'bold'))],
        [sg.Listbox(values=get_produtos(cur), size=(30,4), key='produtos')],
        [sg.Button('Selecionar', button_color=('white', '#357599'))],
        [sg.Text('Novo Nome:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='novo_nome')],
        [sg.Text('Novo Valor:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='novo_valor')],
        [sg.Text('Novo Estoque:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='novo_estoque')],
        [sg.Button('Atualizar', button_color=('white', '#357599')), sg.Button('Cancelar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Farmácia NinhoFarma', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancelar':
            break

        if event == 'Selecionar':
            produto_escolhido = values['produtos'][0].split(' - ')[0]
            ver_produto_especifico(produto_escolhido, cur)
        
        if event == 'Atualizar':
            produto_escolhido = values['produtos'][0].split(' - ')[0]
            novo_nome = values['novo_nome']
            novo_valor = values['novo_valor']
            novo_estoque = values['novo_estoque']

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

            sg.Popup("Alteração realizada com sucesso!\n", font=('Arial', 10, 'bold'))
            break

    window.close()


def ver_produto_especifico(id_produto, cur):
    cur.execute(f'''
    SELECT * FROM "Produtos"
    WHERE "ID_Produto" = {id_produto}
    ORDER BY "ID_Produto"
    ''')

    produto = cur.fetchone()

    layout = [
        [sg.Text('Produto:', font=('Arial', 12, 'bold'))],
        [sg.Text(f'ID: {produto[0]}', font=('Arial', 10, 'bold'))],
        [sg.Text(f'Nome: {produto[1]}', font=('Arial', 10, 'bold'))],
        [sg.Text(f'Valor: {produto[2]}', font=('Arial', 10, 'bold'))],
        [sg.Text(f'Estoque: {produto[3]}', font=('Arial', 10, 'bold'))],
        [sg.Button('Fechar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Farmácia NinhoFarma', layout)

    while True:
        event, _ = window.read()

        if event == 'Fechar' or sg.WINDOW_CLOSED:
            break

    window.close()


def remover_produto():
    cur.execute('''
    SELECT * FROM "Produtos"
    ORDER BY "ID_Produto"
    ''')
    
    colunas = [desc[0] for desc in cur.description]
    linhas = cur.fetchall()
    tabela_produtos = [[str(cell) for cell in linha] for linha in linhas]

    layout = [
        [sg.Text('Lista de Produtos:', font=('Arial', 14, 'bold'))],
        [sg.Table(values=tabela_produtos, headings=colunas, key='tabela_produto', justification='center')],
        [sg.Button('Excluir Produto', button_color=('white', '#357599')), sg.Button('Fechar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Remover Produto', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Fechar':
            break
        elif event == 'Excluir Produto':
            selecionar_linhas = values['tabela_produto']
            if selecionar_linhas:
                produto_escolhido = tabela_produtos[selecionar_linhas[0]][0]

                confirmar = sg.popup_yes_no('Deseja remover este produto?\n', font=('Arial', 10, 'bold'), title='Remover Produto')

                if confirmar == 'Yes':
                    cur.execute(f'''
                        DELETE FROM "Produtos"
                        WHERE "ID_Produto" = '{produto_escolhido}'
                    ''')
                    conn.commit()
                    sg.popup('Produto removido com sucesso.\n', font=('Arial', 10, 'bold'), title='!')
                else:
                    sg.popup('Operação cancelada.\n', font=('Arial', 10, 'bold'), title='!')
            else:
                sg.popup('Nenhum produto selecionado.\n', font=('Arial', 10, 'bold'), title='Erro!')

    window.close()


def get_produtos(cur):
    cur.execute('''
    SELECT "ID_Produto", "Nome_Produto" FROM "Produtos"
    ORDER BY "ID_Produto"
    ''')

    produtos = cur.fetchall()
    options = [f"{produto[0]} - {produto[1]}" for produto in produtos]
    return options
