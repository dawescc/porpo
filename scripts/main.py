import fastf1
from fastf1 import plotting
import matplotlib.pylab as plt
# import numpy as np
# import pandas as pd

# Enable Cache
fastf1.Cache.enable_cache('./data/cache')


class InputVars:
    grand_prix = input(f'Which Grand Prix do you want to evaluate?  ("Imola", "Italy", etc.): \n')
    year = int(input(f'What year did the Grand Prix take place? ("2022", "2021", etc.): \n'))
    ses = input(f'What is the session type? ("R","Sprint", "FP1", etc.): \n')
    driver = input(f'Which driver do you want to evaluate? (ex. Abbreviation or Number): \n')


class SessionInfo:
    session = fastf1.get_session(InputVars.year, InputVars.grand_prix, InputVars.ses)
    session.load()
    results = session.results
    event_name = session.event['EventName']


class DriverInfo:
    info = SessionInfo.session.get_driver(InputVars.driver)
    ses = SessionInfo.session.laps.pick_driver(InputVars.driver)
    fullname = info['FullName']
    team = info['TeamName']
    team_color = fastf1.plotting.team_color(team)
    print(f'Getting data for {fullname}...\n')

    lap_or_ses = input(f'Do you want to evaluate a specific lap? (Y/N/F for Fastest): \n')
    if lap_or_ses == 'Y':
        num = int(input(f'\nInput Lap Number (10, 20, 30, etc.): \n'))
        lap_n = ses[ses['LapNumber'] == num]
        lap_n_tel = lap_n.get_telemetry()
        data = lap_n_tel
        print(f"Getting lap {num} data...\n")

    elif lap_or_ses == 'F':
        f_lap = ses.pick_fastest()
        fastest_lap = f_lap.get_telemetry()
        data = fastest_lap
        print(f"Getting fastest lap data...\n")

    else:
        data = ses
        print(f"Getting full session data...\n")


def define_data():
    var_list = list(DriverInfo.data)
    for number, var in enumerate(var_list):
        print(number, var)
    y = int(input(f'\nSelect Y AXIS data point to evaluate from list above (Int): \n'))
    req_dat_y = var_list[y]
    x = int(input(f'\nSelect X AXIS data point to evaluate from list above (Int): \n'))
    req_dat_x = var_list[x]
    return req_dat_y, req_dat_x


def data():
    req_dat_y, req_dat_x = define_data()
    driver_xvar = DriverInfo.data[f'{req_dat_x}']
    driver_yvar = DriverInfo.data[f'{req_dat_y}']
    return driver_xvar, driver_yvar


def data_plot():
    plt.rcParams["figure.autolayout"] = True

    driver_xvar, driver_yvar = data()
    x = driver_xvar
    y = driver_yvar
    xmin, xmax = x.min(), x.max()

    fig = plt.figure(1)
    speed = fig.subplots()
    speed.plot(x, y, color=DriverInfo.team_color, label=f"{y.name}")
    speed.set_ylabel(f"{y.name}")
    speed.set_xlabel(f"{x.name}")
    speed.set_xlim(xmin, xmax)
    speed.grid(visible=True, axis='y', alpha=.5)
    plt.suptitle(f"{DriverInfo.fullname} - {SessionInfo.event_name}\n{y.name} Analysis")

    plt.savefig(f".data/export/{DriverInfo.fullname} {SessionInfo.event_name} {y.name} Plot.png", dpi=300, transparent=True)

    plt.show()
    print("\nPlot Saved in './data/export/...'\n")
    return fig

def save():
    s = input(f'Do you want to save telemetry data? (Y/N): \n')
    if s == 'Y':
        export = DriverInfo.data
        export.to_csv(fr".data/export/{DriverInfo.fullname} {SessionInfo.event_name} Data.csv")
        print("Data Saved.\n")
    if s == 'N':
        print("Nothing saved.\n")
        pass


def main():
    i = 'Y'
    while i == 'Y':
        data_plot()
        save()
        i = input(f'Do you want to go again? (Y/N): \n')
    else:
        print("All good, thanks!")


main()
