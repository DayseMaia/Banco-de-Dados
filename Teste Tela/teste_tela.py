import PySimpleGUI as sg

def main():
    sg.theme('BlueMono')

    layout = [
        [sg.Column([[sg.Text('Sistema de Gerenciamento NinhoFarma', justification='center', auto_size_text=(20,20))]])],
        [
            sg.Column([
                [sg.Button(image_filename='images/clientes.png', image_size=(100,100))],
                [sg.Text('Clientes')]
            ]),
            sg.Column([
                [sg.Button(image_filename='images/produtos.png', image_size=(100,100))],
                [sg.Text('Produtos')]
            ]),
            sg.Column([
                [sg.Button(image_filename='images/compras.png', image_size=(100,100))],
                [sg.Text('Compras')]
            ])
        ]
    ]

    window = sg.Window('NinhoFarma', layout, size=(800, 600))

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

    window.close()

if __name__ == "__main__":
    main()
