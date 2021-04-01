import re
import hashlib
import os
import base64
import random



def login():
    while True:
        username = input("Username: ")
        if len(username) == 0:
            print("Username can not be empty")
        elif len(username) > 20:
            print("Username is too long")
        elif re.search("[^a-zA-Z0-9\\_\\.\\-\\']", str(username)):
            print("Error usernames may only contain numbers, letters, dashes, underscores, apostrophes and periods")
        else:
            break
    while True:
        password = input("Password: ")
        if len(password) == 0:
            print("Password can not be empty")
        elif len(password) > 30:
            print('Password is too long')
        # elif re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[~!@#$%^&*_\-+=`|\\(){}[\]:;'<>,.?/.]).{8,30}$", password) :
        #     break
        else:
            break
            # print("Error you may have entered some wrong credentials")
    return(username, password)


def userPanel():
    print('\n[ac] Add an Client')
    print('[ec] Edit an Client')
    print('[l] Logout')
    print('[q] Exit')
    return input("\nChoose an option: ")

def advisorPanel():
    print('\n[ac] Add an Client')
    print('[ec] Edit an Client')
    print('[l] Logout')
    print('[q] Exit')
    return input("\nChoose an option: ")

def superAdminPanel():
    print('\n[ac] Add an Client')
    print('[au] Add an user ')
    print('[ec] Edit an Client')
    print('[eu] Edit user role')
    print('[gu] Get all users')
    print('[gc] Get all Clients')
    print('[sl] Show logs')
    print('[l] Logout')
    print('[q] Exit')
    return input("\nChoose an option: ")

def systemAdminPanel():
    print('\n[ac] Add an Client')
    print('[ec] Edit an Client')
    print('[au] Add an user')
    print('[eu] Edit user role')
    print('[sl] Show logs')
    print('[l] Logout')
    print('[q] Exit')
    return input("\nChoose an option: ")

def choose_panel():
    print("\n[1] Login")
    print("[q] Quit\n")
    return input("\nLogin or quit?: ")


def captcha() :
    print("\nCaptcha, You have tried too many bad login attempts please answer the following question: ")
    captchaBool = True
    randomEquation = [('*'),('+'),('-')]
    numberEquation = random.randint(0,2)
    randomNumber1 = random.randint(1, 99)
    randomNumber2 = random.randint(1, 20)
    print("What is the answer to: " + str(randomNumber1) + ' ' + randomEquation[numberEquation] + ' ' + str(randomNumber2))
    while captchaBool:
        answer = input("the answer is: ")
        inputAnswer = str(str(randomNumber1) + ' ' + str(randomEquation[numberEquation]) + ' ' + str(randomNumber2))
        if re.search('[^0-9]',answer) :
            print("Error you can only enter a number")
        elif int(answer) == eval(inputAnswer) :
            captchaBool = False
            break
        else :
            captchaBool = True
            print("Im sorry this answer is incorrect")
