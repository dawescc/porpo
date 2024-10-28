> [!IMPORTANT]  
> Some dependencies have transitioned to a payment model. Software may not work as expected.

> [!NOTE]
> Because some critical dependencies now require payment, this repository has been archived. Thank you for your support!
-----

# Porpo

The 2024 Formula 1 season is live! Download Porpo and take a look at just how well your most (or least) favorite driver / team did on track!

### Issues?

Submit an issue, with a screenshot of the error, and I will get to work.

### Want to contribute?

Contributions are welcome! Be sure to use proper documentation when submitting a PR.

## Table of Contents
- [Porpo](#porpo)
  - [Table of Contents](#table-of-contents)
    - [General Information](#general-information)
    - [Meet porpo, a data collection and visualization tool.](#meet-porpo-a-data-collection-and-visualization-tool)
    - [Getting Started](#getting-started)
  - [Usage](#usage)
  - [Exporting the Plot](#exporting-the-plot)
    - [Specific Lap](#specific-lap)
    - [Fastest Lap](#fastest-lap)
    - [Session](#session)

------

### General Information

### Meet [porpo](https://github.com/dtech-auto/porpo), a data collection and visualization tool.

<p align="center">
  <img src = src/common/images/icon.png />
</p>

------

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

</br>
Porpo is an application that is designed to easily pull telemetry data and create beautiful visualizations for analysis. It allows you to look through historic and current race data, make comparisons across specific laps, fastest laps, or full sessions. Soon, it will let you visualize the track as a map, allowing you to more clearly see where on track an event took place.
</br>
</br>
<i>Note</i>: Python3 is required.
</br>
</br>

**What does porpo mean?**

'porpo' is a shortened form of the word 'porpoise'. An it sounds cool to say over and over again. 
</br>

### Getting Started

After you do that, download the [porpo](https://github.com/dtech-auto/porpo/releases/tag/) source code `.zip`. Extract the contents wherever you want, but keep in mind that is your working directory, so something like `/Documents` would be better than your Desktop.

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
