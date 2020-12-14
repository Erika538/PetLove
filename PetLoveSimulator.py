import time


class Pet:
    RFID = 1
    
    def __init__(self, name, species, breed, username, server):
        self.name = name
        self.species = species
        self.breed = breed
        self.RFID = None
        self.server = server
        self.owner = None
        
        while self.owner == None:
            for user in self.server.users:
                if user.username == username:
                    self.owner = user

            if self.owner == None:
                print()
                print('Error! Owner account not found!')
                print('1. Register new user account')
                print('2. Try a different account')
                print('3. Cancel')
            
                decision = int(input('Enter Choice: '))
                while decision != 1 and decision != 2 and decision != 3:
                    decision = int(input('Error! Please enter 1, 2, or 3: '))

                if decision == 1:
                    self.server.registerUser()
                    for user in self.server.users:
                        if user.username == username:
                            self.owner = user

                elif decision == 2:
                    username = input('Enter new username: ')

                elif decision == 3:
                    break

            else:
                print('Success!')
                print(self.owner)
                break
        

    def assignRFID(self):
        self.RFID = Pet.RFID
        print("RFID assigned! Your pet' RFID number is:", self.RFID)
        Pet.RFID += 1

    def printPetDetails(self):
        print()
        print('Name:', self.name)
        print('Species:', self.species)
        print('Breed:', self.breed)
        print('RFID:', self.RFID)
        
        
    def __str__(self):
        pet_string = f'Name: {self.name}\nSpecies: {self.species}\nBreed: {self.breed}\nRFID: {self.RFID}'
        return pet_string


class TreatDispenser:
    idNum = 1     #global id number used for dispenserIDs
    
    def __init__(self, username, server):
        self.dispenserID = TreatDispenser.idNum    #use global id number
        self.isLoaded = False
        self.doorOpen = False
        self.RFID = False
        self.Motion = False
        self.Sound = False
        self.choice = 0               #<--do we need this?
        self.owner = username         #should this be username or user object
        self.server = server
        TreatDispenser.idNum +=  1    #increment global id number
        


    def __str__(self):
        dispenser_string = f'DeviceNo: {self.dispenserID} /n Owner: {self.owner}'
        return dispenser_string    


    #pass username as argument, match with an account on the server
    #and link the dispenser to that user's account
    def registerDevice(self, user):
        change = False
        for account in self.server.users:
            if account.username == user and account.device == None:
                account.device = self
                change = True
            elif account.username == user and account.device:
                print('Error! Device already linked to this account!')

        if change == False:
            print('Error! user not found!')


    def dispenseTreat(self):
        if self.treatCheck():
            self.openDoor()
        else:
            pass


    def video(self):
        print('Joined Video Call')
        #hardware needed


    def openDoor(self):
        print('Treat door open')
        self.doorOpen = True
        print('Treat Dispensed')
        time.sleep(1)
        print('Treat door closed')
        self.doorOpen = False
        #hardware, add to dispenseTreat


    def treatCheck(self):
        #if sensor read:
        return True
        #else:
        """
        print('Error! Treat Dispenser Empty! Please refill!')
        return False """


    def fillTreats(self):
        self.isLoaded = True


    def simulateRFID(self):
        self.RFID = True


    def simulateMotion(self):
        self.Motion = True
    

    def simulateSound(self):
        self.Sound = True


    def detectSignal(self):
        if self.RFID:
            return 1
        elif self.Motion:
            return 2
        elif self.Sound:
            return 3
        else:
            return -1


    def getChoice(self):

        while self.choice < 1 or self.choice > 4:
            print('Welcome to PetLove Simulator!')
            print('-----------------------------')
            print('1. Simulate Signal')
            print('2. Simulate Motion')
            print('3. Simulate Noise')
            print('4. Exit')
            print()
            choice = int(input('Enter your choice: '))
            self.choice = choice
    

    def run(self):
        self.getChoice()

        if self.choice == 1:
            self.simulateRFID()

        elif self.choice == 2:
            self.simulateMotion()

        elif self.choice == 3:
            self.simulateSound()

        elif self.choice == 4:
            pass
        


class User:
    def __init__(self, name, username, userDevice = None):
        self.name = name
        self.username = username
        self.device = userDevice


    def __str__(self):
        user_string = f"Name: {self.name} '/n' username: {self.username} /n DeviceNo: {self.device}"
        return user_string
        

    def generateMessage(self):
        choice = self.device.detectSignal()
        if choice == 1:
            print('RFID Detected!')
        elif choice == 2:
            print('Motion Detected!')
        elif choice == 3:
            print('Loud Sound Detected!')
        else:
            print('No activity at this time.')


    def getChoice(self):
        choice = 0
        print()
        print('Do you wish to dispense a treat/View video?')
        print('1. Dispense Treat.')
        print('2. View Video')
        print('3. Ignore')
        choice = int(input('Choice: '))
        return choice


class Server:
    def __init__(self):
        self.users = []
        self.dispensers = []
        self.pets = []


    #get info from user, create a user account, add to server's list of users
    def registerUser(self):
        name = input('Enter your name: ')
        username = input('Enter desired username: ')
        while username in self.users:
            print('Error! This username already exists!')
            username = input('Please enter a new one: ')

        user = User(name, username)
        self.users.append(user)
        print()
        print('Success! User added!')
        print(user)


    def registerPet(self):
        #get all necessary pet info
        name = input('Enter pet name: ')
        species = input('Enter pet species: ')
        breed = input('Enter pet breed or n/a if unknown: ')
        owner = input('Enter your username: ')

        #create pet object and add to the server's list of pets
        pet = Pet(name, species, breed, owner, self)
        pet.assignRFID()
        self.pets.append(pet)
        print()
        print('Success! Pet added!')
        print(pet)


    def registerDevice(self):
        username = input('Enter your username: ')

        #create dispenser object and add to server list
        device = TreatDispenser(username, self)
        device.registerDevice(username)
        self.dispensers.append(device)
        print('Success! Device added!')
        print(device)


    def displayUsers(self):
        if len(self.users) > 0:
            for user in self.users:
                print(user)
        else:
            print('No active users')


    def displayPets(self):
        if len(self.pets) > 0:
            for pet in self.pets:
                print(pet)
        
        else:
            print('No active pets')


    def displayDispensers(self):
        if len(self.dispensers) > 0:
            for dispenser in self.dispensers:
                print(dispenser)

        else:
            print('No active dispensers')
        


def main():

    #start the server
    myServer = Server()

    
    #main menu
    answerList = [1,2,3,4,5]    #menu answers, used for error handling
    while True:
        print('Welcome to PetLove Simulator!')
        print('-----------------------------')
        print()
        print('1. Register New User')
        print('2. Register New Pet')
        print('3. Register New Device')
        print('4. Simulate')
        print('5. Exit')
        userInput = int(input('Enter Choice: '))

        while userInput not in answerList:
            userInput = int(input('Enter Choice: '))

        if userInput == 1:
            myServer.registerUser()

        elif userInput == 2:
            myServer.registerPet()

        elif userInput == 3:
            myServer.registerDevice()

        elif userInput == 4:
            myAccount = None
            print()
            print('Login')
            username = input('Enter your username: ')
            
            while myAccount == None:
                for account in myServer.users:
                    if account.username == username:
                        myAccount = account

                if myAccount == None:
                    print('Account not found')
                    username = input('Enter new username: ')

            myDispenser = myAccount.device
            myDispenser.run()    
            myAccount.generateMessage()

            choice = myAccount.getChoice()

            if choice == 1:
                myDispenser.dispenseTreat()
            elif choice == 2:
                myDispenser.video()
            elif choice == 3:
                print('Connection Ended, no treat dispensed.')
                pass

        elif userInput == 5:
            print('Thank you, Exiting...')
            break


main()

    
    
        
            
