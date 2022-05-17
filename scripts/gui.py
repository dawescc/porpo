"""
   Work in progress.

"""

# Imports
import PySimpleGUI as sg
import fastf1
from fastf1 import plotting
import matplotlib.pylab as plt
import os
import datetime

# Declare Cache and Export Paths
cache_path = '~/Documents/F1 Data Analysis/Cache/'
save_path = '~/Documents/F1 Data Analysis/Export/'

# Check if Cache directory Exists & Create if not
CacheExist = os.path.exists(cache_path)
if not CacheExist:
    os.makedirs(cache_path)

# Check if Cache directory Exists & Create if not
SaveExist = os.path.exists(save_path)
if not SaveExist:
    os.makedirs(save_path)

# Enable Cache with Cache Path
fastf1.Cache.enable_cache(cache_path)

####
# Begin Program
####

# Create Year Range for Year Picker
cur_year = datetime.datetime.today().year
year_list = range(2018,cur_year+1)

sg.theme('DarkRed')
main_layout = [
    [sg.OptionMenu(year_list, default_value=f'{cur_year}', expand_x=True)],
    [sg.Button('Load', expand_x=True, bind_return_key=True)]
]

window = sg.Window('F1 Data Analysis', main_layout, size=(200, 75), keep_on_top=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Load' or 'Return':
        class InputVars:
            year = int(values[0])


        class SeasonSchedule:
            season = fastf1.get_event_schedule(InputVars.year)
            gp_list = list(season['EventName'])
            gp_win_layout = [
                [sg.Text('Select Grand Prix:'), sg.OptionMenu(gp_list, default_value=gp_list[2])],
                [sg.Button('Load', bind_return_key=True, expand_x=True)]
            ]
            gp_window = sg.Window('Grand Prix Selection', gp_win_layout, keep_on_top=True)
            while True:
                gp_event, gp_values = gp_window.read()
                if gp_event == sg.WIN_CLOSED:
                    break
                if gp_event == 'Load' or 'Return':
                    grand_prix = gp_values[0]

                    ses_list = ['FP1', 'FP2', 'FP3', 'S', 'Q', 'R']
                    ses_win_layout = [[sg.Text(f'{grand_prix} Sessions:')],
                                        [sg.OptionMenu(ses_list, default_value=ses_list[0], size=15)],
                                        [sg.Button('Load', expand_x=True, bind_return_key=True)]]
                    ses_window = sg.Window('Session Selection', ses_win_layout, keep_on_top=True)

                    window.close()

                    while True:
                        ses_event, ses_values = ses_window.read()
                        if ses_event == sg.WIN_CLOSED:
                            break
                        if ses_event == 'Load' or 'Return':
                            gp_window.close()
                            ses_type = f'{ses_values[0]}'
                            ses_window.close()


        class SessionInfo:
            session = fastf1.get_session(InputVars.year, SeasonSchedule.grand_prix, SeasonSchedule.ses_type)

            class ProgBar:
                prog_win_layout = [[sg.Text('Loading Drivers and Session Data...')], [sg.ProgressBar(30, orientation='h', size=(20, 20), key='PROGRESSBAR',)]]
                prog_win = sg.Window('Loading Data', prog_win_layout, auto_close=True, finalize=True)
                progress_bar = prog_win['PROGRESSBAR']
                for i in range(15):
                    progress_bar.update(current_count=i + 1)
                pass

            session.load()
            for i in range(15, 31):
                ProgBar.progress_bar.update(current_count=i + 1)
                ProgBar.prog_win.close()

            results = session.results
            event_name = session.event['EventName']


        class PickDriver:
            session = SessionInfo.results
            driver_list = list(session['Abbreviation'])
            driver_win_layout = [
                [sg.Text('Select Driver:'), sg.OptionMenu(driver_list, default_value=driver_list[0], size=15)],
                [sg.Button('Load', bind_return_key=True, expand_x=True)]
            ]
            driver_window = sg.Window('Driver Selection', driver_win_layout, keep_on_top=True)
            while True:
                driver_event, driver_values = driver_window.read()
                if driver_event == sg.WIN_CLOSED:
                    break
                if driver_event == 'Load' or 'Return':
                    driver = (driver_values[0])
                    driver_window.close()


        class DriverInfo:
            info = SessionInfo.session.get_driver(PickDriver.driver)
            ses = SessionInfo.session.laps.pick_driver(PickDriver.driver)
            fullname = info['FullName']
            team = info['TeamName']
            team_color = fastf1.plotting.team_color(team)

            lap_or_ses_list = ['Lap', 'Full Session', 'Fastest Lap']
            lap_or_ses_win_layout = [[sg.Text('Evaluate the full session, or a lap?')], [sg.OptionMenu(lap_or_ses_list, default_value=lap_or_ses_list[0], size=15),
                                      sg.Button('Load', expand_x=True, bind_return_key=True)]]

            lap_or_ses_window = sg.Window('Lap Selection', lap_or_ses_win_layout, keep_on_top=True)
            while True:
                lap_or_ses_event, lap_or_ses_values = lap_or_ses_window.read()
                if lap_or_ses_event == sg.WIN_CLOSED:
                    break
                if lap_or_ses_event == 'Load' or 'Return':
                    lap_or_ses = f'{lap_or_ses_values[0]}'
                    if lap_or_ses == 'Lap':
                        lap_slider_layout = [[sg.Slider((ses['LapNumber'].min(), ses['LapNumber'].max()), orientation='h')], 
                                            [sg.Button('Select', bind_return_key=True, expand_x=True)]
                                            ]
                        lap_slider_win = sg.Window('Select Lap', lap_slider_layout, keep_on_top=True)
                        lap_slider_event, num = lap_slider_win.read()
                        if lap_slider_event == sg.WIN_CLOSED:
                            break
                        if lap_slider_event == 'Select' or 'Return':
                            pass
                        lap_n = ses[ses['LapNumber'] == num[0]]
                        lap_n_tel = lap_n.get_telemetry()
                        data = lap_n_tel
                        title = f'{fullname} {SessionInfo.event_name} Lap {num[0]} Data:'
                        def_xvalue = f'Distance'
                        lap_slider_win.close()

                    elif lap_or_ses == 'Fastest Lap':
                        f_lap = ses.pick_fastest()
                        fastest_lap = f_lap.get_telemetry()
                        data = fastest_lap
                        title = f'{fullname} {SessionInfo.event_name} Fastest Lap Data:'
                        def_xvalue = f'Distance'

                    else:
                        data = ses
                        title = f'{fullname} {SessionInfo.event_name} Full {SeasonSchedule.ses_type} Session Data:'
                        def_xvalue = f'LapNumber'

                    lap_or_ses_window.close()

        var_list = list(DriverInfo.data)
        var_win_layout = [
            [sg.Text(f'{DriverInfo.title}')],
            [sg.Text('Y Variable:'), sg.OptionMenu(var_list, default_value=var_list[0], expand_x=True)],
            [sg.Text('X Variable:'), sg.OptionMenu(var_list, default_value=DriverInfo.def_xvalue, expand_x=True)],
            [sg.Text('*Note it is not recomended to change the X Variable from "Distance" or "LapNumber"')],
            [sg.Button('Plot', bind_return_key=True, expand_x=True)]]

        var_window = sg.Window('Variable Selection', var_win_layout, keep_on_top=True)
        while True:
            var_event, var_values = var_window.read()
            if var_event == sg.WIN_CLOSED:
                break
            if var_event == 'Plot':
                driver_yvar = DriverInfo.data[f'{var_values[0]}']
                driver_xvar = DriverInfo.data[f'{var_values[1]}']

                plt.rcParams["figure.autolayout"] = True
                x = driver_xvar
                y = driver_yvar
                xmin, xmax = x.min(), x.max()

                fig = plt.figure(1)
                plot1 = fig.subplots()
                plot1.plot(x, y, color=DriverInfo.team_color, label=f"{y.name}")
                plot1.set_ylabel(f"{y.name}")
                plot1.set_xlabel(f"{x.name}")
                plot1.set_xlim(xmin, xmax)
                plot1.grid(visible=True, axis='y', alpha=.5)
                plt.suptitle(f"{DriverInfo.fullname} - {SessionInfo.event_name}\n{y.name} Analysis")

                plt.savefig(f"{save_path}/{DriverInfo.fullname} {SessionInfo.event_name} {y.name} Plot.png",
                            dpi=300, transparent=True)

                var_window.close()
                plt.show()

window.close()
del window
