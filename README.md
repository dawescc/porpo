<img align="left" width="50" height="50" src="src/common/images/construct.png">

&nbsp;
This repository is a work in progress. Anything and everything is subject to change.


# Porpo

<p align="center">
  <img src = src/common/images/icon.png />
</p>

<p align="center">
  <img src = https://img.shields.io/github/license/dtech-auto/F1DataAnalysis />
    </>
  <img src = https://img.shields.io/github/languages/top/dtech-auto/F1DataAnalysis />
    </>
  <img src = https://img.shields.io/github/v/release/dtech-auto/F1DataAnalysis?display_name=tag&include_prereleases />
    </>
</p>

<p align="center">
  <img src = https://img.shields.io/github/commit-activity/w/dtech-auto/F1DataAnalysis />
    </>
  <img src = https://img.shields.io/github/last-commit/dtech-auto/F1DataAnalysis />
    </>
  <img src = https://img.shields.io/github/issues-raw/dtech-auto/F1DataAnalysis />
</p>

------

## Table of Contents
- [Porpo](#porpo)
  - [Table of Contents](#table-of-contents)
  - [General Information](#general-information)
  - [Getting Started](#getting-started)
  - [Usage](#usage)
    - [Specific Lap](#specific-lap)
    - [Fastest Lap](#fastest-lap)
    - [Session](#session)

------

## General Information

Porpo is a python application that utilizes the [FastF1](https://github.com/theOehrly/Fast-F1) package to easily pull specific data and generate visualizations for analysis.

*Note*: [Python3](https://www.python.org/downloads/) (v.3.8 or greater) is required.

## Getting Started
Currently, there is not a *simple* way to run the program. However, getting it up and running is very easy, regardless of platform. 

Install Dependencies:

```
pip3 install fastf1
pip3 install PySimpleGUI
```

There are 2 methods of execution:

`/scripts/gui.py` to begin using the application with a GUI. (Recommended)

`/scripts/main.py` to begin using the application in CLI.

## Usage

Porpo allows you to individually set all the variables for evaluation. 

You start by selecting the year the Grand Prix took place.

<p align="center">
  <img width="40%" height="40%" src="/src/examples/images/screenshots/year_window.png"/>
</>

Then select the Grand Prix you want.

<p align="center">
  <img width="50%" height="50%" src="/src/examples/images/screenshots/gp_window.png"/>
</>

Then select the session from the Grand Prix.

*Note*: No GP has all sessions.

<p align="center">
  <img width="40%" height="40%" src="/src/examples/images/screenshots/sestype_window.png"/>
</>

Next, selext the driver you'd like to evaluate.

<p align="center">
  <img width="40%" height="40%" src="/src/examples/images/screenshots/driver_window.png"/>
</>

Now decide if you're goinng to evaluate the full session, or a specific lap, or easily select the fastest lap set by your chosen driver.

Check the [FastF1 documentation](https://theoehrly.github.io/Fast-F1/) to see everything that is available for each option.

<p align="center">
  <img width="40%" height="40%" src="/src/examples/images/screenshots/lap_window.png"/>
</>

The last step is to select which variables you want displayed on the axes (X and Y).

Be aware that although you can select any available data as either variable, some combinations may not perform as expected - or at all.

<p align="center">
  <img width="40%" height="40%" src="/src/examples/images/screenshots/var_window.png"/>
</>

The plot will show up in a new window, and automatically save to your export directory when the graph is closed. 
&nbsp;
&nbsp;

If you're unsure where your export directory is, the default is:
&nbsp;

  ```
  ~/Documents/F1 Data Analysis/Export/
  ```
&nbsp;

To change this directory, edit the path at `/scripts/gui.save_path`

### Specific Lap
You can easily pull and visualize data for a lap of an event's session.

![VER_SpeedL_Bah](/src/examples/images/ver_bah_last_speed.png)
<figcaption align = "center">
  <b>Max Verstappen speed on Lap 54 of the 2022 Bahrain GP. We can see he was losing power throughout the lap, up until the moment he completely lost power, and went into the pitlane.</b>
</figcaption>

### Fastest Lap
Alternatively, you can quickly do basic analysis of a fastest lap the selected driver set during an event's session.

![VER_SpeedF_Bah](/src/examples/images/ver_bah_fastest_speed.png)
<figcaption align = "center">
  <b>Max Verstappen speed on the fastest lap he set in 2022 Bahrain GP. We can the difference between this lap and lap 54, when he retired.</b>
</figcaption>

### Session
You can also quickly do an analysis of a driver's performance through an event's entire session.

![VER_SpeedF_Bah](/src/examples/images/ver_imola_laptime.png)
<figcaption align = "center">
  <b>Max Verstappen laptime over the course of the Imola GP. We can see as the track began to dry, laptimes began to fall very quickly.</b>
</figcaption>
