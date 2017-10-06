#Safian Omar Qureshi
#ID 10086638
#TA: Mojtaba Komeili
#T03
#v1.55 (last modified 4:39pm, June 21, 2017)

#A text-based game involving a 'student life simulation' written in Python. Upon running the game,
#a grid is displayed of fun and workpoints with the student 'S' character. Using the number input,
#user can move around the grid to collect points. Random events are also triggered which have an
#an effect on the game. A cheat menu is provided to trigger these events or turn on debug messages.

#Program was written employing functions written my James Tam with permission.

#Limitations: the ctrl+c break out of loop command is handled by the exception and so
#it doesn't break the loop in movement options. Can make it a little annoying to debug but simply enter
#into cheat menu and ctrl+c to break out of loop there.

#I also used weak variable names like 'w' and 'f' instead of workPoints, funPoints because I was
#writing my code as a roughcopy and when doing the final copy it was much too long and the find and
#replace method didn't work to change all instances of 'w's and 'f's since they are simply letters

import random

SIZE = 10
TURNS = 13
STUDENT = "S"
WORK = "w"
FUN = "f"
TAMINATOR = "T"
EMPTY = " "
debugOn = False

# Author:  James Tam
# This function was created entirely by the above author and is
# used with permission.
# '''
# @ This function comes the creation of the list with file input.
# @ It combines readFromFile() and intialize() into one function.
# @ Normally a function should only implement one well define task but in this case
# @ the creation of the list is so trivial it may be okay to combine it with file input.
# @createListFileRead()
# @Argument: None
# @Return value: the game world in the form of a 2D list (each element has
# @been initialized to values read in from the input file
# '''
def createListFileRead():
    r = -1
    c = -1
    world = []
    inputFilename = input("Name of input file: ")
    try:
        inputFile = open(inputFilename,"r")
        r = 0
        for line in inputFile:
            world.append([])
            c = 0
            for ch in line:
                if (c < SIZE):
                    world[r].append(ch)
                c = c + 1
            r = r + 1
        inputFile.close()
    except IOError:
        print("Error reading from " + inputFilename)

    return(world)

# Author:  James Tam
# This function was created entirely by the above author and is
# used with permission.
# '''
# @display()
# @Argument: a reference the 2D list which is game world.
# @The list must be already created and properly initialized
# @prior to calling this function!
# @Return value: Mone
# @Displays each element of the world with each row all on one line
# @Each element is bound: above, left, right and below with a bar (to
# @make elements easier to see.
# '''
def display(world):
    for r in range (0, SIZE, 1):
    # Row of dashes before each row
        for i in range (0, SIZE, 1):
            print(" -", end="")
        print()
        for c in range (0, SIZE, 1):
            # Vertical bar before displaying each element
            print("|" + world[r][c], end="")
        print("|") # Vertical bar right of last element + CR to
		           # move output to the next line

    # A line of dashes before each row, one line after the last
    # row.
    for i in range (0, SIZE, 1):
        print(" -", end="")
    print()

# Author:  James Tam
# This function was created entirely by the above author and is
# used with permission.
# '''
# @ This function works in conjunction with readFromFile()
# @intialize()
# @Argument: None
# @Return value: the game world in the form of a 2D list (each element
# @is set to an exclamation mark).
# '''
def initialize():
    world = []
    for r in range (0, SIZE, 1):
        world.append ([])
        for c in range (0, SIZE, 1):
            world[r].append ("!")
    return(world)

# '''
# @ This method works in conjunction with initialize. Initialize creates
# @ the list with list elements containing a default value '!'. This method
# @ relies on the list already being created and sets each list element to
# @ a corresponding value read in from the input file e.g. the string at
# @ row 2 and column 4 in the input file will initialize the list element
# @ at this same location in the 2D list (game world).
# @readFromFile()
# @Argument: None
# @Return value: the game world in the form of a 2D list (each element
# @will now be initialized to the values read in from the input file
# '''
def readFromFile():
    r = -1
    c = -1
    world = initialize() # Needed to create the 2D list
    inputFilename = input("Name of input file: ")
    inputOk=False
    while inputOk==False:
        try:  #here i added a try/except block to handle invalid file names
            inputFile = open(inputFilename,"r")
            r = 0
            # Read one line at a time from the file into a string
            for line in inputFile:
                c = 0
                # Iterate 1 char at a time through the string
                for ch in line:
                    # Including EOL there's 11 characters per line
                    # 10x10 list , exclude the EOL to avoid reading
                    # outside the bounds of the list (10 columns)
                    if (c < SIZE):
                        # Set list element to the single char
                        # read from file
                        world[r][c] = ch
                        # Advance to next element along row
                        c = c + 1
                    # Entire row has been set to values read in from
                    # file, move to next row
                r = r + 1
            inputFile.close()
            inputOk=True
        except:
            print("Error reading from file, please try again!")
            inputFilename = input("Enter a valid name for the input file: ")
    return(world)

######################################################################################################
######################################################################################################


def studentLocation(world): #this function parses through the 2D list world to get student location
    sRow=0
    sCol=0
    for r in range (0,SIZE,1):
        sCol=0
        for c in range (0,SIZE,1):
            if world[r][c]==STUDENT:
                sRow=sRow
                sCol=sCol
                return(sRow,sCol)
            sCol=sCol+1
        sRow=sRow+1


def selectionChecker(selection): #function is passed selection parameter which then checks it and returns to caller
    inputOk=False
    while inputOk==False:
        try:
            selection=int(input("Selection (must be 1-9): "))
            while (selection<0 or selection>9):
                print("Invalid selection! Must be 1-9!")
                selection=int(input("Selection (must be 1-9): "))
        except:
            print("Non-numerical character input! Must be 1-9!")
        else:
            inputOk=True
    return(selection)


def inBounds(row,col): #boolean function employed to check for user student 'S' bounds, uses passed row,col amd returns true/false to caller
    outside = True
    if ((row<0) or (col<0) or (row>=SIZE) or (col>=SIZE)):
        outside=False
    return(outside)


def moveDown(world,sRow,sCol,turn,w,f): #individual move functions for specific movements, takes world parameter to create movement
    if (sRow<SIZE-1):   #and takes sRow, sCol turn w and f parameters to update location/points, returns them back to caller
        sRow=sRow+1
        sCol=sCol
        w,f=pointCheck(world,sRow,sCol,w,f)
        if ((inBounds(sRow-1,sCol))==True):
            world[sRow-1][sCol]=EMPTY
        if ((inBounds(sRow,sCol))==True):
            world[sRow][sCol]=STUDENT

    else:
        world[sRow][sCol]=STUDENT
    return(sRow,sCol,turn,w,f)


def moveUp(world,sRow,sCol,turn,w,f):
    if (sRow>0):
        sRow=sRow-1
        sCol=sCol
        w,f=pointCheck(world,sRow,sCol,w,f)
        if ((inBounds(sRow+1,sCol))==True):
            world[sRow+1][sCol]=EMPTY
        if ((inBounds(sRow,sCol))==True):
            world[sRow][sCol]=STUDENT

    else:
        world[sRow][sCol]=STUDENT
    return(sRow,sCol,turn,w,f)


def moveUpRight(world,sRow,sCol,turn,w,f):
    if (sRow>0 and sCol<SIZE-1):
        sRow=sRow-1
        sCol=sCol+1
        w,f=pointCheck(world,sRow,sCol,w,f)
        if ((inBounds(sRow+1,sCol-1))==True):
            world[sRow+1][sCol-1]=EMPTY
        if ((inBounds(sRow,sCol))==True):
            world[sRow][sCol]=STUDENT
    else:
        world[sRow][sCol]=STUDENT
    return(sRow,sCol,turn,w,f)


def moveUpLeft(world,sRow,sCol,turn,w,f):
    if (sRow>0 and sCol>0):
        sRow=sRow-1
        sCol=sCol-1
        w,f=pointCheck(world,sRow,sCol,w,f)
        if ((inBounds(sRow+1,sCol+1))==True):
            world[sRow+1][sCol+1]=EMPTY
        if ((inBounds(sRow,sCol))==True):
            world[sRow][sCol]=STUDENT
    else:
        world[sRow][sCol]=STUDENT
    return(sRow,sCol,turn,w,f)


def moveLeft(world,sRow,sCol,turn,w,f):
    if (sCol>0):
        sRow=sRow
        sCol=sCol-1
        w,f=pointCheck(world,sRow,sCol,w,f)
        if ((inBounds(sRow,sCol+1))==True):
            world[sRow][sCol+1]=EMPTY
        if ((inBounds(sRow,sCol))==True):
            world[sRow][sCol]=STUDENT
    else:
        world[sRow][sCol]=STUDENT
    return(sRow,sCol,turn,w,f)


def moveRight(world,sRow,sCol,turn,w,f):
    if (sCol<SIZE-1):
        sRow=sRow
        sCol=sCol+1
        w,f=pointCheck(world,sRow,sCol,w,f)
        if ((inBounds(sRow,sCol-1))==True):
            world[sRow][sCol-1]=EMPTY
        if ((inBounds(sRow,sCol))==True):
            world[sRow][sCol]=STUDENT
    else:
        world[sRow][sCol]=STUDENT
    return(sRow,sCol,turn,w,f)


def moveDownRight(world,sRow,sCol,turn,w,f):
    if (sRow<SIZE-1 and sCol<SIZE-1):
        sRow=sRow+1
        sCol=sCol+1
        w,f=pointCheck(world,sRow,sCol,w,f)
        if ((inBounds(sRow-1,sCol-1))==True):
            world[sRow-1][sCol-1]=EMPTY
        if ((inBounds(sRow,sCol))==True):
            world[sRow][sCol]=STUDENT
    else:
        world[sRow][sCol]=STUDENT
    return(sRow,sCol,turn,w,f)


def moveDownLeft(world,sRow,sCol,turn,w,f):
    if (sRow<SIZE-1 and sCol>0):
        sRow=sRow+1
        sCol=sCol-1
        w,f=pointCheck(world,sRow,sCol,w,f)
        if ((inBounds(sRow-1,sCol+1))==True):
            world[sRow-1][sCol+1]=EMPTY
        if ((inBounds(sRow,sCol))==True):
            world[sRow][sCol]=STUDENT
    else:
        world[sRow][sCol]=STUDENT
    return(sRow,sCol,turn,w,f)


def pointCheck(world,sRow,sCol,w,f): #checks if the character user will land on is a w or f, updates the variables
    if world[sRow][sCol]==WORK:      #I know I should have used a better name like workPoints/funPoints for the variable name
        w=w+1                       #but I realized this too late in my program and find/replace did not work to find single w/f characters
    elif world[sRow][sCol]==FUN:    #too many instances to replace them all manually, please consider that thanks
        f=f+1
    return(w,f) #returns w,f to caller in using to update points


def playerMove(world,sRow,sCol,turn,w,f,selection): #player move function as an aggregate, takes world,sRow,sCol,turn,w,f,selection
    sRow=sRow                                   #parameters to update them accordingly
    sCol=sCol

    if (selection==1):
        sRow,sCol,turn,w,f=moveDownLeft(world,sRow,sCol,turn,w,f)
    elif (selection==2):
        sRow,sCol,turn,w,f=moveDown(world,sRow,sCol,turn,w,f)
    elif (selection==3):
        sRow,sCol,turn,w,f=moveDownRight(world,sRow,sCol,turn,w,f)
    elif (selection==4):
        sRow,sCol,turn,w,f=moveLeft(world,sRow,sCol,turn,w,f)
    elif (selection==6):
        sRow,sCol,turn,w,f=moveRight(world,sRow,sCol,turn,w,f)
    elif (selection==7):
        sRow,sCol,turn,w,f=moveUpLeft(world,sRow,sCol,turn,w,f)
    elif (selection==8):
        sRow,sCol,turn,w,f=moveUp(world,sRow,sCol,turn,w,f)
    elif (selection==9):
        sRow,sCol,turn,w,f=moveUpRight(world,sRow,sCol,turn,w,f)
    return(sRow,sCol,turn,w,f) #returns updated points/row/column of student


def pavolEvent(turn,pavolActive): #pavol event function, generates 1/10 number and if it is that one, triggers pavol
    pavolChance=random.randint(0,9) #takes turn as parameter to update it, pavol active to determining of pavol can be triggered or not
    if pavolChance==0:
        if debugOn==True:
            print("//pavol triggered")
        print("You are blessed by Pavol, you're next turn # is same as previous turn #")
        turn=turn-1
        pavolActive=True
    return(turn,pavolActive)


def tamEvent(world,sRow,sCol,taminatorTurns): #tam event triggered with 25% chance, takes world parameter to see where to put it randomly
    tamChance=random.randint(0,3) #taminator turns is used to count turns it is active

    if tamChance==0:
        if debugOn==True:
            print("//tam triggered")
        print("<<Taminator SPAWNED!>>")
        taminatorTurns=taminatorTurns+1 #updates the turns for taminator to be active
        tRow=random.randint(0,SIZE-1) #randomly puts it in some location
        tCol=random.randint(0,SIZE-1)
        world[tRow][tCol]=TAMINATOR

        if tRow==sRow and tCol==sCol:
            print("A very, VERY unlikely event occured! Taminator tried to spawn on top of you but you fought him off!")
            world[tRow][tCol]=STUDENT
    else:
        tRow=-1
        tCol=-1
    return(taminatorTurns,tRow,tCol) #returns the tRow,tCol to be used in chase algorithm, taminatorturns for checking how long it can be active


def taminatorChase(sRow,sCol,tRow,tCol,dRow,dCol): #chase algorithm for taminator, takes current student position and current tam position
                                                #also takes tam destination row/col to not land on the student
    if sRow>tRow:
        if (sRow - tRow ==1):
            dRow=tRow+1
        else:
            dRow=tRow+2
        if dRow==sRow and dCol==sCol:
            dRow=dRow-1
    elif sRow<tRow:
        if (tRow - sRow == 1):
            dRow=tRow-1
        else:
            dRow=tRow-2
        if dRow==sRow and dCol==sCol:
            dRow=dRow+1
    else:
        dRow=tRow

    if sCol>tCol:
        if (sCol - tCol ==1):
            dCol=tCol+1
        else:
            dCol=tCol+2
        if dRow==sRow and dCol==sCol:
            dCol=dCol-1
    elif sCol<tCol:
        if tCol - sCol==1:
            dCol=tCol-1

        else:
            dCol=tCol-2
        if dRow==sRow and dCol==sCol:
            dCol=dCol+1
    else:
        dCol=tCol

    if dRow==sRow and dCol==sCol:      #this is a very special boundary case
        dRow=dRow-1                 #that I encountered after exhaustive placement of Taminator against the top edge
        if dRow==-1:                #of the map. Essentially if taminator goes out of bounds, this brings it back
            dRow=dRow+1         #it was a VERY RARE bug that I had to encounter by actually trying all possible tam locations
            dCol=dCol+1
            if dCol==SIZE:
                dCol=dCol-2

    return(dRow,dCol) #outputs a destination location that will be used by the tam move function


def tamCheckDown(world,turn,taminatorTurns,tRow,tCol,caught):

    if ((inBounds(tRow-1,tCol))==True): #check down
        if (world[tRow-1][tCol]==STUDENT):
            turn=turn+2
            taminatorTurns=0
            if debugOn==True:
                print("//caught you DOWN")
            print("Haha, caught you!")
            caught=True

    return(turn,taminatorTurns,caught)


def tamCheckUp(world,turn,taminatorTurns,tRow,tCol,caught):

    if ((inBounds(tRow+1,tCol))==True): #check up
        if (world[tRow+1][tCol]==STUDENT):
            turn=turn+2
            taminatorTurns=0
            if debugOn==True:
                print("//caught you UP")
            print("Haha, caught you!")
            caught=True

    return(turn,taminatorTurns,caught)


def tamCheckUpRight(world,turn,taminatorTurns,tRow,tCol,caught):

    if ((inBounds(tRow-1,tCol+1))==True): #check upright
        if (world[tRow-1][tCol+1]==STUDENT):
            turn=turn+2
            taminatorTurns=0
            if debugOn==True:
                print("//caught you UPRIGHT")
            print("Haha, caught you!")
            caught=True

    return(turn,taminatorTurns,caught)


def tamCheckUpLeft(world,turn,taminatorTurns,tRow,tCol,caught):

    if ((inBounds(tRow-1,tCol-1))==True): #check upleft
        if (world[tRow-1][tCol-1]==STUDENT):
            turn=turn+2
            taminatorTurns=0
            if debugOn==True:
                print("//caught you UPLEFT")
            print("Haha, caught you!")
            caught=True

    return(turn,taminatorTurns,caught)


def tamCheckLeft(world,turn,taminatorTurns,tRow,tCol,caught):

    if ((inBounds(tRow,tCol-1))==True): #check left
        if (world[tRow][tCol-1]==STUDENT):
            turn=turn+2
            taminatorTurns=0
            if debugOn==True:
                print("//caught you LEFT")
            print("Haha, caught you!")
            caught=True

    return(turn,taminatorTurns,caught)


def tamCheckRight(world,turn,taminatorTurns,tRow,tCol,caught):

    if ((inBounds(tRow,tCol+1))==True): #check right
        if (world[tRow][tCol+1]==STUDENT):
            turn=turn+2
            taminatorTurns=0
            if debugOn==True:
                print("//caught you RIGHT")
            print("Haha, caught you!")
            caught=True

    return(turn,taminatorTurns,caught)


def tamCheckDownRight(world,turn,taminatorTurns,tRow,tCol,caught):

    if ((inBounds(tRow+1,tCol+1))==True): #down right
        if (world[tRow+1][tCol+1]==STUDENT):
            turn=turn+2
            taminatorTurns=0
            if debugOn==True:
                print("//caught you DOWNRIGHT")
            print("Haha, caught you!")
            caught=True

    return(turn,taminatorTurns,caught)


def tamCheckDownLeft(world,turn,taminatorTurns,tRow,tCol,caught):

    if ((inBounds(tRow+1,tCol-1))==True): #downleft
        if (world[tRow+1][tCol-1]==STUDENT):
            turn=turn+2
            taminatorTurns=0
            if debugOn==True:
                print("//caught you DOWNLEFT")
            print("Haha, caught you!")
            caught=True

    return(turn,taminatorTurns,caught)


def tamLocCheck(world,turn,taminatorTurns,tRow,tCol): #this function checks all blocks around taminator to check for student

    caught=False                                    #world is checking along with turns to update if player is caught
    turn,taminatorTurns,caught=tamCheckDown(world,turn,taminatorTurns,tRow,tCol,caught)
    turn,taminatorTurns,caught=tamCheckUp(world,turn,taminatorTurns,tRow,tCol,caught)
    turn,taminatorTurns,caught=tamCheckUpLeft(world,turn,taminatorTurns,tRow,tCol,caught)
    turn,taminatorTurns,caught=tamCheckUpRight(world,turn,taminatorTurns,tRow,tCol,caught)
    turn,taminatorTurns,caught=tamCheckLeft(world,turn,taminatorTurns,tRow,tCol,caught)
    turn,taminatorTurns,caught=tamCheckRight(world,turn,taminatorTurns,tRow,tCol,caught)
    turn,taminatorTurns,caught=tamCheckDownLeft(world,turn,taminatorTurns,tRow,tCol,caught)
    turn,taminatorTurns,caught=tamCheckDownRight(world,turn,taminatorTurns,tRow,tCol,caught)

    return(turn,taminatorTurns,caught) #returns taminator turns if player is caught, tam turns = 0, returns turns and also caught variable
                                    #caught variable used to update taminator list to move it out of the display(world)

def taminatorMove(world,tRow,tCol,dRow,dCol): #move function which replaces previous location with empty
    if ((inBounds(tRow,tCol))==True):
        world[tRow][tCol]=EMPTY
    if ((inBounds(dRow,dCol))==True):
        world[dRow][dCol]=TAMINATOR #taking into arguments the ones provided by chase algorithm function


def cheatMenuOptions():
    print("")
    print("Cheat menu options")
    print("=================")
    print("(t)oggle debug messages on/off")
    print("(m)ake Taminator appear!")
    print("(p)avol manifest itself")
    print("(q)uit cheat menu")


def debugSubMenu(): #activating debugging
    global debugOn

    toggleMessages=input("Press 'y' for debugging messages, 'n' for none, any other key to return to main cheat menu: ")
    if toggleMessages=="y":
        debugOn=True
        print("You have turned debugging messages ON, debugOn variable is", debugOn)
    elif toggleMessages=="n":
        debugOn=False
        print("You have turned debugging messages OFF, debugOn variable is", debugOn)
    else:
        print("You have pressed a key beside 'y' or 'n' and have returned back to main cheat menu")


def tamCheatEvent(world,sRow,sCol,tRow,tCol,taminatorTurns,pavolActive): #checks if pavol/tam are already active first
    if pavolActive==True: #world, tRow,tCol is used as paramaters to see where to put taminator
        print("")           #taminatorturns and pavolActive used to see if tamiantor can be activated or not
        print("Pavol is active! The blessed power stops Taminator...")
    elif taminatorTurns!=0:
        print("")
        print("Whoa, whoa, whoa! Taminator is already active, can't have two! That would be crazy!")

    else:
        print("")
        print("You are about to activate TAMINATOR")

        inputOk=False #exception handling is used for non numerical input
        while inputOk==False:
            try:
                checkOnTop=True
                while checkOnTop==True:
                    tRow = int(input("Select the row you would like to spawn Taminator: "))
                    while (tRow<0 or tRow>SIZE-1): #choosing location to spawn taminator
                        print("Row is out of bounds! Must be between 0 and",SIZE-1)
                        tRow = int(input("Select the row you would like to spawn Taminator: "))

                    tCol = int(input("Select the column you would like to spawn Taminator: "))
                    while (tCol<0 or tCol>SIZE-1):
                        print("Column is out of bounds! Must be between 0 and",SIZE-1)
                        tCol = int(input("Select the column you would like to spawn Taminator: "))
                    if (tRow==sRow and tCol==sCol):
                        print("Error! Can not spawn Taminator on top of student! Give him a chance!")
                    else:
                        checkOnTop=False

            except:
                print("Non-numeric type entered! Try again!")
            else:
                inputOk=True
        taminatorTurns=1
        world[tRow][tCol]=TAMINATOR
        print("")
        print("Taminator successfully activated by cheat!\nTaminator will appear at:\nRow:", tRow,"Column:", tCol)
    return(tRow,tCol,taminatorTurns)


def pavolCheatEvent(turn,taminatorTurns,pavolActive): #checks if pavol/tam is already active, if not then activates it
    if pavolActive==True:
        print("")
        print("Hey, hey, hey!\nPavol is already active!")
    elif taminatorTurns!=0:
        print("")
        print("Looks like Taminator is active, Pavol is too scared to come out...")
    else:
        print("")
        print("You activated Pavol by cheat and got a free turn!")
        turn=turn-1
        pavolActive=True
    return(turn,pavolActive) #returns turn/pavolActive to caller so that it may/may not be actiaveted again, turn updates main game turns


def cheatMode(world,sRow,sCol,turn,tRow,tCol,taminatorTurns,pavolActive): #main cheat function used for accessing the submenus, takes
    quitCheats=False   #world,turn,tRow,tCol,taminatorTurns,pavolactive as parameters because they affect main game

    while quitCheats==False:
        cheatMenuOptions()
        cheatSelection=input("Enter 't' or 'm' or 'p' or 'q': ")

        if cheatSelection=="t":
            debugSubMenu()

        elif cheatSelection=="m":
            tRow,tCol,taminatorTurns=tamCheatEvent(world,sRow,sCol,tRow,tCol,taminatorTurns,pavolActive)

        elif cheatSelection=="p":
            turn,pavolActive=pavolCheatEvent(turn,taminatorTurns,pavolActive)

        elif cheatSelection=="q":
            print("Returning back to game...")
            print("")
            if pavolActive==True:
                print("You are blessed by Pavol (by cheats!), you're next turn # is same as previous turn #")
            elif taminatorTurns!=0:
                print("<<Taminator SPAWNED (by cheats!)>>")
            quitCheats=True
        else:
            print("Invalid selection! Enter only 't' or 'm' or 'p' or 'q': ")

    return(turn,tRow,tCol,taminatorTurns,pavolActive) #returns it back to main game caller function to be used


def gameMenuOptions():
    print("")
    print("MOVEMENT OPTIONS")
    print("7 8 9\n5 5 6\n1 2 3")
    print("Type a number on the keypad to indicate direction of movement.")
    print("Type 5 to pass movement")
    if (debugOn==True):
        print("//Debugging messages are ON")


def theGame(world,sRow,sCol): #main game function, takes the sRow/sCol used by the parser function in the very beginning
                            #world parameter taken by James Tams functions
    turn=0
    w=0 #again, should have used better variable names like workPoints/funPoints but was too late into program
    f=0#and replacing all manually by hand (couldn't use find/replace) proved to be too difficult

    tRow=-1
    tCol=-1
    taminatorTurns=0
    selection=-1
    dRow=-1
    dCol=-1

    while (turn<TURNS): #runs for 13 turns (week 1 to week 13)
        if debugOn==True:
            print("//you are on the top of main game, beginning turn session...")

        pavolActive=False
        caught=False
        oRow=sRow
        oCol=sCol

        gameMenuOptions()
        selection = selectionChecker(selection)

        if (selection==0):
            turn,tRow,tCol,taminatorTurns,pavolActive=cheatMode(world,sRow,sCol,turn,tRow,tCol,taminatorTurns,pavolActive)

        elif (selection==5):
            sRow=sRow
            sCol=sCol
            print("You skipped your turn for some reason...")

        elif (selection==1 or 2 or 3 or 4 or 6 or 7 or 8 or 9):
            sRow,sCol,turn,w,f=playerMove(world,sRow,sCol,turn,w,f,selection)
            while sRow==oRow and sCol==oCol:
                print("Out of boundary selection! Must be 1-9 but not 5!")
                selection = selectionChecker(selection)
                sRow,sCol,turn,w,f=playerMove(world,sRow,sCol,turn,w,f,selection)

        if (taminatorTurns==0 and pavolActive==False):
            turn,pavolActive=pavolEvent(turn,pavolActive)

        if (taminatorTurns==0 and pavolActive==False):
            taminatorTurns,tRow,tCol=tamEvent(world,sRow,sCol,taminatorTurns)
            turn,taminatorTurns,caught=tamLocCheck(world,turn,taminatorTurns,tRow,tCol)
            if caught==True:
                print("Well that was unfortunate, Taminator spawned beside you!")

        elif (taminatorTurns==1 or taminatorTurns==2):
            if debugOn==True:
                print("//chase algo begin!")

            dRow,dCol=taminatorChase(sRow,sCol,tRow,tCol,dRow,dCol)
            taminatorMove(world,tRow,tCol,dRow,dCol)
            tRow=dRow
            tCol=dCol
            taminatorTurns=taminatorTurns+1
            turn,taminatorTurns,caught=tamLocCheck(world,turn,taminatorTurns,tRow,tCol)

        elif taminatorTurns==3:
            print("You have escaped the Taminator...for now...")
            world[tRow][tCol]=EMPTY
            taminatorTurns=0
        world[sRow][sCol]=STUDENT
        turn=turn+1
        display(world)
        if (caught==True or taminatorTurns==0):
            world[tRow][tCol]=EMPTY #this is out of display world so there is a visual indicator of when taminator catches student
                                    #and then it turns empty
        print("Current turn =", turn)
        print("Current fun points =", f)
        print("Current work points =", w)

    return(w,f)


def fileOutput(w,f): #file output function for exporting scores to file stats.txt, takes w/f as parameters from the maingame function

    if (w==0):
        grade="F"
    elif(w==1):
        grade="D"
    elif(w==2):
        grade="C"
    elif(w==3):
        grade="B"
    elif(w>=4):
        grade="A"

    
    try:
        stats = open("stats.txt","w")
        stats.write("Fun point(s) = " + str(f)+'\n')
        stats.write("Work point(s) = " + str(w)+'\n')
        stats.write("Letter Grade = " + str(grade)+'\n')
        stats.close()
        outputOk=True
    except:
        print("An error occured writing to scores.txt.")

    print("End game stats")
    print("==============")
    print("Work points = ", w)
    print("Fun points = ", f)
    print("Letter grade = ", grade,"\n")
    print("Information also saved to stats.txt")


def start(): #main start functin
    world = readFromFile()
    sRow,sCol=studentLocation(world)
    display(world)
    w,f=theGame(world,sRow,sCol) #main game function outputs w,f to be used by fileOutput function
    fileOutput(w,f)
start()
