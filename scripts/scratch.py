"""
   This app is still in development.

"""

import PySimpleGUI as sg
import fastf1
from fastf1 import plotting
import matplotlib.pylab as plt
import os

# Declare [Cache, Export] Paths
cache_path = '~/Documents/F1 Data Analysis/Cache/'
save_path = '~/Documents/F1 Data Analysis/Export/'

# Check if Cache directory Exists
# Create if not
CacheExist = os.path.exists(cache_path)
if not CacheExist:
    os.makedirs(cache_path)

# Check if Cache directory Exists
# Create if not
SaveExist = os.path.exists(save_path)
if not SaveExist:
    os.makedirs(save_path)

# Enable Cache
fastf1.Cache.enable_cache(cache_path)

####
####

sg.theme('DarkRed')
main_layout = [
    [sg.Text('Grand Prix Year:'), sg.Push(), sg.InputText(size=15, justification='right')],
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
                [sg.Button('Load', bind_return_key=True)]
            ]
            gp_window = sg.Window('Grand Prix Selection', gp_win_layout, keep_on_top=True)
            while True:
                gp_event, gp_values = gp_window.read()
                if gp_event == sg.WIN_CLOSED:
                    break
                if gp_event == 'Load' or 'Return':
                    grand_prix = gp_values[0]

                    ses_list = ['FP1', 'FP2', 'FP3', 'S', 'Q', 'R']
                    ses_win_layout = [[sg.OptionMenu(ses_list, default_value=ses_list[0], size=15),
                                       sg.Button('Load', expand_x=True, bind_return_key=True)]]
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
                prog_win_layout = [[sg.ProgressBar(30, orientation='h', size=(20, 20), key='PROGRESSBAR')]]
                prog_win = sg.Window('Loading Drivers', prog_win_layout, auto_close=True, finalize=True)
                progress_bar = prog_win['PROGRESSBAR']
                for i in range(15):
                    progress_bar.update(current_count=i + 1)
                pass

            session.load()
            for i in range(15, 31):
                ProgBar.progress_bar.update(current_count=i + 1)

            results = session.results
            event_name = session.event['EventName']


        class PickDriver:
            session = SessionInfo.results
            driver_list = list(session['Abbreviation'])
            driver_win_layout = [
                [sg.Text('Select Driver:'), sg.OptionMenu(driver_list, default_value=driver_list[0], size=15)],
                [sg.Button('Load', bind_return_key=True)]
            ]
            driver_window = sg.Window('Grand Prix Selection', driver_win_layout, keep_on_top=True)
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

            lap_or_ses_list = ['Lap', 'Full Session', 'Fastest']
            lap_or_ses_win_layout = [[sg.OptionMenu(lap_or_ses_list, default_value=lap_or_ses_list[0], size=15),
                                      sg.Button('Load', expand_x=True, bind_return_key=True)]]

            lap_or_ses_window = sg.Window('Session Selection', lap_or_ses_win_layout, keep_on_top=True)
            while True:
                lap_or_ses_event, lap_or_ses_values = lap_or_ses_window.read()
                if lap_or_ses_event == sg.WIN_CLOSED:
                    break
                if lap_or_ses_event == 'Load' or 'Return':
                    lap_or_ses = f'{lap_or_ses_values[0]}'
                    lap_or_ses_window.close()
                    if lap_or_ses == 'Lap':
                        num = int(sg.popup_get_text('Input Lap Number (10, 20, 30, etc.):'))
                        lap_n = ses[ses['LapNumber'] == num]
                        lap_n_tel = lap_n.get_telemetry()
                        data = lap_n_tel

                    elif lap_or_ses == 'Fastest':
                        f_lap = ses.pick_fastest()
                        fastest_lap = f_lap.get_telemetry()
                        data = fastest_lap

                    else:
                        data = ses


        var_list = list(DriverInfo.data)
        var_win_layout = [
            [sg.Text('Y Variable:'), sg.OptionMenu(var_list, default_value=var_list[0])],
            [sg.Text('X Variable:'), sg.OptionMenu(var_list, default_value=var_list[12])],
            [sg.Button('Plot')]
        ]
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
