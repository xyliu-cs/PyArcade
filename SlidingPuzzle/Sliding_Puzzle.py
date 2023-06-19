import random

# used to record the steps            
count = 0

# Ask the user to input a value to certify the puzzle's scale
# keep prompting the user to input again if the conditions are not satisfied 
# Assign the input value to integer n as a global variable
def chooseNum():
    while True:
        # the puzzle is an n*n matrix
        global n 
        n = input('Please choose a number from 3 to 10 for your puzzle: ')
        try:
            n = int(n)
            if n >= 3 and n <= 10:
                # break only if n is an integer and is in [3,10]
                break
            else:
                continue
        except:
            continue

# Ask the user to choose four characters to execute moving up, down, left and right
# keep prompting the user to input again if the input is not a character
# Assign the inputs to the up/down/left/right as global variables
def checkChar():
    global up, down, left, right
    prompt2 = 'Please check your input again!'
    while True:
        temp1 = input('Please select a character for moving upwards: ')
        if temp1 in alphabet:
            up = temp1
            # remove the chosen character from the alphabet to avoid repetition error
            alphabet.remove(temp1) 
            # break only if the input is in the alphabet
            break     
        else:
            print(prompt2)
            continue
    
    while True:
        temp2 = input('Please select a character for moving downwards: ')
        if temp2 in alphabet:
            down = temp2
            alphabet.remove(temp2)
            break     
        else:
            print(prompt2)
            continue

    while True:
        temp3 = input('Please select a character for moving leftwards: ')
        if temp3 in alphabet:
            left = temp3
            alphabet.remove(temp3)
            break        
        else:
            print(prompt2)
            continue

    while True:
        temp4 = input('Please select a character for moving rightwards: ')
        if temp4 in alphabet:
            right = temp4
            break     
        else:
            print(prompt2)
            continue

# Generate a one-dimensional list by sequence and insert '0' at the last position
# execute upwards/downwards/leftwards/rightwards function to the puzzle randomly by n^4 times
# return the list as the initial puzzle 
def createlist():
    # the prototype of the puzzle
    global rawlst
    rawlst = [i for i in range(1, n**2)]
    rawlst.insert(n**2 -1, 0)
    i = 0
    while i < n**4:
        # generate a random integer in [1,4] to execute the according function
        k = random.randint(1,4)
        if k == 1:
            upwards()
            i += 1
        elif k == 2:
            downwards()
            i += 1
        elif k == 3:
            leftwards()
            i += 1
        elif k == 4:
            rightwards()
            i += 1
    # return the list after execute n^4 times
    return rawlst

# Switch the position between '0' and the number beneath it and return the outcome
# return the initial list if there's nothing beneath '0'
# similar logic used for the following three movement functions
def upwards():
    global count
    n1 = rawlst.index(0)
    # the index of the number beneath '0' is greater than that of '0' by n
    n2 = n1 + n
    # check if the index is out of range. i.e. there's nothing beneath '0'
    if n2 > n**2 - 1:
        return rawlst
    else:
        rawlst[n1], rawlst[n2] = rawlst[n2], rawlst[n1]
        # only count the valid step
        count += 1
        return rawlst  

def downwards():
    global count
    n1 = rawlst.index(0)
    n2 = n1 - n
    # check if there's anything above '0'
    if n2 < 0:
        return rawlst
    else:
        rawlst[n1], rawlst[n2] = rawlst[n2], rawlst[n1]
        count += 1
        return rawlst  

def leftwards():
    global count
    n1 = rawlst.index(0)
    # the index of the number right next to '0' equals to the index of '0' plus 1
    n2 = n1 + 1
    #check if '0' is at the end of the row. i.e. nothing right to it.
    if (n1+1) % n == 0:
        return rawlst
    else:
        rawlst[n1], rawlst[n2] = rawlst[n2], rawlst[n1]
        count += 1
        return rawlst  

def rightwards():
    global count
    n1 = rawlst.index(0)
    n2 = n1 - 1
    # check if '0' is at the beginning of the row. i.e. nothing left to it
    if n1 % n == 0:
        return rawlst
    else:
        rawlst[n1], rawlst[n2] = rawlst[n2], rawlst[n1]
        count += 1
        return rawlst, count

# Replace '0' with a blank to form a new list
# print the new list with n numbers a row
def printout():
    countnum = 0
    flst = [' ' if i == 0 else i for i in rawlst]
    for i in flst:
        # format the output by assigning 4 positions to each number 
        print(str(i).ljust(4, ' '), end='')
        countnum +=1
        # print on a new line if there are n numbers in a row
        if countnum % n == 0:
            print(end='\n')

# Ask the user to execute the movement repeatedly until the final conditions are met
# print the outcome for each movement
# prompt a reminder if the input is not matched with the any chosen characters before
# print the congrats & steps used to complete if passes the evalutaion
def repetition():
    global count
    global up, down, left, right
    while True:
        prompt1 = 'Please continue your move ("%s"-up/"%s"-down/"%s"-left/"%s"-right/"exit" to exit): '\
             %(up, down, left, right)
        temp = input(prompt1)
        # match input with according character to triger the function
        if temp == up:
            upwards()
            printout()
        elif temp == down:
            downwards()
            printout()
        elif temp == left:
            leftwards()
            printout()
        elif temp == right:
            rightwards()
            printout()
        # the user may exit the game anytime by inputting 'exit'
        elif temp == 'exit':
            break
        # no match found between the input and the characters chosen 
        else:
            print('Please check your instruction input')
        # break the loop if final conditions are met
        if checkfinal():
            print('Congratulations! You have winned this game in %s steps!!'%str(count))
            break

# check if the list is sorted by sequence 
def checkfinal():
    global rawlst
    newlst = [i for i in range(1,n**2+1)]
    manlst = [n**2 if i == 0 else i for i in rawlst]
    if manlst == newlst: 
        return True
    else:
        return False
        
def main():
    global count
    print('Welcome to Xiaoyuan\'s puzzle world! \nHave Fun & Good Luck :)' )
    chooseNum()
    checkChar()
    createlist()
    # clear the steps used for preparing the list
    count = 0
    printout()
    repetition()

# Ask the if user want to restart a game after finished 
while True:
    # created to check if the input is a character
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n', \
            'o','p','q','r','s','t','u','v','w','x','y','z']
    main()
    choice = input('Do you want to start a new game? "y"-Yes, enter anything else to exit ')
    if choice == 'y':
        continue
    else:
        break
