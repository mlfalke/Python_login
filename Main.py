import os
import Authentication.Authentication as Authentication
import Authentication.Data.DataFile as iniData
import datetime
import time

def main_menu(Role):
    iniData.display_title_bar()
    rRole = Role.split(' ',1)
    continueM = True
    while continueM ==  True:
        if rRole[0] == 'User':
            print('\nWhat would you like to do: ')
            continueM = iniData.Main_Menu(Role, Authentication.userPanel())
        elif rRole[0] == 'Advisor':
            print('\nWelcome to the advisor menu: ')
            continueM = iniData.Main_Menu(Role, Authentication.advisorPanel())
        elif rRole[0] == 'SystemAdmin':
            print('\nWelcome to the admin menu: ')
            continueM = iniData.Main_Menu(Role, Authentication.systemAdminPanel())
        elif rRole[0] == 'SuperAdmin':
            print('\nWelcome to the Super Admin menu: ')
            continueM = iniData.Main_Menu(Role, Authentication.superAdminPanel())    
        else :
            print('\nError you entered some wrong credentials, please try again')
            time.sleep(5)
            break

def initialiseData():
    while (os.path.isfile(iniData.usersFile) == False 
        or os.path.isfile(iniData.clientsFile) == False 
        or os.path.isfile(iniData.logFile) == False):
        if os.path.isfile(iniData.clientsFile) == False:
            iniData.iniClient()
            continue
        if os.path.isfile(iniData.usersFile) == False:
            iniData.initUser()
            continue
        if os.path.isfile(iniData.logFile) == False :
            iniData.initLogs()
            continue
        else :
            break
    return
        

def login():
    count = 0
    iniData.display_title_bar()
    print("\nPlease enter your credentials")
    auth = 'Login False'
    while auth == 'Login False' :
        login = Authentication.login()
        auth = iniData.checkCredentials(login[0],login[1])
        if count > 3 :
            iniData.insertLog('Too many incorrect login attempts')
            Authentication.captcha()
            time.sleep(5)
            StartUp()
        elif auth != 'Login False' :
            break
        else :
            print("Error you have entered incorrect credentials, please try again")
            count = count + 1
    main_menu(auth)



def StartUp():
    choice = ''
    initialiseData()
    iniData.display_title_bar()
    while choice != 'q':
        choice = Authentication.choose_panel()
        iniData.display_title_bar()
        if choice == '1':
            login()
        elif choice == 'q':
            quit()
            print("\nExiting the application")
        else:
            print("\nWrong input")

StartUp()