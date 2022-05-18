import datetime
import os

import fastf1
import matplotlib.pylab as plt
import PySimpleGUI as sg
from fastf1 import plotting

###############################################
# Define Classes
###############################################

class dirs():
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

class Years():
    # Create Year Range for Year Picker
    this_year = datetime.datetime.today().year
    list = list(range(2018, this_year+1))

class Input():
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

class Session():
    data = fastf1.get_session(Input.year, Input.grand_prix, Input.ses)
    data.load()
    results = data.results
    event = data.event['EventName']

    def __init__(self):
        self.data.load()

class Driver():
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

class Lists():
        sessions = ['FP1', 'FP2', 'FP3', 'S', 'Q', 'R']
        lap_or_ses = ['Lap', 'Full Session', 'Fastest Lap']
        years = Years.list
        gps = Input.gps
        drivers = list(Session.results['Abbreviation'])
        vars = list(Driver.data)

class Data():
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

class Plot():
    def plot():
        driver_yvar = DriverInfo.data[f'{var_values[0]}']
        driver_xvar = DriverInfo.data[f'{var_values[1]}']

        plotting.setup_mpl()

        x = driver_xvar
        y = driver_yvar
        xmin, xmax = x.min(), x.max()

        fig = plt.figure(1, figsize=(16,9), constrained_layout=True)
        plot1 = fig.subplots()
        plot1.plot(x, y, color=DriverInfo.team_color, label=f"{y.name}")
        plot1.set_ylabel(f"{y.name}")
        plot1.set_xlabel(f"{x.name}")
        plot1.set_xlim(xmin, xmax)
        plot1.minorticks_on()
        plot1.grid(visible=True, axis='both', which='major', linewidth=0.8, alpha=.5)
        plot1.grid(visible=True, axis='both', which='minor', linestyle=':', linewidth=0.5, alpha=.5)
        plt.suptitle(f"{DriverInfo.fullname} - {SessionInfo.event_name}\n{y.name} Analysis")

        plt.savefig(f"{save_path}/{DriverInfo.fullname} {SessionInfo.event_name} {y.name} Plot.png", dpi=300)

        var_window.close()
        plt.show()

###############################################
# Make Window, Menubar, and Set Theme
###############################################

def make_window():
    sg.theme('DarkBlack')
    menu_def = [['&porpo', ['&About', '&Preferences', 'E&xit']]]
    right_click_menu_def = [[], ['Edit Me', 'Please!']]

# Define Layouts
    gp_layout = [
        [sg.Text('Select the year of Grand Prix:')],
        [sg.OptionMenu(Lists.years, default_value=f'{Lists.years[-1]}', k='-YEAR MENU-')],
        [sg.Button('Load GPs')],
        
        [sg.Text('Select Grand Prix:')],
        [sg.OptionMenu(Lists.gps, default_value=f'{Lists.gps[0]}', expand_x=True, k='-GP MENU-')],
        
        [sg.Text('Select Session:')],
        [sg.OptionMenu(Lists.sessions, default_value=Lists.sessions[0], k='-SES MENU-')],
        [sg.Button('Load Drivers')]]

    driver_layout = [
        [sg.Text('Select Driver:')],
        [sg.OptionMenu(Lists.drivers, k='-DRIVER MENU-')],
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

    frame_layout = [[sg.Image(source='src/common/images/icon_small.png', expand_x=True, expand_y=True, key='-LOGO-')]
        ]

    preferences_layout = [

    ]

    
    layout = [
        [sg.MenubarCustom(menu_def, key='-MENU-')],
        [sg.Frame('Home', frame_layout, expand_x=True, expand_y=True,)]
    ]
    
    layout += [[sg.TabGroup([[sg.Tab('Grand Prix', gp_layout, key='-GP TAB-', expand_x=True, expand_y=True),
                              sg.Tab('Drivers', driver_layout, key='-DRIVER TAB-', expand_x=True, expand_y=True),
                              sg.Tab('Laps', lap_layout, key='-LAPS TAB-', expand_x=True, expand_y=True),
                              sg.Tab('Variables', var_layout)]], key='-TAB GROUP-', expand_x=True, expand_y=True, enable_events=True),

                ]]

    window = sg.Window('porpo', layout, right_click_menu=right_click_menu_def,
                       right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0, 0),
                       use_custom_titlebar=True, finalize=True, keep_on_top=True, #scaling=2.0,
                       )

# Set Window Size
# Return
    window.set_min_size(window.size)
    return window

###############################################
# Define Main fuction
###############################################

def main():
    window = make_window()

    # Window Open, Begin Event Loop
    while True:
        event, values = window.read(timeout=100)
        
###############################################
# Define functions for button pushes
###############################################
        class ButtonFunc:
            # Load GP Button
            def load_gp():
                print(f"[LOG] Load Grand Prix for {values['-YEAR MENU-']}")
                Input.year = int(values['-YEAR MENU-'])
                Input.season = fastf1.get_event_schedule(Input.year)
                Input.gps = list(Input.season['EventName'])
                update_data = (Input.gps)
                window.Element('-GP MENU-').update(values=update_data)
                window.Element('-GP MENU-').default_value=(f'{Input.gps[0]}')
                window.refresh()

            def load_drivers():
                print(f"[LOG] Load Drivers for {values['-GP MENU-']}!")
                Input.year = int(values['-YEAR MENU-'])
                Input.grand_prix = str(values['-GP MENU-'])
                Input.ses = str(values['-SES MENU-'])
                Session()
                Lists.drivers = list(Session.results['Abbreviation'])
                update_data = (Lists.drivers)
                window.Element('-DRIVER MENU-').update(values=update_data)
                window.refresh
                window.find_element('-DRIVER MENU-').set_focus()

###############################################
# Begin 'If' Events for Button Pushes
###############################################

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
            ButtonFunc.load_gp()

        # Grand Prix Items
        # Load Drivers        
        elif event == 'Load Drivers':
            ButtonFunc.load_drivers()

    window.close()
    exit(0)

###############################################
# Check if exexcuted from Main
###############################################

if __name__ == '__main__':
    sg.theme('DarkRed')
    main()
else:
    sg.theme('DarkRed')
    main()
