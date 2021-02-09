import random
import sys

# TODO What can I add?
# Make the program more user-friendly:
# Maybe if we get an infiniteError, allow the user to alter the words or the size of the grid and retry
# Add a file writer for the key to the word search
# Make it easier for the user to input without having to type them in all over again if something goes wrong

# TODO NOTE: Max length for an rtf file (and all other file types I think) is 28


class colors:  # Allows me to use colors in the terminal
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# All letters into one string
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

elements = []  # Empty List

# Asks for size of grid
length = int(input("Length of grid:"))
height = int(input("Height of grid:"))

# Adds <height> lists to elements
count1 = 0
while count1 < height:
    elements.append([])
    count1 += 1

# Adds random letters to fill a length x height grid
for i in range(height):
    count2 = 0
    while count2 < length:
        elements[i].append(letters[random.randint(0, 25)])
        count2 += 1

# Prints grid
for i in range(height):
    print(elements[i])

# Asks for words to put in word search
print("Input the words you want in the word search:\nType \'done\' when you are finished")

# Puts words into a list called words
words = []
repeat = True
while repeat is True:
    inpt = input()
    if inpt.lower() == 'done':
        repeat = False
    elif inpt.lower() == 'undo':  # Allows user to undo the word the recently inputted
        print("Removed %s" % words[len(words) - 1])
        words.remove(words[(len(words) - 1)])
    # Checks if word will fit inside grid
    elif len(inpt) > height and len(inpt) > length:
        print("Word too large.")
    else:
        words.append(inpt.upper())

# Prints set of words
print(words)

alreadyUsed = []  # Empty list

# Dictionary holding all the slot directions with with xy coord changes
allDirections = {'directionx0': 0,
                 'directionx1': 1,
                 'directionx2': 1,
                 'directionx3': 1,
                 'directionx4': 0,
                 'directionx5': -1,
                 'directionx6': -1,
                 'directionx7': -1,
                 'directiony0': -1,
                 'directiony1': -1,
                 'directiony2': 0,
                 'directiony3': 1,
                 'directiony4': 1,
                 'directiony5': 1,
                 'directiony6': 0,
                 'directiony7': -1}

'''
    DIRECTION KEY:
    0 = North
    1 = NorthEast
    2 = East
    3 = SouthEast
    4 = South
    5 = SouthWest
    6 = West
    7 = NorthWest

    Y Value is flipped!
'''


def canWordBeInserted(word, direction, x, y):  # Checks if word can be inserted

    result = True

    i = 0
    for letter in range(0, len(word)):  # Checks if the whole word will fit in the grid
        if isSpotAvailable([x + (i * (allDirections['directionx%d' % direction])),
                            y + (i * (allDirections['directiony%d' % direction]))], word[i]) is False:
            result = False
        i += 1
    return result


def insertLetter(letter, x, y):  # Inserts letter into the grid
    elements[y][x] = letter  # Inserts letter
    alreadyUsed.append([x, y])
    alreadyUsed.append(letter)


def isSpotAvailable(location, letter):  # Checks if 'location'(given as [x, y]) is available for 'letter'
    result = True
    for i in range(len(alreadyUsed)):  # Loops through alreadyUsed
        if i % 2 == 0:  # If the spot being looked at is a coord pair
            if alreadyUsed[i][0] == location[0] and \
                            alreadyUsed[i][1] == location[1] and alreadyUsed[i + 1] != letter:
                result = False

    if location[0] >= length or location[0] < 0:  # Checks if x-value of location is within the grid
        result = False
    if location[1] >= height or location[1] < 0:  # Checks if y-value of location is within the grid
        result = False

    return result


def printKey():
    # Finds and prints grid with letters of words standing out
    for i in range(height):  # Iterates through y values
        string = ''  # Empty string
        for j in range(len(elements[i])):  # Iterates through x values
            doThis = True
            for k in range(len(alreadyUsed)):  # Iterates through alreadyUsed
                if k % 2 == 0:  # Only checks coord pair in alreadyUsed
                    if [j, i] == alreadyUsed[k]:  # If that spot is being taken up by part of a word
                        string += (colors.OKBLUE + '%s  ' + colors.ENDC) % (elements[i][j])  # Prints letter with color
                        doThis = False  # Makes sure it doesn't print again normally (non-colored)
                        break
            if doThis is True:
                string += '%s  ' % elements[i][j]
        print(string)


def printGrid():
    # Prints grid
    for i in range(height):
        string = ''
        for j in range(len(elements[i])):
            string += '%s  ' % elements[i][j]
        print(string)


# Inserts word into grid
for word in words:

    infiniteError = 0
    retry = True
    while retry is True:  # Loops until a the word has found a spot where it will fit

        retry = False

        infiniteError += 1
        if infiniteError >= 15000:  # Is this number alright?
            sys.exit("Process expired. Perhaps there were too many words in too small of a space..")

        # Chooses random values for x, y, and direction
        y = random.randint(0, height - 1)
        x = random.randint(0, length - 1)
        direction = random.randint(0, 7)

        if canWordBeInserted(word, direction, x, y) is False:
            retry = True
        else:
            i = 0
            for letter in range(0, len(word)):  # Inserts word into grid
                insertLetter(word[letter], x + (i * (allDirections['directionx%d' % direction])),
                                           y + (i * (allDirections['directiony%d' % direction])))
                i += 1

printGrid()

print(words)

print("Press ENTER when you would like to the key")
input()

printKey()

response = input("Would you like to save this word search?")
if response.lower() == 'yes':

    title = input("What would you like to call this word search?")

    path = ''
    house = input("Are you at your (moms) house or your (dads) house?")
    if house.lower() == 'dads':
        path = 'C:\\Users\\jtlov_000\\Desktop\\Everything\\Coding and Programming\\PythonWordSearches'
    else:
        path = 'C:\\Users\\Josh\\Desktop\\Everything\\Coding and Programming\\PythonWordSearches'

    askfiletype = int(input("Do you want a 1)docx file \t2)txt file \t3)rtf file"))
    filetype = ''
    while True:

        if askfiletype == 1:
            filetype = '.docx'
            break
        elif askfiletype == 2:
            filetype = ".txt"
            break
        elif askfiletype == 3:
            filetype == ".rtf"
            break
        else:
            print("Please re-enter")

    file1 = open(path + '//' + title + filetype, 'w')  # Creates a file of name with title

    file1.write(title + '\n\n')

    # Prints grid
    for i in range(height):
        string = ''
        for j in range(len(elements[i])):
            string += '%s  ' % elements[i][j]
        file1.write(string + '\n')

    # Prints words
    file1.write("\n\n")
    for word in words:
        file1.write(word + '\t')

    file1.close()

print("Goodbye")
sys.exit()
