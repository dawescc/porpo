import datetime
import os
import webbrowser

import fastf1
import matplotlib.pylab as plt
import PySimpleGUI as sg
from fastf1 import plotting

###############################################
# Define Classes
###############################################

class CacheDir:
    def __init__(self, path):
        path = 'path'

    def Set(path):
        CacheExist = os.path.exists(path)
        if not CacheExist:
            os.makedirs(path)
        cache_path = path

class ExportDir:
    def __init__(self, path):
        path = 'path'

    def Set(path):
        ExportExist = os.path.exists(path)
        if not ExportExist:
            os.makedirs(path)
        save_path = path


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
    sg.theme('DarkRed')
    menu_def = [[('&porpo'), ['&About', '&Preferences', '&GitHub', 'E&xit']]]

# Define Layouts
    gp_layout = [
        [sg.Text('Select the year of Grand Prix:')],
        [sg.OptionMenu(Lists.years, default_value=f'{Lists.years[-1]}', k='-YEAR MENU-')],
        [sg.Button('Load GPs')],

        [sg.Text('Select Session:')],
        [sg.OptionMenu(Lists.sessions, default_value=Lists.sessions[0], k='-SES MENU-')],
        [sg.Button('Load Drivers')],

        [sg.Text('Select Grand Prix:')],
        [sg.Listbox(Lists.gps, expand_x=True, horizontal_scroll=False, size=(None, 7), enable_events=True, k='-GP MENU-'),]]
        

    driver_layout = [
        [sg.Text('Select Driver:')],
        [sg.Listbox(Lists.drivers, expand_x=True, horizontal_scroll=False, size=(None, 7), enable_events=True, k='-DRIVER MENU-')],
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
        [sg.Menubar(menu_def, key='-MENU-')],
        [sg.Frame('',frame_layout, expand_x=True, expand_y=True,)]
    ]
    
    layout += [[sg.TabGroup([[sg.Tab('Grand Prix', gp_layout, key='-GP TAB-', expand_x=True, expand_y=True),
                              sg.Tab('Drivers', driver_layout, key='-DRIVER TAB-', expand_x=True, expand_y=True),
                              sg.Tab('Laps', lap_layout, key='-LAPS TAB-', expand_x=True, expand_y=True),
                              sg.Tab('Variables', var_layout)]], key='-TAB GROUP-', expand_x=True, expand_y=True),

                ]]

    window = sg.Window('porpo', layout, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0, 0),
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

            #About
            def about():
                about_layout = [[sg.Text('porpo is not affiliated with Formula 1 or the FIA')],
                                [sg.Text('License MIT - Free to Distribute', justification='center')],]
                about_win = sg.Window('About porpo', about_layout, size=(200,50), modal=True, keep_on_top=True, disable_close=False)
                event = about_win.read()
                if event == sg.WIN_CLOSED:
                    about_win.close()

            #Preferences
            def preferences():
                pref_layout = [[[sg.Text('Select Your Cache Folder for Session')], [sg.FolderBrowse('Set Cache', enable_events=True, key='-CACHE-')]],
                                [[sg.Text('Select Your Export Folder for Session')], [sg.FolderBrowse('Set Export', enable_events=True, key='-EXPORT-')]],
                                [[sg.Push()], [sg.OK('OK')]],]
                pref_win = sg.Window('porpo Preferences', pref_layout, modal=True, keep_on_top=True, disable_close=True, force_toplevel=True)
                event, values = pref_win.read()
                while True:
                    if event == 'OK' or sg.WIN_CLOSED:
                        pref_win.close(); del pref_win

                    elif event == 'Set Cache':
                        CacheDir.Set({values['-CACHE-']})
                        print(f"Set CACHE to {values['-CACHE-']}")

                    elif event == 'Set Export':
                        ExportDir.Set({values['-CACHE-']})
                        print(f"Set CACHE to {values['-EXPORT-']}")

            #GitHub
            def GitHub():
                webbrowser.open('https://github.com/dtech-auto/porpo/', new=2)
                print(f"[LOG] Load Grand Prix for {values['-YEAR-']}")

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
            ButtonFunc.about()

        # Menu Items
        # Preferences
        elif event == 'Preferences':
            print("[LOG] Clicked Preferences")
            ButtonFunc.preferences()

        # Menu Items
        # GitHub
        elif event == 'GitHub':
            print("[LOG] Clicked Preferences")
            ButtonFunc.GitHub()

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
