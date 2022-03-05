# Author: https://github.com/LeoPersike
# Script: Space Crypto Multi Account Python Bot
# How to use: https://github.com/LeoPersike/SpaceCryptoPythonBot
# Repository: https://github.com/LeoPersike/SpaceCryptoPythonBot
# Support: https://github.com/LeoPersike/SpaceCryptoPythonBot/issues
# License: GNU General Public License v3.0
# License type: Open Source
    
# Import
import os
import pygetwindow
import pyautogui
import time
import datetime
import dataclasses
import logging
from PIL import ImageGrab

##########################
### USER CONFIGURATION ###
##########################
class userConfiguration:
    minShipsToStart:            int = 10    # Define the minimum amount of ships to start the fight
    surrenderOnLevel:           int = 11    # Define the level which the script will surrender and start from level 1 again
    reloadShipsEveryMinutes:    int = 4     # Reload ships every X minutes
    refreshBrowserEveryMinutes: int = 30    # Refresh the screen every X minutes, this prevents the script to get stuck because of browser issues
    saveLogFile:                bool = True # [True/False] - Save log file (useful in case debug is required)
# Creating instance
userConfigurations = userConfiguration()

################
### DONATION ###
################
# This script is open source and available to the community for free!
# In any case, if the script is useful for you and you would like to contribute
# the following crypto addresses can be used:
# $DOGE [BSC]: 0xcE5B54c07F7609f6eaD1C5306d07EbFf3349Fc31
# $BNB  [BSC]: 0xcE5B54c07F7609f6eaD1C5306d07EbFf3349Fc31    
# Donations are always a nice way to support the developers!

#######################################################################
### WARNING! WARNING! WARNING! WARNING! WARNING! WARNING! WARNING!  ###
### Changing the lines below will affect the behavior of the script ###
#######################################################################

# Version
VERSION = "1.0"

# Debug levels
class debugLevel: # This configuration changes what is printed on the console
    critical:   bool = False     # A serious error, indicating that the program itself may be unable to continue running.
    error:      bool = False     # Due to a more serious problem, the software has not been able to perform some function.
    warning:    bool = False     # An indication that something unexpected happened, or indicative of some problem in the near future
    info:       bool = True     # Confirmation that things are working as expected.
    debug:      bool = False    # Detailed information, typically of interest only when diagnosing problems.   
# Creating instance
debugLevels = debugLevel()

# Global parameters
class globalParameter:
   amountOfBrowsers:        int = 0 # can also be seen as number of accounts
   maximumNumberOfScrolls:  int = 10
# Creating instance
globalParameters = globalParameter()

# Configuration flags
class stateMachineFlag:
    prepareBrowsers:    bool = True
    connect:            bool = True
    loadShips:          bool = True
    fightBoss:          bool = False
    pressConfirm:       bool = True
    reloadShips:        bool = True
    checkError:         bool = True
    surrender:          bool = True
    refreshBrowser:     bool = True     
# Creating instance
stateMachineFlags = stateMachineFlag()

# Timing parameters
class timingParameter:
    lastReloadShipsTime:    float = 0.0
    lastRefreshBrowserTime: float = 0.0
# Creating instance
timingParameters = timingParameter()

# Sleep intervals
class sleepInterval:
    shortSleep:     int = 1
    mediumSleep:    int = 2
    longSleep:      int = 7        
# Creating instance
sleepIntervals = sleepInterval()

# Confidence of image search
class confidenceValue:
    low:    float = 0.65
    medium: float = 0.80
    high:   float = 0.95
    ultra:  float = 0.99
# Creating instance    
confidenceValues = confidenceValue()

#################
### FUNCTIONS ###
#################

# debugHandler(type,message)
# This function will handle the console output and also create a log file if required
def debugHandler(*arguments):
    # Forcing python to use global values
    global debugLevels
        
    # Get timestamp   
    #t = time.localtime()
    #current_time = time.strftime("%H:%M:%S", t)
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Get arguments
    items = []
    for element in arguments:
        items.append(element)  

    # Console log
    try:    
        message = items[0] + ": " + items[1]
        # Debugging on console
        if items[0] == "CRITICAL" and debugLevels.critical == True:
            print(current_time,":",message)   
        elif items[0] == "ERROR" and debugLevels.error == True:
            print(current_time,":",message) 
        elif items[0] == "WARNING" and debugLevels.warning == True:
            print(current_time,":",message)  
        elif items[0] == "INFO" and debugLevels.info == True:
            print(current_time,":",message) 
        elif items[0] == "DEBUG" and debugLevels.debug == True:
            print(current_time,":",message) 

    except:
        pass
    
    # File Log
    if userConfiguration.saveLogFile == True:
        try:    
            message = items[1]
            # Debugging on console
            if items[0] == "CRITICAL":
                logging.critical(message)
            elif items[0] == "ERROR":
                logging.error(message)
            elif items[0] == "WARNING":
                logging.warning(message)
            elif items[0] == "INFO":
                logging.info(message)
            elif items[0] == "DEBUG":
                logging.debug(message)
    
        except:
            pass 
            
# prepareBrowsers()
# This function moves and resizes every Space Crypto window opened
def preparingBrowsers():
    # Debug info
    debugHandler("INFO","Function call: prepareBrowsers()")
    
    # Forcing python to use global values
    global userConfigurations
    global globalParameters
    global timingParameters
    global sleepIntervals
    global stateMachineFlags
    global confidenceValues

    globalParameters.amountOfBrowsers = 0 

    try:    
        while True:
            browser = pygetwindow.getWindowsWithTitle('Space Crypto')[globalParameters.amountOfBrowsers]
            globalParameters.amountOfBrowsers += 1
            browser.moveTo(100,50)
            browser.resizeTo(1000, 800)
            time.sleep(sleepIntervals.mediumSleep)
            
    except:
        if globalParameters.amountOfBrowsers == 0:
            debugHandler("WARNING","No browser was found.")    
        else:
            debugHandler("INFO","Total number of browsers found: " + str(globalParameters.amountOfBrowsers))


# runThroughBrowsersAndPlay()                      
# This function go through all Firefox browsers and call playGame()
def runThroughBrowsersAndPlay():
    # Debug info
    debugHandler("INFO","Function call: runThroughBrowserAndPlay()")
    
    # Forcing python to use global values
    global userConfigurations
    global globalParameters
    global timingParameters
    global sleepIntervals
    global stateMachineFlags
    global confidenceValues

    # Prepare browsers
    if stateMachineFlags.prepareBrowsers == True:
        preparingBrowsers()
   
    # Run the script
    try:
        for selectedBrowser in range(0,globalParameters.amountOfBrowsers):    
            browser = pygetwindow.getWindowsWithTitle('Space Crypto')[selectedBrowser]
            browser.moveTo(100,50) # Bring it to front
            debugHandler("INFO","Starting routine on browser: " + str(selectedBrowser+1))
            playGameStateMachine()
            debugHandler("INFO","Finished routine routine on browser: " + str(selectedBrowser+1))

            time.sleep(sleepIntervals.mediumSleep)
            
    except:
        print("WARNING","runThroughBrowserAndPlay(): Error switching browsers. Was one of them closed?")          

           
# playGameStateMachine()
# This function will detect the buttons and play the game based on a defined routine 
def playGameStateMachine():
    # Debug info
    debugHandler("INFO","Function call: playGameStateMachine()")
    
    # Forcing python to use global values
    global userConfigurations
    global globalParameters
    global timingParameters
    global sleepIntervals
    global stateMachineFlags
    global confidenceValues

    # State machine 
    if stateMachineFlags.connect == True:
        connectingToGame()
                       
    if stateMachineFlags.loadShips == True:
        loadingShips()
                    
    if stateMachineFlags.fightBoss == True:
        fightingBoss()
        
    if stateMachineFlags.reloadShips == True:
        reloadingShips()
                       
    if stateMachineFlags.surrender == True:
        surrenderingOnDesiredLevel()
        
    if stateMachineFlags.pressConfirm == True:
        pressingConfirm()
            
    if stateMachineFlags.checkError == True:
        checkingError()
        
        
# connectingToGame()
# This function will click on connect, sign the metamask, play, and order by max ammo
def connectingToGame():
    # Debug
    debugHandler("INFO","Function call: connectToGame()")
    
    # Forcing python to use global values
    global userConfigurations
    global globalParameters
    global timingParameters
    global sleepIntervals
    global stateMachineFlags
    global confidenceValues
       
    try:
        # Check interval time to refresh the browser
        interval = time.time() - timingParameters.lastRefreshBrowserTime
        if (interval > userConfigurations.refreshBrowserEveryMinutes*60) and stateMachineFlags.refreshBrowser == True:
            pyautogui.press('f5')
            timingParameters.lastRefreshBrowserTime = time.time()
            time.sleep(2*sleepIntervals.longSleep) # Waiting X seconds to load the screen

            # Clear console
            if os.name in ('nt', 'dos'):
                os.system('cls')
            else:
                os.system('clear')

        else:
            debugHandler("INFO","Actual refresh browser interval is: " + str(int(interval)) + "s")
        
        try:
            buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/loginConnectWallet.png',confidence=confidenceValues.high)
            pyautogui.moveTo(buttonX, buttonY)
            pyautogui.click()
            time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen
        except:
            pass
        
        try:
            buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/loginSignMeta.png',confidence=confidenceValues.high)
            pyautogui.moveTo(buttonX, buttonY)
            pyautogui.click()
            time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen
        except:
            pass

        try:        
            buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/loginPlay.png',confidence=confidenceValues.high)
            pyautogui.moveTo(buttonX, buttonY)
            pyautogui.click()
            time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen
            orderingByMaxAmmo()
        except:
            pass       

    except:
        debugHandler("WARNING","connectToGame(): Connect failed. Already connected?")
        time.sleep(sleepIntervals.shortSleep) # Waiting X seconds to update the screen

     
# orderingByMaxAmmo()
# This function will order the ships by max ammo
def orderingByMaxAmmo():
    # Debug
    debugHandler("INFO","Function call: orderByMaxAmmo()")
    
    # Forcing python to use global values
    global userConfigurations
    global globalParameters
    global timingParameters
    global sleepIntervals
    global stateMachineFlags
    global confidenceValues
    
    try:
        # Go to Spaceship selection screen
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/orderNewest.png',confidence=confidenceValues.high)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        time.sleep(sleepIntervals.mediumSleep) # Waiting X seconds to update the screen
        
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/orderMaxAmmo.png',confidence=confidenceValues.high)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        time.sleep(sleepIntervals.mediumSleep) # Waiting X seconds to update the screen
        
    except:
        debugHandler("WARNING","orderByMaxAmmo(): Failed to order by Max Ammo. Already selected?")
        time.sleep(sleepIntervals.shortSleep) # Waiting X seconds to update the screen
        
        
# loadingShips()
# This function will load the ships and check if minimum is availble to start the battle        
def loadingShips():
    # Debug
    debugHandler("INFO","Function call: loadShips()")
    
    # Forcing python to use global values
    global userConfigurations
    global globalParameters
    global timingParameters
    global sleepIntervals
    global stateMachineFlags
    global confidenceValues
      
    try:
        # unloadingShips before trying to get them        
        unloadingShips()

        # Go to base selection screen and back to spaceship (to order the ships and remove button bug from game design)
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/menuBase.png',confidence=confidenceValues.high)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen

        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/menuSpaceship.png',confidence=confidenceValues.high)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen        

        # Control variables
        shipsReady = 0
        scrollsLeft = globalParameters.maximumNumberOfScrolls
       
        while (shipsReady < 15) and (scrollsLeft > 0):
            try: # Load the ships
            
                if False: # Single searching, buggy because of game design and browser effects
                    buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/shipAdd.png',confidence=confidenceValues.high)
                    pyautogui.moveTo(buttonX, buttonY)
                    pyautogui.click()
                    shipsReady += 1
                    time.sleep(sleepIntervals.shortSleep) # Waiting X seconds to update the screen
                    
                else: # Multiple searching: workaround 
                    buttons = pyautogui.locateAllOnScreen('./assets/shipAdd.png',confidence=confidenceValues.medium)
                    listOfButtons = list(buttons)
                    amountOfButtonsFound = len(listOfButtons)

                    if amountOfButtonsFound > 0:
                        lastShipsReady = shipsReady
                        try:
                            for index in range(0,amountOfButtonsFound-1):
                                if shipsReady == 15:
                                    break
                                
                                cordX = listOfButtons[index].left
                                cordY = listOfButtons[index].top
                                pixelRGB = ImageGrab.grab().getpixel((cordX, cordY))
                                
                                if pixelRGB[0] > 100 and pixelRGB[1] < 30 and pixelRGB[2] < 40: # Workaround to find red button
                                    centerX = cordX + listOfButtons[index].width / 2
                                    centerY = cordY + listOfButtons[index].height / 2
                                    pyautogui.moveTo(centerX, centerY)
                                    pyautogui.click()
                                    shipsReady += 1
                                    time.sleep(sleepIntervals.shortSleep) # Waiting X seconds to update the screenn   
                        except: 
                            pass
                        
                        if shipsReady == lastShipsReady:
                            raise Exception("No ships found. Scrolling.")
                        
            except: # No fight was found, scrolling
                try:
                    scrollsLeft -= 1
                    buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/iconCoin.png',confidence=confidenceValues.high)
                    pyautogui.moveTo(buttonX-100, buttonY+150)
                    time.sleep(sleepIntervals.shortSleep)
                    pyautogui.dragTo(buttonX-100, buttonY-50, 1.2, button='left')                 
                    pyautogui.moveTo(buttonX-100, buttonY+150)
                    pyautogui.click()
                    time.sleep(sleepIntervals.shortSleep)# Waiting X seconds to update the screen
                except: 
                    debugHandler("ERROR","loadShips(): Failed to scroll.")
    
        # Finished loading rountine. Checking...
        if shipsReady < userConfigurations.minShipsToStart:
            debugHandler("INFO","loadShips(): Not enough Spaceships, removing them to re-charge.")
            stateMachineFlags.fightBoss = False
            unloadingShips()
        else:
            debugHandler("INFO","Fighting enabled. Ships ready to battle: " + str(shipsReady))
            stateMachineFlags.fightBoss = True
      
    except:
        debugHandler("WARNING","Exception on loadShips(): Can't load the Spaceships. Already in battle?")        
        pass
      
      
# unloadingShips()
# This function will unload all ships already in battle
def unloadingShips():
    # Debug
    debugHandler("INFO","Function call: unloadShips()")
    
    # Forcing python to use global values
    global userConfigurations
    global globalParameters
    global timingParameters
    global sleepIntervals
    global stateMachineFlags
    global confidenceValues 
   
    try:
        while True:
            buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/shipRemove.png',confidence=confidenceValues.high)
            pyautogui.moveTo(buttonX, buttonY)
            pyautogui.click()
            time.sleep(sleepIntervals.shortSleep) # Waiting X seconds to update the screen
    except: 
        debugHandler("WARNING","unloadShips(): No more spaceships to unload. Were all spaceships unloaded?")
        time.sleep(sleepIntervals.mediumSleep) # Waiting X seconds to update the screen
        pass


# fightingBoss()
# This function will begin the fight
def fightingBoss():
    # Debug
    debugHandler("INFO","Function call: fightBoss()")
    
    # Forcing python to use global values
    global userConfigurations
    global globalParameters
    global timingParameters
    global sleepIntervals
    global stateMachineFlags
    global confidenceValues 

    try:
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/fightBoss.png',confidence=confidenceValues.high)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen
        stateMachineFlags.fightBoss = False
        
        try:
            buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/confirmDefeat.png',confidence=confidenceValues.high)
            pyautogui.moveTo(buttonX, buttonY)
            pyautogui.click()
        except:
            pass
            
        time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen              
        
    except:
        debugHandler("WARNING","fightBoss(): Fight boss button not found. Already fighting?")
        pass
        
       
# realoadingShips()
# This function will reload the ships if time window is exceeded and levels are 4 or 9
def reloadingShips():
    # Debug
    debugHandler("INFO","Function call: reloadingShips()")
    
    # Forcing python to use global values
    global userConfigurations
    global globalParameters
    global timingParameters
    global sleepIntervals
    global stateMachineFlags
    global confidenceValues
    
    # Check interval time to reload ships
    interval = time.time() - timingParameters.lastReloadShipsTime
    if interval > userConfigurations.reloadShipsEveryMinutes*60:
        try:
            debugHandler("INFO","Spaceships will be reloaded.")
            buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/returnToSpaceship.png',confidence=confidenceValues.high)
            pyautogui.moveTo(buttonX, buttonY)
            pyautogui.click()
            timingParameters.lastReloadShipsTime = time.time()
            time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen   
            stateMachineFlags.fightBoss = False
        except: 
            pass         
    else:
        debugHandler("INFO","Actual reload ships interval is: " + str(int(interval)) + "s")
      
          
# surrenderingOnDesiredLevel()
# This function will surrender on the desired level, only available on level 11 now
def surrenderingOnDesiredLevel():
    # Debug
    debugHandler("INFO","Function call: surrenderOnLevel()")

    # Forcing python to use global values
    global userConfigurations
    global globalParameters
    global timingParameters
    global sleepIntervals
    global stateMachineFlags
    global confidenceValues
    
    try: # only surrendering on level 11 so far
        if userConfigurations.surrenderOnLevel == 6:
            buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/boss6.png',confidence=confidenceValues.high)
        elif userConfigurations.surrenderOnLevel == 11:
            buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/boss11.png',confidence=confidenceValues.high)
        elif userConfigurations.surrenderOnLevel == 16:
            buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/boss16.png',confidence=confidenceValues.high)
        else:
            debugHandler("WARNING","surrenderOnLevel(): Selected surrender-level is not available") 
        
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/surrender.png',confidence=confidenceValues.high)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        time.sleep(sleepIntervals.mediumSleep) # Waiting X seconds to update the screen  
        
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/confirmSurrender.png',confidence=confidenceValues.high)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen   
        
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/returnToSpaceship.png',confidence=confidenceValues.high)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen   
        
        stateMachineFlags.fightBoss = False
    except:
        debugHandler("INFO","surrenderOnLevel(): Surrender level not yet reached.") 
        
        
# pressingConfirm()
# This function will press confirm in case of a victory or defeat
def pressingConfirm():
    # Debug
    debugHandler("INFO","Function call: pressingConfirm()")
    
    # Forcing python to use global values
    global userConfigurations
    global globalParameters
    global timingParameters
    global sleepIntervals
    global stateMachineFlags
    global confidenceValues
        
    # Defeat confirm
    try:
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/confirmDefeat.png',confidence=confidenceValues.high)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen  
        
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/returnToSpaceship.png',confidence=confidenceValues.medium)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen                
    except:
        pass
        
    # Victory confirm
    try:
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/confirmVictory.png',confidence=confidenceValues.high)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen  
    except:
        pass
       
    
# checkingError()
# This function will reload the browser in case an error is detected
def checkingError():
    # Debug
    debugHandler("INFO","Function call: checkingError()")

    # Forcing python to use global values
    global userConfigurations
    global globalParameters
    global timingParameters
    global sleepIntervals
    global stateMachineFlags
    global confidenceValues
    
    # Abnormal error
    try: 
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/errorAbnormal.png',confidence=confidenceValues.medium)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        pyautogui.press("f5") # Refresh browser
        time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen   
    except:
        pass
    
    # Close error
    try: 
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/errorClose.png',confidence=confidenceValues.medium)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        pyautogui.press("f5") # Refresh browser
        time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen   
    except:
        pass
    
    # Memory error
    try: 
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/errorMemory.png',confidence=confidenceValues.medium)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        pyautogui.press("f5") # Refresh browser
        time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen   
    except:
        pass
    
    # Memory error
    try: 
        buttonX, buttonY = pyautogui.locateCenterOnScreen('./assets/loginFailedConfirm.png',confidence=confidenceValues.medium)
        pyautogui.moveTo(buttonX, buttonY)
        pyautogui.click()
        pyautogui.press("f5") # Refresh browser
        time.sleep(sleepIntervals.longSleep) # Waiting X seconds to update the screen   
    except:
        pass
    
    
###########################################################################################       
###########################################################################################
###########################################################################################

# Main #
def main():
    # Forcing python to use global values
    global userConfigurations
    global globalParameters
    global timingParameters
    global sleepIntervals
    global stateMachineFlags
    global confidenceValues
    
    # Creating log file
    if userConfiguration.saveLogFile == True:
        LOG_FILENAME = datetime.datetime.now().strftime('logfile_%H_%M_%S_%d_%m_%Y.log')
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
  
        logging.basicConfig(
            filename = LOG_FILENAME,
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.DEBUG,
            datefmt='%Y-%m-%d %H:%M:%S')
        
    # Initialization
    debugHandler("INFO","Initializing the script. Version is " + str(VERSION))    
    debugHandler("INFO","Official script repository: https://github.com/LeoPersike/SpaceCryptoPythonBot")
    
    # Timing
    timingParameters.lastReloadShipsTime = time.time()
    timingParameters.lastRefreshBrowserTime = time.time()
    

    
    # Loop
    while True:
        
        runThroughBrowsersAndPlay()
        time.sleep(sleepIntervals.mediumSleep)
         
    return 0

# Guard #
if __name__ == '__main__':
    main()