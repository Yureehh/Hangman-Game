import tkinter as tk
from tkinter import *
import random
from PIL import ImageTk, Image


#Fonts
btn_font = ("arial", 9)
guess_font = ("monospace", 24)
lost_font = ('arial', 20)
#Colors
background = "grey94"
endBackground = "lemon chiffon"
buttonsBg = "lemon chiffon"
buttonsBg2 = "grey80"
#Windows Dimesions
winWidth= 585
winHeight= 800
winEndHeight = 300
#Word and Buttons
buttons = {}
buttonSymbols = {}


#selects a random word in the "words" file
def randomWord():
    file = open('words.txt', "r")
    wordList = file.readlines()
    i = random.randint(0, len(wordList)-1)
    return wordList[i]

#creates the main window
def createWin(win, destroy):
    if destroy:
        win.destroy()
        win = Tk()
    win.title("Hangman Game")
    win.configure(bg=background if not destroy else endBackground)
    win.geometry(f"{winWidth}x{winHeight}" if not destroy else f"{winWidth}x{winEndHeight}")
    win.resizable(FALSE, FALSE)
    return win

#images taken from the folder "images"
def loadImages():
    pics = [PhotoImage(file = "images/hangman0.png"), PhotoImage(file = "images/hangman1.png"), PhotoImage(file = "images/hangman2.png"),
             PhotoImage(file = "images/hangman3.png"), PhotoImage(file = "images/hangman4.png"), PhotoImage(file = "images/hangman5.png"), PhotoImage(file = "images/hangman6.png")]
    return pics

#creates 2 rows of 13 letters on the top of the screen
def createButtons():
    print(letters)
    for i in range (2):
        for j in range (13):
            print(letters[i][j])
            button = Button(win, text = letters[i][j], width = 5, height = 2, bg = buttonsBg, font = btn_font, bd = 2, command= lambda x=i, y=j: buttonHit(x,y))
            button.grid(row=i, column=j)
            buttons[i,j] = button
            buttonSymbols[i,j] = letters[i][j]

#Triggered by clicking the button
def buttonHit(x, y):
    global guessed
    global lives
    buttons[x,y]["command"]= DISABLED
    buttons[x,y].configure(bg = buttonsBg2)
    guessed.append(buttons[x,y]["text"])
    yourWord, check = tryLetter(word, guessed)
    if yourWord.count("_") == 0:
        end(True)
    else:
        if  check:
            updateWord(yourWord)
        else:
            wrongLetter()

def tryLetter(word, guessedLetters):
    spacedWord = ''
    for x in range(len(word)-1):
        if word[x] != ' ':
            if word[x].upper() in guessedLetters:
                spacedWord += word[x].upper() + ' '
            else:
                spacedWord += "_ "
        elif word[x] == ' ':
            spacedWord += ' '
    check = hang(guessedLetters[-1].lower())
    return spacedWord, check

def hang(guess):
    return guess in word

def updateWord(word):
    wordToGuessLabel.configure(text = word)

def wrongLetter():
    global lives
    global imageLabel, livesLabel
    lives -=1
    imageLabel.configure(image = hangmanPics[6-lives])
    livesLabel.configure(text = "Lives: "+str(lives))

    if lives == 0:
        killAllButtons()
        win.after(800,end)


def killAllButtons():
    for key in buttons.keys():
        buttons[key]["command"]= DISABLED
        buttons[key].configure(bg = buttonsBg2)

def end(lost=False):

    #deletes main window to create a new one for the endscreen
    global win
    win = createWin(win, True)
    win.protocol("WM_DELETE_WINDOW", gameOver)

    #3 labels for the endscreen
    result  = Label(win,font =("Courier", 30, "bold"), bg = endBackground)
    txtWord = "The word was: "+word
    wordWas = Label(win,font =("Courier", 24), text = txtWord, bg = endBackground)
    txtPress = 'Press ESC to exit\nOr another key to play again'
    keyToPress = Label(win,font =("Courier", 24), text = txtPress, bg = endBackground)
    if lost:
        result.configure(text = "You Win")
    else:
        result.configure(text = "You Lost")

    result.pack()
    wordWas.pack()
    keyToPress.pack()

    #any key press or a doubleclick will start a new game
    win.bind("<Key>", newGame)
    win.bind("<Double-Button-1>", newGame)



def createLabels(text):
    #gets the dimesion and places the image somehow centered, long words are asymmetrical
    w = hangmanPics[0].width()
    h = hangmanPics[0].height()
    x = winWidth/2 - w/2
    y = winHeight/2 - h/2
    imagelbl = Label(win, image = hangmanPics[0])
    imagelbl.place(x = x-7, y = y+50)
    wordToGuesslbl = Label(win, text= text, font = guess_font)
    wordToGuesslbl.place(x = x-len(text)/2, y = y-50)
    liveslbl = Label(win, text= "Lives: "+ str(lives), font = guess_font, anchor = NE, fg="red")
    liveslbl.place(x = x, y = y+300)
    return  imagelbl, wordToGuesslbl, liveslbl

def gameOver(Event = None):
    global win
    global play
    play = False
    win.destroy()

def newGame(Event):
    global win
    win.destroy()

if __name__ == "__main__":
    play = True
    while play:
        letters = [ ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"],
                      ["N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] ]
        lives = 6
        guessed = []
        #picks a random word
        word = randomWord()
        tmp = ""
        for x in range(len(word)):
            tmp += "_ "
        #main window
        win = Tk()
        win.protocol("WM_DELETE_WINDOW", gameOver)
        win.bind("<Escape>", gameOver)
        win = createWin(win, False)
        #load pics
        hangmanPics = loadImages()
        #add buttons
        createButtons()
        #add hangman image
        imageLabel,wordToGuessLabel, livesLabel = createLabels(tmp)


        win.mainloop()
