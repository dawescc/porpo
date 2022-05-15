import PySimpleGUI as sg
import pandas
import gui

sg.theme('DarkBlack1')

table = gui.DriverInfo.data
main_win_table = sg.Table(table)

main_top_frame_layout = [[main_win_table], [sg.Button('Okay'), sg.Button('Cancel')]]
main_top_frame = sg.Frame('Frame Title', main_top_frame_layout, vertical_alignment='top', expand_x=True, expand_y=True)

main_win_layout = [[main_top_frame], [sg.Button('Okay'), sg.Button('Cancel')]]
main_window = sg.Window('Main Window', main_win_layout, size=(400, 400))

while True:
    main_window_event, main_window_values = main_window.read()
    if main_window_event == sg.WIN_CLOSED or 'Cancel':
        break
    if main_window_event == 'Okay':
        break

main_window.close()
del main_window
