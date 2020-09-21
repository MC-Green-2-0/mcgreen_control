import pygame
from pygame import mixer
import random
import time
import math
import sys
import threading
import os

homedir = os.getcwd()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
darker_red = (200, 0, 0)
green = (0, 255, 0)
darker_green = (0, 200, 0)
blue = (50, 89, 250)
darker_blue = (35, 67, 250)
yellow = (255, 255, 0)
darker_yellow = (200, 200, 0)
cyan = (0, 255, 255)
darker_cyan = (0, 200, 200)
pygame.display.set_caption("Games Menu")
pygame.init()

window = (1920, 1080)
screen = pygame.display.set_mode(window)


class Button:
    def __init__ (self, surfaceName, ac, ic, rectVals, text, font):
        self.ac = ac #Active color of button
        self.ic = ic #Inactive color of button
        self.rectAttrs = rectVals #(x, y, w, h) of button
        self.surfaceName = surfaceName
        self.text = text
        self.font = font

    def generate(self):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()

        #Check if mouse is on button
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.surfaceName, self.ac, self.rectAttrs)

        #Else just show darker button
        else:
            pygame.draw.rect(self.surfaceName, self.ic, self.rectAttrs)

        textSurf, textRect = text_objects(self.text, self.font)

        textRect.center = (x + (w / 2), y + (h / 2))
        self.surfaceName.blit(textSurf, textRect)
        pygame.display.update(self.get_rect())

    def get_rect(self):
        x, y, w, h = self.rectAttrs
        return pygame.rect.Rect(x, y, w, h)

    def is_pressed(self, touch_status):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()

        #Check if mouse is hovering over button or not
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if touch_status == True:
                #print('CLICK DETECTED')
                return True

            elif touch_status == False:
                return False

        #If mouse is not hovering over button, button must obviously not be pressed
        else:
            return False
def text_objects(text, font, color=(0,0,0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


buttonText = pygame.font.Font('FreeSansBold.ttf', 32)
font = pygame.font.Font('FreeSansBold.ttf', 50)
electricityButton = Button(screen, darker_yellow, yellow, (1/12*window[0], 1/4*window[1], 1/3*window[0], 3/16*window[1]), "Electricity Quiz", buttonText)
sustainabilityButton =  Button(screen, darker_green, green, (1/12*window[0], 2/4*window[1], 1/3*window[0], 3/16*window[1]), "Sustainability Quiz", buttonText)
whatswrongButton =  Button(screen, darker_red, red, (7/12*window[0], 1/4*window[1], 1/3*window[0], 3/16*window[1]), "Whats Wrong Game", buttonText)
RecycleItButton =  Button(screen, darker_blue, blue, (7/12*window[0], 2/4*window[1], 1/3*window[0], 3/16*window[1]), "Recycle It Game", buttonText)
WaterButton =  Button(screen,  darker_cyan, cyan, (1/3*window[0], 3/4*window[1], 1/3*window[0], 3/16*window[1]), "Water Calculator", buttonText)
screen.fill((255, 255, 255))
middlesex = pygame.image.load('Middlesex.png')
screen.blit(middlesex, (705, 50))
textSurf, textRect = text_objects('Games Menu', font)
textRect.center = ((window[0] / 2), 200)

screen.blit(textSurf, textRect)
while True:
    for event in pygame.event.get():
        print(event)

        if event.type == pygame.QUIT:
            # Set Face to Neutral
            # controller.face_update(getFaceNum())

            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            touch_status = True

            #Check if buttons are pressed if mouse button is down
            if electricityButton.is_pressed(touch_status):
                os.chdir(homedir + '/electricity_quiz')
                exec(open("./electric_quiz.py").read())
                os.chdir(homedir)

            elif sustainabilityButton.is_pressed(touch_status):
                os.chdir(homedir + '/sustainability_quiz')
                exec(open("./sustainability_quiz.py").read())
                os.chdir(homedir)

            elif whatswrongButton.is_pressed(touch_status):
                os.chdir(homedir + '/whats_wrong')
                exec(open("./Game File.py").read())
                os.chdir(homedir)
            elif RecycleItButton.is_pressed(touch_status):
                os.chdir(homedir + '/recycle_it')
                exec(open("./game_file.py").read())
                os.chdir(homedir)

            elif WaterButton.is_pressed(touch_status):
                os.chdir(homedir + '/water_calculator')
                exec(open("./water_calculator.py").read())
                os.chdir(homedir)



        electricityButton.generate()
        sustainabilityButton.generate()
        whatswrongButton.generate()
        RecycleItButton.generate()
        WaterButton.generate()

        pygame.display.update()
