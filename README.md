# SpaceCryptoPythonBot
This repository contains a Python script which can be used to automatize the NFT game Space Crypto.

# Table of Contents
1. [License](#License)
2. [Donate](#Donate)
3. [Features example](#Features-example)
4. [Requirements](#Requirements)
5. [How to use](#How-to-use)
6. [Tips](#Tips)
7. [Upcoming features](#Upcoming-features)
8. [Frequent asked questions (FAQ)](#Frequent-asked-questions-(FAQ))
9. [Support-and-feature-requests](#Support-and-feature-requests)

# License
The script is open source and available to the community for free under the GNU General Public License v3.0.

# Donate
If you feel like, donations are always a nice way to support the developers and keep them motivated to implement new features and fix bugs.
Donations can be done to the following wallet:

- Address: 0xcE5B54c07F7609f6eaD1C5306d07EbFf3349Fc31
- Cryptos: $BNB (BNB), $DOGE (Dogecoin) 
- Chain: BNB - BNB Smart Chain (BEP20)

Thank you!

# Features
- Multi-account. No limit on number of accounts! Just open as many browsers as you want!
- Configurable minimum number of ships to start the battle. -- Default: 10 ships
- Configurable surrender on levels: 6, 11, and 16. -- Default: Level 11
- Configurable reload ships every X minutes. -- Default: 4 minutes
- Configurable refresh browser every X minutes. -- Default: 30 minutes
- Configurable log file

# Requirements

## Python version requirement:
The following version is required:
- Python 3

Official Python website: https://www.python.org/downloads/

#### Checking Python version using the command prompt (Win+R -> cmd)
> py --version

### Packages
The following packages are required:
- pyautogui
- pygetwindow
- pillow
- opencv-python

#### Installing packages using the command prompt (Win+R -> cmd)
> py -m pip install --upgrade pip setuptools wheel<br>
> py -m pip install pyautogui<br>
> py -m pip install pygetwindow<br>
> py -m pip install pillow<br>
> py -m pip install opencv-python

In case you don't know how to install packages, please refer to the following guide: https://packaging.python.org/en/latest/tutorials/installing-packages/


# How to use
- 1st: Download or clone this repository
- 2nd: Open all browsers and do the metamask login
- 3rd: Open the Space Crypto game website. It is not necessary to connect, the script will connect automatically
- 4th: Open a command prompt (Win+R -> cmd) and navigate to the folder where the script is downloaded
- 5th: Run the command:
> py spaceCryptoBotPersike.py

## Changing user configurable parameters
The user configurable paramters can be found on lines 20 to 24 of the spaceCryptoBot.py file.
To configure it, just change the number according to your wishes.

>minShipsToStart:            int = 10    # [1 to 15]     Define the minimum amount of ships to start the fight <br>
>surrenderOnLevel:           int = 11    # [6,11,16]     Define the level which the script will surrender and start from level 1 again <br>
>reloadShipsEveryMinutes:    int = 4     # [any value]   Reload ships every X minutes <br>
>refreshBrowserEveryMinutes: int = 30    # [any value]   Refresh the screen every X minutes, this prevents the script to get stuck because of browser issues <br>
>saveLogFile:                bool = True # [True/False]  Save log file (useful in case debug is required)


# Tips
- The script is based on a 1000x800 window, thefore the resolution of the screen must be higher than that
- Set the Windows and browsers zoom to 100%
- Tested on the following browsers: Firefox, Brave, and Chrome
- Remove the console from the front of the browsers

# Upcoming features
- Configurable surrender level

# Note in case of multiple acounts
The script will cycle through all the browsers which has the Space Crypto open and run the routine on each of them.
In case there are too many browsers opened, the script may not behave addequately. Possible consequences:
- Does not surrender on desired level
- Reload ships will happen too late and you will be defeated

# Frequent asked questions (FAQ)
<br>
- Does it work for multi account?
<br>
- Yes. It will run through every browser which has the Space Crypto opened.
<br>
<br>
- Are random clicks implemented?
<br>
- No. Space Crypto allows bots or scripts, therefore random clicks are not required.
<br>

# Support and feature requests
Please use the "issues" feature from GitHub in order to report bugs and get support from the script creator.

# Change log
V1.0 - Initial release.
V1.1 - Cooldown time in case not enough ships are available.