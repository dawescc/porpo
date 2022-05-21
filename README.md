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
  - [Exporting the Plot](#exporting-the-plot)
    - [Specific Lap](#specific-lap)
    - [Fastest Lap](#fastest-lap)
    - [Session](#session)

------

## General Information

Porpo is a python application that utilizes the [FastF1](https://github.com/theOehrly/Fast-F1) package to easily pull specific data and generate visualizations for analysis.

*Note*: [Python3](https://www.python.org/downloads/) (v.3.8 or greater) is required.

<p align="center">
  <img src = src/examples/images/screenshots/porpo.png />
</p>

## Getting Started
Currently, there is not a *simple* way to run the program. However, getting it up and running is very easy, regardless of platform. 

In a virtual enviornment, install dependencies:

```
pip3 install fastf1
pip3 install PySimpleGUI
```

There are 2 methods of execution:

`/scripts/gui.py` to begin using the application with a GUI. (Recommended)

`/scripts/main.py` to begin using the application in CLI. (*Depreciated*)

## Usage


**Porpo allows you to individually set all the variables for evaluation.** 

You start by selecting the year the Grand Prix took place.

Load the list of GPs for that season. Load the list again any time you want to evaluate a different season.

Select the Grand Prix you want, and select the session from the Grand Prix.

*Note*: Sprint not available for every Grand Prix.

Now load the list of drivers for your Grand Prix and session. Load the list again any time you want to evaluate a different Grand Prix.

Decide if you're going to evaluate the full session, or a specific lap, or easily select the fastest lap set by your chosen driver.

*Note:* Check the [FastF1 documentation](https://theoehrly.github.io/Fast-F1/) to see the data values available for each option.

The last step is to select which variables you want displayed on the axes (X and Y). Be aware that although you can select any available data as either variable, some combinations may not perform as expected - or at all.

Click 'Confirm All' to update selected values, and 'Analyse' to see your visualization.

## Exporting the Plot

The plot will show up in a new window, and automatically save to your export directory when the window is closed.

If you're unsure where your export directory is, the default relative path is:

  ```
  ~/Documents/F1 Data Analysis/Export/
  ```
&nbsp;

To change this directory, edit the export path in the preferences window. For now, if you want a different directory, you need to do this every time you open the app or it will reset to default.

### Specific Lap
You can easily pull and visualize data for a single lap of a session.

![VER_SpeedL_Bah](/src/examples/images/ver_bah_last_speed.png)
<figcaption align = "center">
  <b>Max Verstappen speed on Lap 54 of the 2022 Bahrain GP. We can see he was losing power throughout the lap, up until the moment he completely lost power, and went into the pitlane.</b>
</figcaption>

### Fastest Lap
By default, you can quickly do analysis of the fastest lap set by the selected driver during a session.

![VER_SpeedF_Bah](/src/examples/images/ver_bah_fastest_speed.png)
<figcaption align = "center">
  <b>Max Verstappen speed on the fastest lap he set in 2022 Bahrain GP. We can the difference between this lap and lap 54, when he retired.</b>
</figcaption>

### Session
You can also quickly do an analysis of a driver's performance through an entire session.

![VER_SpeedF_Bah](/src/examples/images/ver_imola_laptime.png)
<figcaption align = "center">
  <b>Max Verstappen laptime over the course of the Imola GP. We can see as the track began to dry, laptimes began to fall very quickly.</b>
</figcaption>
