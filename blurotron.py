import PySimpleGUI as sg
from blur_protocol import blur

sg.theme('Topanga')

layout = [[sg.Text('Input:'), sg.Input(key='-IN-'),sg.FileBrowse(key="-IN-")],
          [sg.Text('Output (write in a .mp4 extension):'), sg.Input(key='-OUTPUT-')],
          [sg.Button('Blur'), sg.Button('Exit')]]

window = sg.Window('Blur-o-tron', layout)

while True:  # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Blur':
        blur(values['-IN-'],values['-OUTPUT-'])

window.close()


