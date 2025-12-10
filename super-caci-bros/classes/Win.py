import pygame
import sys

from classes.Spritesheet import Spritesheet
from classes.GaussianBlur import GaussianBlur

import tkinter as tk
from tkinter import simpledialog, messagebox

ROOT = tk.Tk()
ROOT.withdraw()

class Win:
    def __init__(self, screen, entity, dashboard):
        self.screen = screen
        self.entity = entity
        self.dashboard = dashboard
        self.state = 0
        self.spritesheet = Spritesheet("./img/title_screen.png")
        self.pause_srfc = GaussianBlur().filter(self.screen, 0, 0, 640, 480)
        self.dot = self.spritesheet.image_at(
            0, 150, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )
        self.gray_dot = self.spritesheet.image_at(
            20, 150, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )

    def update(self, once):
        self.screen.blit(self.pause_srfc, (0, 0))
        self.dashboard.drawText("YOU WON", 120, 160, 68)
        # check it out
        # the input dialog
        if once:
            valid = False
            picked = None
            team_names = ['harry potter', 'hermione granger', 'ron weasley', 'luna lovegood', 'draco malfoy'
                          'rubeus hagrid', 'severus snape', 'minerva mcgonagall', 'albus dumbledore', 'lord voldemort']
            riddle = {  'harry potter':'''''', # Q
                        'hermione granger':'''''', # Z
                        'ron weasley':'''''', # S
                        'luna lovegood':'''''', # K
                        'draco malfoy':'''''', # K
                        'rubeus hagrid':'''''', # G
                        'severus snape':'''''', # G
                        'minerva mcgonagall':'''''', # S
                        'albus dumbledore':'''''', # K
                        'lord voldemort':'''Beside the lake where ripples gleam
A "Soul" awaits with quiz like scheme
Answer true, let wit prevail
Earn House points by the water's trail''' # L
            }
            while not valid:
                USER_INP = simpledialog.askstring(title="Team Name",
                                        prompt="What's your Team Name? (partial name works too)")
                if len(USER_INP) < 3:
                    messagebox.showwarning("Warning:", "Input must be longer")
                    continue
                for tn in team_names:
                    if USER_INP.lower() in tn:
                        valid = True
                        picked = tn
                
            messagebox.showinfo(f'{picked} Riddle:', riddle[picked])
            
        self.dashboard.drawText("CONGRATS !", 150, 280, 32)
        self.dashboard.drawText("BACK TO MENU", 150, 320, 32)
        self.drawDot()
        pygame.display.update()
        self.checkInput()

    def drawDot(self):
        if self.state == 0:
            self.screen.blit(self.dot, (100, 275))
            self.screen.blit(self.gray_dot, (100, 315))
        elif self.state == 1:
            self.screen.blit(self.dot, (100, 315))
            self.screen.blit(self.gray_dot, (100, 275))

    def checkInput(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.state == 0:
                        self.entity.pause = False
                    elif self.state == 1:
                        self.entity.restart = True
                elif event.key == pygame.K_UP:
                    if self.state > 0:
                        self.state -= 1
                elif event.key == pygame.K_DOWN:
                    if self.state < 1:
                        self.state += 1

    def createBackgroundBlur(self):
        self.pause_srfc = GaussianBlur().filter(self.screen, 0, 0, 640, 480)
