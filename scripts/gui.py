import PySimpleGUI as sg
import fastf1
from fastf1 import plotting
import matplotlib.pylab as plt
import os
import datetime

from matplotlib.pyplot import autoscale

class dirs:
    # Declare Cache & Export Paths
    cache_path = '~/Documents/F1 Data Analysis/Cache/'
    save_path = '~/Documents/F1 Data Analysis/Export/'

    # Check if Cache directory Exists
    CacheExist = os.path.exists(cache_path)
    # If it doesn't - Make it
    if not CacheExist:
        os.makedirs(cache_path)

    # Check if Cache directory Exists
    SaveExist = os.path.exists(save_path)
    # If it doesn't - Make it
    if not SaveExist:
        os.makedirs(save_path)

    # Enable Cache at Cache Path
    fastf1.Cache.enable_cache(cache_path)

class Years:
    # Create Year Range for Year Picker
    this_year = datetime.datetime.today().year
    list = list(range(2018, this_year+1))

class Input:
    season = fastf1.get_event_schedule(Years.this_year)
    gps = list(season['EventName'])

    if 'values' in locals():
        grand_prix = values['-GP MENU-']
        year = values['-YEAR MENU-']
        ses = values['-SES MENU-']
        driver = values['-DRIVER MENU-']
    else:
        grand_prix = f'{gps[0]}'
        year = int(f'{Years.this_year}')
        ses = 'FP1'
        driver = f'VER'

class Session:
    data = fastf1.get_session(Input.year, Input.grand_prix, Input.ses)
    data.load()
    results = data.results
    event = data.event['EventName']

class Driver:
    info = Session.data.get_driver(Input.driver)
    session = Session.data.laps.pick_driver(Input.driver)
    fullname = info['FullName']
    team = info['TeamName']
    team_color = fastf1.plotting.team_color(team)

    if 'values' in locals():
        lap_or_ses = values['-LAP MENU-']
    else:
        lap_or_ses = f'Fastest'

    if lap_or_ses == 'Lap':
        lap_num = int(sg.popup([sg.Slider((session['LapNumber'].min(), session['LapNumber'].max()), orientation='h')]))
        lap_n = session[session['LapNumber'] == lap_num]
        lap_n_tel = lap_n.get_telemetry()
        # Define Lap N Data for Selection
        data = lap_n_tel
        title = f'{fullname} {Session.event} Lap {lap_num} Data:'
        def_xvalue = f'Distance'
        def_yvalue = f'Speed'
        

    elif lap_or_ses == 'Fastest Lap':
        personal_best = session.pick_fastest()
        fast_lap = personal_best.get_telemetry()
        # Define Fastest Lap Data for Selection
        data = fast_lap
        title = f'{fullname} {Session.event} Fastest Lap Data:'
        def_xvalue = f'Distance'
        def_yvalue = f'Speed'

    else:
        # Define Full Session Data for Selection
        data = session
        title = f'{fullname} {Session.event} Full Session Data:'
        def_xvalue = f'LapNumber'
        def_yvalue = f'LapTime'

class Lists:
        sessions = ['FP1', 'FP2', 'FP3', 'S', 'Q', 'R']
        lap_or_ses = ['Lap', 'Full Session', 'Fastest Lap']
        years = Years.list
        gps = Input.gps
        drivers = list(Session.results['Abbreviation'])
        vars = list(Driver.data)

class Data:
    if 'values' in locals():
        y = values['-Y VAR-']
        x = values['-X VAR-']
        req_dat_y = Lists.vars[y]
        req_dat_x = Lists.vars[x]
    else:
        y = 6
        x = 12
        req_dat_y = Lists.vars[y]
        req_dat_x = Lists.vars[x]


# Define Make Window Function
def make_window():
    sg.theme('DarkBlack')
    menu_def = [['&porpo', ['&About', '&Preferences', 'E&xit']]]
    right_click_menu_def = [[], ['Edit Me', 'Please!']]

    gp_layout = [
        [sg.Text('Select the year of Grand Prix:')],
        [sg.OptionMenu(Lists.years, default_value=f'{Lists.years[-1]}', k='-YEAR MENU-')],
        [sg.Button('Load GPs')],
        
        [sg.Text('Select Grand Prix:')],
        [sg.OptionMenu(Lists.gps, k='-GP MENU-')],
        
        [sg.Text('Select Session:')],
        [sg.OptionMenu(Lists.sessions, default_value=Lists.sessions[0], k='-SES MENU-')],
        [sg.Button('Load Drivers')]]


    driver_layout = [
        [sg.Text('Select Driver:')],
        [sg.OptionMenu(Lists.drivers, default_value=Lists.drivers[0], k='-DRIVER MENU-')],
        [sg.Button('Load Data')]]


    lap_layout = [
        [sg.Text('Evaluate session or lap?')],
        [sg.OptionMenu(Lists.lap_or_ses, default_value=Lists.lap_or_ses[0], k='-LAP MENU-')],
        [sg.Button('Load Variables')]]


    var_layout = [
        [sg.Text(f'{Driver.title}')],
        [sg.Text('Y Variable:')], [sg.OptionMenu(Lists.vars, default_value=Driver.def_yvalue, k='-Y VAR-')],
        [sg.Text('X Variable:')], [sg.OptionMenu(Lists.vars, default_value=Driver.def_xvalue, k='-X VAR-')],
        [sg.Button('Plot', expand_x=True)]]


    preferences_layout = []



    frame_layout = [[sg.Image(source='src/common/images/icon_small.png', expand_x=True, expand_y=True, key='-LOGO-')]]
    layout = [
        [sg.MenubarCustom(menu_def, key='-MENU-')],
        [sg.Frame('Home', frame_layout, expand_x=True, expand_y=True,)]
    ]
    
    layout += [[sg.TabGroup([[sg.Tab('Grand Prix', gp_layout),
                              sg.Tab('Drivers', driver_layout),
                              sg.Tab('Laps', lap_layout),
                              sg.Tab('Variables', var_layout)]], key='-TAB GROUP-', expand_x=True, expand_y=True),

                ]]

    window = sg.Window('porpo', layout, right_click_menu=right_click_menu_def,
                       right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0, 0),
                       use_custom_titlebar=True, finalize=True, keep_on_top=True, #scaling=2.0,
                       )

    window.set_min_size(window.size)
    return window


def main():
    window = make_window()

    # Window Open, Begin Event Loop
    while True:
        event, values = window.read(timeout=100)
        
        # Menu Items
        # Exit
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break

        # Menu Items
        # About
        elif event == 'About':
            print("[LOG] Clicked About")
            sg.popup('About porpo',
                     'GitHub',
                     'Twitter',
                     keep_on_top=True)

        # Menu Items
        # Preferences
        elif event == 'Preferences':
            print("[LOG] Clicked Preferences")
            sg.popup('porpo preferences', keep_on_top=True)

        # Grand Prix Items
        # Load GPs
        elif event == 'Load GPs':
            print(f"[LOG] Load Grand Prix for {values['-YEAR MENU-']}")
            
            update = list(var)
            window.Element('-GP MENU-').update(values=update)

        # Grand Prix Items
        # Load Drivers        
        elif event == 'Load Drivers':
            print(f"[LOG] Load Drivers for {values['-GP MENU-']}!")
            window.close()
            window = make_window()

    window.close()
    exit(0)


if __name__ == '__main__':
    sg.theme('DarkRed')
    main()
else:
    sg.theme('DarkRed')
    main()