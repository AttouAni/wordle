import pygame
import sys
import random
import nltk
from tkinter import messagebox

pygame.init()

nltk.download('words')
wordlist = nltk.corpus.words.words()
words= [word.lower() for word in wordlist if len(word)==5]

width = 485
height = 690

screen = pygame.display.set_mode((width,height))
background = pygame.image.load("assets/bg.png")
background_rect = background.get_rect(center=(242,230))
pygame.display.set_caption("Hello Wordle!")

screen.fill("white")
screen.blit(background, background_rect)
pygame.display.update()

green = "#6aaa64"
yellow = "#c9b458"
grey = "#787c7e"
outline = "#d3d6da"
filled_outline = "#878a8c"

correct_word = random.choice(words)
#correct_word="coder"

available_letter_font = pygame.font.Font("assets/FreeSansBold.otf", 20)
alphabet = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
keys = []

class Key:
    def __init__(self,x, y, letter):
        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 37, 49)
        self.bg_color = outline

    def draw(self):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        self.text_surface = available_letter_font.render(self.text,True,"white")
        self.text_rect = self.text_surface.get_rect(center=(self.x+18,self.y+20))
        screen.blit(self.text_surface,self.text_rect)
        pygame.display.update()


keyX=10
keyY=490

for i in range(3):
    for letter in alphabet[i]:
        newKey = Key(keyX,keyY,letter)
        keys.append(newKey)
        newKey.draw()
        keyX = keyX+47.5
    keyY = keyY+60
    if i ==0:
        keyX=35
    elif i == 1:
        keyX= 82


#Les variables global 
guesses_count= 0
guesses = [[]]*6
current_guess= []
current_guess_string= ""
current_letter_X = 82
game_result=""


guessed_lettter_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
letter_size= 60
letterX =65
letterY = 8
class Letter:
    def __init__(self,text,bg_position):
        self.bg_color = "white"
        self.text_color="black"
        self.bg_position= bg_position
        self.bgX=bg_position[0]
        self.bgY=bg_position[1]
        self.bg_rect= (self.bgX,self.bgY,letter_size,letter_size)
        self.text = text
        self.text_position= (self.bgX+30, self.bgY+30)
        self.text_surface = guessed_lettter_font.render(self.text,True,self.text_color)
        self.text_rect= self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        pygame.draw.rect(screen,self.bg_color,self.bg_rect)
        if self.bg_color=='white':
            pygame.draw.rect(screen,filled_outline,self.bg_rect,2)
        self.text_surface = guessed_lettter_font.render(self.text,True,self.text_color)
        screen.blit(self.text_surface,self.text_rect)
        pygame.display.update()

    def delete(self):
        pygame.draw.rect(screen, "white",self.bg_rect)
        pygame.draw.rect(screen,outline,self.bg_rect,2)
        pygame.display.update()

def create_new_letter():
    global current_guess_string, current_letter_X
    current_guess_string= current_guess_string+ key_pressed
    new_letter = Letter(key_pressed, (current_letter_X, guesses_count*77+letterY))
    current_letter_X = current_letter_X + letterX
    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()

def delete_letter():
    global current_guess_string,current_letter_X
    guesses[guesses_count][-1].delete()
    guesses[guesses_count].pop()
    current_guess_string = current_guess_string[:-1]
    current_guess.pop()
    current_letter_X=current_letter_X-letterX

def check_guess(g):
    global current_guess,current_guess_string,guesses_count,current_letter_X,game_result
    game_decided=False
    dupCheck=list(correct_word)
    print(dupCheck)
    for i in range(5):
        letter = g[i].text.lower()
        if letter in correct_word:
            if letter==correct_word[i]:
                dupCheck[i]=""
                g[i].bg_color = green
                g[i].text_color = "white"

                for key in keys:
                    if key.text == letter.upper():
                        key.bg_color= green
                        key.draw()

                if game_decided==False :
                    game_result="W"
            else:
                index = dupCheck.index(letter)
                dupCheck[index]= ""

                g[i].bg_color = yellow
                g[i].text_color = "white"

                for key in keys:
                    if key.text == letter.upper() and key.bg_color != green:
                        key.bg_color = yellow
                        key.draw()

                game_result = ""
                game_decided = True
        else:
            g[i].bg_color = grey
            g[i].text_color = "white"  

            for key in keys:
                if key.text == letter.upper():
                    key.bg_color= grey
                    key.draw()

            game_result = ""
            game_decided = True 
        g[i].draw()
        pygame.display.update()
    print(dupCheck)
    guesses_count=guesses_count+1
    current_guess= []
    current_guess_string=""
    current_letter_X =82

    if guesses_count ==6 and game_result=="":
        game_result="L"

def play_again():
    pygame.draw.rect(screen,"white",(10,450,width-20,500))
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 30)
    play_again_text = play_again_font.render("Press ENTER to Play Again!",True,"black")
    play_again_rect = play_again_text.get_rect(center=(width/2, 600))
    right_word = "The word was "+correct_word+" !"
    right_word_text = play_again_font.render(right_word, True,"black")
    right_word_rect = right_word_text.get_rect(center=(width/2, 550))
    screen.blit(right_word_text, right_word_rect)
    screen.blit(play_again_text, play_again_rect)
    pygame.display.update()

def reset():
    global guesses_count, correct_word, guesses, current_guess,current_guess_string, game_result
    screen.fill("white")
    screen.blit(background,background_rect)
    guesses_count=0
    correct_word= random.choice(words)
    guesses = [[]]*6
    current_guess=[]
    current_guess_string= ""
    game_result= ""
    pygame.display.update()
    for key in keys:
        key.bg_color= outline
        key.draw()




while True:
    if game_result != "":
        play_again()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_result != "":
                    reset()
                else:
                    if len(current_guess_string) != 5:
                        messagebox.showerror("Error", "Word must be of 5 letters !")
                    elif current_guess_string.lower() not in words:
                        messagebox.showerror("Erreur", "Word does not exist !")
                    else:
                        check_guess(current_guess)
            elif event.key == pygame.K_BACKSPACE:
                if len(current_guess) >0:
                    delete_letter()
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                    if len(current_guess_string) <5 and game_result =="":
                        create_new_letter()
