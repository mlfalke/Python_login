import xml.etree.ElementTree as ET
from xml.dom import minidom
import hashlib
import os
import base64
import re
import time
import datetime
import socket

usersFile = './Authentication/Data/DataBase/Users'
clientsFile = './Authentication/Data/DataBase/Clients'
logFile = './Authentication/Data/Log/Logs'

def parseFile(cfile) :
    ChooseFile = ''
    if cfile == 'user' :
        ChooseFile = usersFile
    elif cfile == 'client' :
        ChooseFile = clientsFile
    elif cfile == 'log':
        ChooseFile = logFile
    elif cfile != 'user' or 'client' or 'log' :
        print("Wrong file")
    with open (ChooseFile,'r') as myfile :
        content = myfile.read()
    return ET.fromstring(base64.b64decode(bytes(decode64(content),'utf_8')).decode('utf_8'))

def saveFile(data,cfile) :
    ChooseFile = ''
    if cfile == 'user' :
        ChooseFile = usersFile
    elif cfile == 'log':
        ChooseFile = logFile
    elif cfile == 'client' :
        ChooseFile = clientsFile
    elif cfile != 'user' or 'client' or 'log' :
        print("Wrong file")
    myfile = open(ChooseFile, "wb")
    myfile.write(encode64(base64.encodebytes(data)))
    myfile.close()

def showLogs() : 
    root = parseFile('log')
    for child in root :
        print('\n'+str(child.tag) + ' : ' + str(child.attrib['ID']))
        for subchild in child :
            print('\t'+str(subchild.tag) + ' : ' + str(subchild.text))

def display_title_bar():
    # Clears the terminal screen, and displays a title bar.
    os.system('cls' if os.name == 'nt' else 'clear')
    filler = "*"
    Title = "House Construction Panel!"
    print(filler.center(120,"*"))
    print(Title.center(120,"*"))
    print(filler.center(120,"*"))

def iniClient():
    # create the file structure
    Clients = ET.Element('Clients')
    Client = ET.SubElement(Clients, 'Client')
    Full_Name = ET.SubElement(Client, 'Full_Name')
    Email = ET.SubElement(Client, "Email")
    Phone = ET.SubElement(Client, "Phone")
    Address = ET.SubElement(Client, 'Address')
    Street_Number = ET.SubElement(Address, 'Street_Number')
    Zip_Code = ET.SubElement(Address, 'Zip_Code')
    City = ET.SubElement(Address, 'City')
    # create names
    Client.set('Username', 'Test')
    Client.set('ID', '0')
    # set Data
    Full_Name.text = 'Test'
    Email.text = 'Test@Email.com'
    Phone.text = '0648327465'
    Street_Number.text ='TestStraat 123'
    Zip_Code.text = '2345ZB'
    City.text = 'Roffa'
    # create a new XML file with the results
    mydata = ET.tostring(Clients,encoding='utf_8',method='xml')
    saveFile(mydata,'client')

def initLogs():
    Logs = ET.Element('Logs')
    Log = ET.SubElement(Logs, 'Log')
    ET.SubElement(Log, 'DateTime')
    ET.SubElement(Log, 'Username')
    ET.SubElement(Log, 'Host')
    ET.SubElement(Log, 'Log')
    Log.set('ID', '0')
    mydata = ET.tostring(Logs, encoding='utf8', method='xml')
    saveFile(mydata, 'log')

def initUser():
    # create the file structure
    Users = ET.Element('Users')
    User = ET.SubElement(Users, 'User')
    ET.SubElement(User, 'Username')
    ET.SubElement(User, 'Password')
    ET.SubElement(User, 'Role')
    # create names
    User.set('ID', '0')
    User.set('Username','Test')
    # create a new XML file with the results
    mydata = ET.tostring(Users,encoding='utf_8',method='xml')
    saveFile(mydata,'user')

def searchAllUsers():
    root = parseFile('user')

    # items = mydoc.getElementsByTagName('Client')
    for child in root :
        print("\nUser: " + child.attrib['ID'])
        print(child.tag, child.attrib, child.text)
        for subchild in child:
            print("\t"+subchild.tag, ":", subchild.text)

def searchAllClient():
    root = parseFile('client')

    # items = mydoc.getElementsByTagName('Client')
    for child in root :
        print("\nUser: " + child.attrib['Username'])
        print(child.tag, child.attrib)
        for subchild in child:
            if subchild.tag == 'Address':
                print("\t"+subchild.tag, ":")
                for subchild2 in subchild:
                    print("\t\t"+subchild2.tag,":",subchild2.text)
            else:
                print("\t"+subchild.tag, ":", subchild.text)

def editClient(user,inputUser):
    root = parseFile('client')
    Role = str(user).split(' ',1)
    element = str(inputUser).lower()
    if ((Role[0] == 'SystemAdmin' or Role[0] == 'SuperAdmin') and (element != Role[1])) or element == Role[1] :
        for child in root.iter('Client') :
            # print(Role[0] + " " + Role[1] + " " + child.attrib['Username'] + " " + element)
            if (str(child.attrib['Username']).lower() == element) :
                print('\nUser: ' + child.attrib['Username'] + '\n')
                print('ID: ' + child.attrib['ID'])
                for subchild in child :
                    if str(subchild.tag) == 'Address' :
                        print('\t' + str(subchild.tag))
                        for subelement in subchild :
                            print('\t\t'+str(subelement.tag) + ' : ' + str(subelement.text))
                    else :
                        print('\t'+str(subchild.tag) + ' : ' + str(subchild.text))
        choiceID = input('\nWhich client do you want to edit? select the ID: ')
        for child2 in root.iter('Client') :
            if ((str(child2.attrib['ID']) == str(choiceID)) and (str(child2.attrib['Username']).lower() == element)):
                editClientID(child)
                mydata = ET.tostring(root,encoding='utf8',method='xml')
                saveFile(mydata,'client')
                return
    time.sleep(5)
    print("Error you probably have entered a wrong input please try again")
            
def editClientID(userChild):
    choice = ''
    while choice != 'q' :
        display_title_bar()
        for subchild in userChild :
            if str(subchild.tag) == 'Address' :
                print('\t' + str(subchild.tag))
                for subelement in subchild :
                    print('\t\t'+str(subelement.tag) + ' : ' + str(subelement.text))
            else :
                print('\t'+str(subchild.tag) + ' : ' + str(subchild.text))
        print("\npress q to exit")
        print("please select one of the following: Full_Name, Email, Phone, Address")
        choice = input("\nWhat do you want to edit? ")
        for subchild in userChild :
            if str(choice) == 'Address' and str(subchild.tag) == 'Address' :
                print("\nPlease select one of the following: Street_Number, Zip_Code, City")
                AddressValue = input("Which address value do you want to edit: ") 
                for Addresschild in subchild :
                    if str(Addresschild.tag) == AddressValue :
                        Addresschild.text = validateClient(Addresschild.tag)
            elif str(subchild.tag) == str(choice) :
                subchild.text = validateClient(subchild.tag)            
        if str(choice) == 'q' :
            break
                
def editUserRole(User,Role):
    root = parseFile('user')
    user = Role.split(' ',1)
    if user[1] == User.lower() :
        print("\nError you cannot change your own Role, that makes no sense")
        return
    for child in root.iter('User') :
        if child.find('Username').text == User.lower() :
            choice = ''
            while choice != 'q':
                print('\n[0] User \n[1] Advisor \n[2] SystemAdmin \n[3] SuperAdmin\n[q] exit(return)')
                choice = input('\nSelect the new Role:')
                if (choice == '0' and (set([user[0]]).issubset(set(['SuperAdmin',  'SystemAdmin'] )) and (child.find('Role').text != user[0]) )):
                    child.find('Role').text = 'User'
                    print('role changed to User')
                elif (choice == '1' and (set([user[0]]).issubset(set(['SuperAdmin',  'SystemAdmin'] )) and (child.find('Role').text != user[0]) )):
                    child.find('Role').text = 'Advisor'
                    print('role changed to Advisor')
                elif (choice == '2' and (set([user[0]]).issubset(set(['SuperAdmin'] )) and (child.find('Role').text != user[0]) )):
                    child.find('Role').text = 'SystemAdmin'
                    print('role changed to SystemAdmin')
                elif (choice == '3' and (set([user[0]]).issubset(set(['SuperAdmin'] )) and (child.find('Role').text != user[0]) )):
                    child.find('Role').text = 'SuperAdmin'
                    print('role changed to SuperAdmin')
                elif choice == 'q':
                    mydata = ET.tostring(root,encoding='utf_8',method='xml')
                    saveFile(mydata,'user')
                    print('exiting')
                else:
                    print('You are not able to edit this users role')

def insertUser(inputUser, password) :
    root = parseFile('user')
    username = str(inputUser).lower()
    for child in root.iter('User') :
        if child.attrib['Username'] == username :
            print("Error: Username already exists, please pick another one") 
            return False
        elif (set([username]).issubset(set(['superAdmin', 'advisor', 'systemAdmin', 'user'] ) )) :
            print("Error: This username is locked and cannot be used, please choose another one")
            return False
            # setup infrastructure
    element = ET.Element('User')
    user = ET.SubElement(element, 'Username')
    passw = ET.SubElement(element, 'Password')
    role = ET.SubElement(element, 'Role') 
    # set user
    element.set('ID', str(len(root)))
    element.set('Username', str(username))
    # set data
    user.text = username
    passw.text = encrypt(password)
    role.text = 'User'
    # append data
    root.append(element)
    # save data
    mydata = ET.tostring(root,encoding='utf_8',method='xml')
    saveFile(mydata,'user')
    return True

def insertLog(log) :
    root = parseFile('log')
    element = ET.Element('Log')
    DateTimeText = ET.SubElement(element, 'DateTime')
    Host = ET.SubElement(element, 'Host')
    Log = ET.SubElement(element, 'Log')
    # set data
    element.set('ID',str(len(root)))
    DateTimeText.text = str(datetime.datetime.now())
    Host.text = str(socket.gethostname())
    Log.text = str(log)
    #append data
    root.append(element)
    mydata = ET.tostring(root,encoding='utf8',method='xml')
    saveFile(mydata,'log')

def insertClient(username,Full_Name,Email,Phone,Street_Number,Zip_Code, City):
    # get current file
    root = parseFile('client')

    Phonechunk = [Phone[i:i+2] for i in range(0,len(Phone),2)]
    # setup infrastructure
    element = ET.Element('Client')
    fullName = ET.SubElement(element,'Full_Name')
    Mail = ET.SubElement(element,'Email')
    Number = ET.SubElement(element,'Phone')
    address = address = ET.SubElement(element,'Address')
    Street = ET.SubElement(address,'Street_Number')
    Zip = ET.SubElement(address,'Zip_Code')
    Town = ET.SubElement(address,'City')
    # set client
    element.set('Username', str(username))
    element.set('ID', str(len(root)))
    # set data
    cityList = ['Rotterdam', 'Amsterdam', 'Delft', 'Sao Paolo', 'New York', 'Berlijn', 'Munchen', 'Parijs', 'Lyon', 'Hong kong']
    fullName.text = Full_Name
    Mail.text = Email
    Number.text = "+31-6-" + str(Phonechunk[1]) + str(Phonechunk[2]) + "-" + str(Phonechunk[3]) + str(Phonechunk[4])
    Street.text = Street_Number
    Zip.text = Zip_Code
    Town.text = cityList[int(City)-1]
    # append child-element
    root.append(element)
    # update current file
    mydata = ET.tostring(root,encoding='utf8',method='xml')
    saveFile(mydata,'client')

def checkCredentials(username, password):
    root = parseFile('user')
    # if root.find('') == username :
    #     print('succes')
    if username == 'SuperAdmin':
        if password == 'DontForget' :
            return 'SuperAdmin' + ' ' + 'SuperAdmin'
        else :
            return 'Login' + ' ' + 'False'
    else :
        for child in root.iter('User') :
            if child.find('Username').text == str(username).lower() :
                # if child.find() == str(username).lower() :
                passv = child.find('Password').text
                passvalue = str(passv).split(' ',1)
                # check if hash is correct 
                if decrypt(passvalue[0], passvalue[1], password):
                    print('Login authenticated')
                    return (child.find('Role').text + ' ' + child.find('Username').text)
                else :
                    print('Invalid credentials')
                    return 'Login' + ' ' + 'False'    
        if child.find('Username').text != str(username).lower() :
            print('Invalid credentials')
            return 'Login' + ' ' + 'False'

def decrypt(salt,key,password) :
    Bsalt = base64.decodebytes(bytes(salt,'utf_8'))
    Bkey = base64.decodebytes(bytes(key, 'utf_8'))
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf_8'), Bsalt, 100000) == Bkey
    
def encrypt(password) :
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 100000)
    return str(base64.encodestring(salt),'utf_8') + ' ' + str(base64.encodestring(key),'utf_8')

def Main_Menu(Role, choice):

    user = Role.split(' ',1)
    choose = choice
    if choose == 'ac' and (set([user[0]]).issubset(set(['SuperAdmin', 'Advisor', 'SystemAdmin', 'User'] ))) :
        display_title_bar()
        inserttextClient(user[1])
    elif choose == 'au' and (set([user[0]]).issubset(set(['SuperAdmin',  'SystemAdmin'] ))) :
        display_title_bar()
        Register()
    elif choose == 'ec' and (set([user[0]]).issubset(set(['SuperAdmin', 'Advisor', 'SystemAdmin', 'User'] ) )) :
        display_title_bar()
        editClient(Role,input("\nUsername: "))
    elif choose == 'eu' and (set([user[0]]).issubset(set(['SuperAdmin', 'Advisor', 'SystemAdmin'] ) )) :
        display_title_bar()
        print('select the username which you want to edit: ')
        editUserRole(input("\nUsername: "),Role)
    elif choose == 'gu' and (user[0] == 'SuperAdmin' ) :
        display_title_bar()
        searchAllUsers()
    elif choose == "gc" and (user[0] == 'SuperAdmin' ) :
        display_title_bar()
        searchAllClient()
    elif choose == 'l' :
        display_title_bar()
        return False
    elif choose == 'sl' and (set([user[0]]).issubset(set(['SuperAdmin',  'SystemAdmin'] ))):
        display_title_bar()
        showLogs()
    elif choose == 'q' :
        exit()
    else :
        display_title_bar()
        print('Error you selected an wrong choice')
    return True

def inserttextClient(user):
    while True:
        Full_Name = input('Full Name: ')
        if len(Full_Name) == 0:
            print("Error name can not be empty")
        elif re.search(r"[*!@#$%^*()[\];\"\']",Full_Name) :
            print("Error name cannot contin any of the following symbols [*!@#$%^*()]")
        else :
            break
    while True:
        Street_Number = input('Street and number: ')
        if len(Street_Number) == 0 :
            print("Error street can not be empty")
        elif re.search(r"[*!@#$%^*()[\];\"\'\\/]",Street_Number) :
            print("Error streetname can not contain any of the following symbols [*!@#$%^*()]")
        elif re.search(r"^([1-9][e][\s])*([a-zA-Z]+(([\.][\s])|([\s]))?)+[1-9][0-9]*(([-][1-9][0-9]*)|([\s]?[a-zA-Z]+))?$", Street_Number) :
            break
        else :
            print("You have not entered a valid Address, Number combination. Please enter a valid address")
    while True :
        Zip_Code = input('Zip Code: ')
        if re.search("^[0-9]{4}[a-zA-Z]{2}$", Zip_Code) : 
            break
        else :
            print('Error you have not entered a correct zip code, Zipcode must be off format DDDDXX')
    while True:
        Email = input('Email: ')
        if len(Email) == 0:
          print("Error email can not be empty")
        elif re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",Email) :
            break
        else :
            print("Error you have not entered an valid email, please enter an valid email")
    while True:
        Phone = input('Mobile Phone: ')
        if re.search("^06[0-9]{8}$",Phone) :
            break
        elif len(Phone) != 10 :
            print("Error number can only be 10 digits long")
        else : 
            print("Error number is incorrect, number should be format 06XXXXXXXX")
    while True:
        print('Which city do you want to select: ')
        print('[1] Rotterdam [2] Amsterdam [3] Delft')
        print('[4] Sao Paolo [5] New York  [6] Berlijn')
        print('[7] Munchen   [8] Parijs    [9] Lyon')
        print('[10] Hong-kong')
        City = input('City: ')
        if len(City) > 2:
            print('Error incorrect city')
        elif re.search("^([1-9]{1})$", City) or City == '10' :
            break
        else :
            print("Error incorrect input, please choose a number between 1-10")
    insertClient(user,Full_Name, Email,Phone,Street_Number,Zip_Code,City)

def Register():
    # display_title_bar()
    print("\n Please enter your personal data")
    register2 = register()
    while insertUser(register2[0], register2[1]) != True:
        register2 = register()
    # display_title_bar()
    print('succesfully registered')

def register():
    while True:
        username = input("Username: ")
        if len(username) < 5:
            print("Username must consist of atleast 5 characters")
        elif len(username) > 20:
            print("Username can't consist of more than 20 characters")
        elif re.search("^[^a-zA-Z]", username):
            print("Username must begin with a letter")
        elif re.search("[^a-zA-Z0-9-_'.]", username):
            print("Usernames may only contain numbers, letters, dashes, underscores, apostrophes and periods")
        else:
            break

    while True:
        password = input("Password: ")
        if len(password) < 8:
            print("Password must consist of atleast 8 characters")
        elif len(password) > 30:
            print("Password can't consist of more than 30 characters")
        elif re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[~!@#$%^&*_\-+=`|\\(){}[\]:;'<>,.?/.]).{8,30}$", password):
            break
        else: 
            print("Password must contain atleast one uppercase, one lowercase, one special character and one number")
 
    return (username,password)

def validateClient(inputValue) :
    boolInput = True
    cityList = ['Rotterdam', 'Amsterdam', 'Delft', 'Sao Paolo', 'New York', 'Berlijn', 'Munchen', 'Parijs', 'Lyon', 'Hong kong']
    while boolInput == True :
        if inputValue == 'Full_Name':
            newValue = input("\nEnter a new value: ")
            if len(newValue) == 0:
                print("Error name can not be empty")
            elif len(newValue) > 80:
                print("Error name can not be longer than 80 characters")
            elif re.search(r"[*!@#$%^*()0-9]",newValue) :
                print('Error name cannot contain any special characters [.*!@#$%^*()0-9]')
            else :
                return newValue
        elif inputValue == 'Street_Number':
            newValue = input("\nEnter a new value: ")
            if len(newValue) == 0 :
                print("Error street can not be empty")
            elif re.search(r"[.*!@#$%^*()]",newValue) :
                print("Error streetname can not contain any of the following symbols [.*!@#$%^*()]")
            elif re.search(r"^([1-9][e][\s])*([a-zA-Z]+(([\.][\s])|([\s]))?)+[1-9][0-9]*(([-][1-9][0-9]*)|([\s]?[a-zA-Z]+))?$", newValue) :
                return newValue
            else :
                print("You have not entered a valid Address, Number combination. Please enter a valid address")
        elif inputValue == 'Zip_Code':
            newValue = input("\nEnter a new value: ")
            if re.search("^[0-9]{4}[a-zA-Z]{2}$", newValue) : 
                return newValue
            else :
                print('Error you have not entered a correct zip code, Zipcode must be off format DDDDXX')
        elif inputValue == 'Email':
            newValue = input("\nEnter a new value: ")
            if len(newValue) == 0:
                print("Error email can not be empty")
            elif len(newValue) > 80 :
                print("Error email can not be longer than 80 characters")
            elif re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",newValue) :
                return newValue
            else :
                print("You have not entered a valid email, please enter a valid email")
        elif inputValue == 'Phone':
            newValue = input("\nEnter a new value: ")
            if re.search("^06[0-9]{8}$",newValue) :
                Phonechunk = [newValue[i:i+2] for i in range(0,len(newValue),2)]
                return "+31-6-" + str(Phonechunk[1]) + str(Phonechunk[2]) + "-" + str(Phonechunk[3]) + str(Phonechunk[4])
            elif len(newValue) != 10 :
                print("Error number can only be 10 digits long")
            else : 
                print("Error number is incorrect, number should be format 06XXXXXXXX")
        elif inputValue == 'City':
            print('Which city do you want to select: ')
            print('[1] Rotterdam [2] Amsterdam [3] Delft')
            print('[4] Sao Paolo [5] New York  [6] Berlijn')
            print('[7] Munchen   [8] Parijs    [9] Lyon')
            print('[10] Hong-kong')
            newValue = input("\nEnter a new value: ")
            if len(newValue) > 2:
                print('Error incorrect city')
            elif re.search("^([1-9]{1})$", newValue) or newValue == '10' :
                return cityList[int(newValue)-1]
            else :
                print("Error incorrect input, please choose a number between 1-10")

def encode64(data) :
    newDATA = str(bytes(data).decode('utf8')).replace("\n", ' ')
    chunks, chunk_size = len(newDATA), len(newDATA)//len(newDATA)
    DataChunk = [newDATA[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
    # print(DataChunk)
    newData = ''
    # DataChunk = [data[i:i+1] for i in range(0,len(data),1)]
    for i in range((len(DataChunk)-1),0,-1) :
        newData = newData + str(DataChunk[i])

    return bytes(newData,'utf8')

def decode64(data) :
    newDATA = data.replace(' ', "\n")
    chunks, chunk_size = len(newDATA)-1, len(newDATA)//len(newDATA)
    DataChunk = [newDATA[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
    newData = 'PD'
    # print(DataChunk)
    # DataChunk = [data[i:i+1] for i in range(0,len(data),1)]
    for i in range((len(DataChunk)-1),0,-1) :
        newData = newData + str(DataChunk[i])
    # newData = newData + str(DataChunk[len(DataChunk)-1])
    # print(newData)
    return newData
