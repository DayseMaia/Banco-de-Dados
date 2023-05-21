import PySimpleGUI as sg
import psycopg2
import emojipy

conn = psycopg2.connect(
    host="localhost",
    database="Farmacia",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()


def menu_clientes():
    layout = [
        [sg.Text("Menu Clientes", font=('Arial', 14, 'bold'))],
        [sg.Button('Lista de Clientes', size=(20, 2), button_color=('white', '#304d63')), sg.Button('Cadastrar Novo Cliente', size=(20, 2), button_color=('white', '#304d63'))],
        [sg.Button('Atualizar Cliente', size=(20, 2), button_color=('white', '#304d63')), sg.Button('Remover Cliente', size=(20, 2), button_color=('white', '#304d63'))],
        [sg.Button('Lista de Clientes Inativos', size=(20, 2), button_color=('white', '#304d63')), sg.Button('Menu Principal', size=(20, 2), button_color=('white', '#e74c3c'))],
    ]
    
    window = sg.Window('Farmácia NinhoFarma', layout, size=(380, 200))
    
    while True:
        event, _ = window.read()

        if event == 'Lista de Clientes':
            mostrar_clientes()
        elif event == 'Cadastrar Novo Cliente':
            cadastrar_cliente()
        elif event == 'Atualizar Cliente':
            atualizar_cliente(cur)
        elif event == 'Remover Cliente':
            remover_cliente()
        elif event == 'Lista de Clientes Inativos':
            mostrar_clientes_inativos()
        elif event == 'Menu Principal' or event == sg.WINDOW_CLOSED:
            break
    
    window.close()

def mostrar_clientes():
    cur.execute('''
    SELECT * FROM "Clientes"
    WHERE "Status" = 'Ativo'
    ORDER BY "ID_Cliente"
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    data = []
    for linha in linhas:
        data.append(list(linha))

    layout = [
        [sg.Text('Lista de Clientes', font=('Arial', 14, 'bold'))],
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


def cadastrar_cliente():
    layout = [
        [sg.Text('Cadastro de Cliente', font=('Arial', 14, 'bold'))],
        [sg.Text('Nome: *', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='nome')],
        [sg.Text('CPF (somente números): *', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='cpf')],
        [sg.Text('Email:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='email')],
        [sg.Text('Telefone:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='telefone')],
        [sg.Text('Preenchimento obrigatório (*)', font=('Arial', 10, 'bold'))],
        [sg.Button('Cadastrar', button_color=('white', '#4e8cff')), sg.Button('Cancelar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Farmácia NinhoFarma', layout)

    while True:
        event, values = window.read()

        if event == 'Cadastrar':
            nome = values['nome']
            cpf = values['cpf']
            email = values['email']
            telefone = values['telefone']

            if len(cpf) == 11 and cpf.isnumeric():
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

                sg.Popup(f"O cliente {nome} foi cadastrado com sucesso.\n", font=('Arial', 10, 'bold'), title="Cadastro de Cliente")
                break
            else:
                sg.Popup('''
CPF inválido!

O CPF deve conter 11 dígitos e ter somente números.
''', font=('Arial', 10, 'bold'), 
                title="CPF inválido!")
        elif event == 'Cancelar' or event == sg.WINDOW_CLOSED:
            break

    window.close()


def atualizar_cliente(cur):
    layout = [
        [sg.Text('Atualizar Cliente', font=('Arial', 14, 'bold'))],
        [sg.Text('Clientes:', font=('Arial', 12, 'bold'))],
        [sg.Listbox(values=get_clientes(cur), size=(30, 4), key='clientes')],
        [sg.Button('Selecionar', button_color=('white', '#4e8cff'))],
        [sg.Text('Novo Nome:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='novo_nome')],
        [sg.Text('Novo CPF:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='novo_cpf')],
        [sg.Text('Novo Email:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='novo_email')],
        [sg.Text('Novo Telefone:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='novo_telefone')],
        [sg.Button('Atualizar', button_color=('white', '#4e8cff')), sg.Button('Cancelar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Farmácia NinhoFarma', layout)

    while True:
        event, values = window.read()

        if event == 'Selecionar':
            cliente_escolhido = values['clientes'][0].split(' - ')[0]
            ver_cliente_especifico(cliente_escolhido, cur)
        elif event == 'Atualizar':
            cliente_escolhido = values['clientes'][0].split(' - ')[0]
            novo_nome = values['novo_nome']
            novo_cpf = values['novo_cpf']
            novo_email = values['novo_email']
            novo_telefone = values['novo_telefone']

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

            sg.Popup("Alteração realizada com sucesso!\n", font=('Arial', 10, 'bold'))
            break
        elif event == 'Cancelar' or event == sg.WINDOW_CLOSED:
            break

    window.close()


def ver_cliente_especifico(id_cliente, cur):
    cur.execute(f'''
    SELECT * FROM "Clientes"
    WHERE "ID_Cliente" = {id_cliente}
    ORDER BY "ID_Cliente"
    ''')

    cliente = cur.fetchone()

    layout = [
        [sg.Text('Cliente:', font=('Arial', 12, 'bold'))],
        [sg.Text(f'ID: {cliente[0]}', font=('Arial', 10, 'bold'))],
        [sg.Text(f'Nome: {cliente[1]}', font=('Arial', 10, 'bold'))],
        [sg.Text(f'CPF: {cliente[2]}', font=('Arial', 10, 'bold'))],
        [sg.Text(f'Email: {cliente[3]}', font=('Arial', 10, 'bold'))],
        [sg.Text(f'Telefone: {cliente[4]}', font=('Arial', 10, 'bold'))],
        [sg.Button('Fechar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Farmácia NinhoFarma', layout)

    while True:
        event, _ = window.read()
        if event == 'Fechar' or sg.WINDOW_CLOSED:
            break

    window.close()


def remover_cliente():
    cur.execute('''
    SELECT * FROM "Clientes"
    WHERE "Status" = 'Ativo' 
    ORDER BY "ID_Cliente"
    ''')
    
    colunas = [desc[0] for desc in cur.description]
    linhas = cur.fetchall()
    tabela_clientes = [[str(cell) for cell in linha] for linha in linhas]

    layout = [
        [sg.Text('Lista de Clientes:', font=('Arial', 14, 'bold'))],
        [sg.Table(values=tabela_clientes, headings=colunas, key='tabela_cliente', justification='center')],
        [sg.Button('Excluir Cliente', button_color=('white', '#4e8cff')), sg.Button('Fechar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Remover Cliente', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Fechar':
            break
        elif event == 'Excluir Cliente':
            selecionar_linhas = values['tabela_cliente']
            if selecionar_linhas:
                cliente_escolhido = tabela_clientes[selecionar_linhas[0]][0]
                ver_cliente_espec_remover(cliente_escolhido)

                confirmar = sg.popup_yes_no('Deseja remover este cliente?\n', font=('Arial', 10, 'bold'), title='Remover Cliente')

                if confirmar == 'Yes':
                    cur.execute(f'''
                        UPDATE "Clientes"
                        SET "Status" = 'Inativo'
                        WHERE "ID_Cliente" = '{cliente_escolhido}'
                    ''')
                    conn.commit()
                    sg.popup('Cliente removido com sucesso.\n', font=('Arial', 10, 'bold'), title='!')
                else:
                    sg.popup('Operação cancelada.\n', font=('Arial', 10, 'bold'), title='!')
            else:
                sg.popup('Nenhum cliente selecionado.\n', font=('Arial', 10, 'bold'), title='Erro!')

    window.close()


def ver_cliente_espec_remover(id_cliente):
    cur.execute(f'''
    SELECT * FROM "Clientes"
    WHERE "ID_Cliente" = {id_cliente}
    ORDER BY "ID_Cliente"
    ''')

    colunas = [desc[0] for desc in cur.description]
    linhas = cur.fetchall()

    tabela_clientes = [[str(cell) for cell in linha] for linha in linhas]

    cur.execute(f'''
    SELECT * FROM "Compras"
    WHERE "ID_Cliente" = {id_cliente}
    ORDER BY "ID_Compra"
    ''')

    colunas = [desc[0] for desc in cur.description]
    linhas = cur.fetchall()

    tabela_compras = [[str(cell) for cell in linha] for linha in linhas]

    layout = [
        [sg.Text('Cliente:', font=('Arial', 14, 'bold'))],
        [sg.Table(values=tabela_clientes, headings=colunas, justification='center', num_rows=min(3, 20))],
        [sg.Text('Compras do Cliente:', font=('Arial', 14, "bold"))],
        [sg.Table(values=tabela_compras, headings=colunas, justification='center', num_rows=min(3, 20))],
        [sg.Button('Fechar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Detalhes do Cliente', layout)

    while True:
        event, _ = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Fechar':
            break

    window.close()


def mostrar_clientes_inativos():
    cur.execute('''
    SELECT * FROM "Clientes"
    WHERE "Status" = 'Inativo' 
    ORDER BY "ID_Cliente"
    ''')
    
    colunas = [desc[0] for desc in cur.description]
    linhas = cur.fetchall()
    tabela_clientes = [[str(cell) for cell in linha] for linha in linhas]

    layout = [
        [sg.Text('Lista de Clientes Inativos:', font=('Arial', 14, 'bold'))],
        [sg.Table(values=tabela_clientes, headings=colunas, key='tabela_cliente', justification='center')],
        [sg.Button('Recadastrar Cliente', button_color=('white', '#4e8cff')), sg.Button('Fechar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Cliente Inativos', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Fechar':
            break
        elif event == 'Recadastrar Cliente':
            selecionar_linhas = values['tabela_cliente']
            if selecionar_linhas:
                id_cliente = tabela_clientes[selecionar_linhas[0]][0]

                confirmar = sg.popup_yes_no('Deseja recadastrar este cliente?\n', font=('Arial', 10, 'bold'), title='Recadastro')

                if confirmar == 'Yes':
                    cur.execute(f'''
                    UPDATE "Clientes"
                    SET "Status" = 'Ativo'
                    WHERE "ID_Cliente" = {id_cliente}
                    ''')
                    conn.commit()
                    sg.popup('Cliente recadastrado com sucesso.\n', font=('Arial', 10, 'bold'), title='!')
                else:
                    sg.popup('Operação cancelada.\n', font=('Arial', 10, 'bold'), title='!')
            else:
                sg.popup('Nenhum cliente selecionado.\n', font=('Arial', 10, 'bold'), title='Erro!')

    window.close()

def get_clientes(cur):
    cur.execute('''
    SELECT "ID_Cliente", "Nome_Cliente" FROM "Clientes"
    WHERE "Status" = 'Ativo'
    ORDER BY "ID_Cliente"
    ''')

    clientes = cur.fetchall()
    options = [f"{cliente[0]} - {cliente[1]}" for cliente in clientes]
    return options
