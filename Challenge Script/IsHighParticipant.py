

from calendar import c
import os
import json
from turtle import update
import pygame
import requests
import tkinter as tk

from time import sleep
from colorama import Fore
from requests.packages.urllib3.exceptions import InsecureRequestWarning

Username = "AShayEna"

activePlayerData = "https://127.0.0.1:2999/liveclientdata/playerscores?summonerName="
playerList = "https://127.0.0.1:2999/liveclientdata/playerlist"

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

nowPlaying = ""



class Overlay:
    """
    Creates an overlay window using tkinter
    Uses the "-topmost" property to always stay on top of other Windows
    """
    def __init__(self, initial_text: str):
        self.initial_text = initial_text
        self.root = tk.Tk()

        # Set up Close Label
        self.close_label = tk.Label(
            self.root,
            text=' X |',
            font=('Consolas', '14'),
            fg='green3',
            bg='grey19'
        )

        # Set up Ping Label
        self.ping_text = tk.StringVar()
        self.ping_label = tk.Label(
            self.root,
            textvariable=self.ping_text,
            font=('Consolas', '14'),
            fg='green3',
            bg='grey19'
        )
        self.ping_label.grid(row=0, column=1)

        # Define Window Geometry
        self.root.overrideredirect(True)
        self.root.geometry("+5+5")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

        self.root.after(1000, self.getData)

    def getData(self):
        kills, assists = getPlayerKP()
        # kp = kills + assists
        allKills = allyKills(getAllyName()) + kills
        calcKP(kills, assists, allKills)
        self.root.after(1000, self.getData)

    def update_label(self, update_text) -> None:
        self.ping_text.set(update_text)

    def run(self) -> None:
        self.ping_text.set(self.initial_text)
        self.root.mainloop()

def getPlayerKP():
    try:
        r =requests.get(activePlayerData + Username, verify=False)
        jsonPlayer = json.loads(r.text)
    except:
        print("\n")
        print("Failed: getting player KP!\n Make sure you are on a game!")
        exit(1)
    kills, assists = parseKP(r)

    kp = int(kills) + int(assists)
    return parseKP(r)

def parseKP(r):
    jsonPlayer = json.loads(r.text)

    kills = jsonPlayer['kills']
    assists = jsonPlayer['assists']

    return kills, assists

def allyKills(AllyList):
    allKills = 0
    
    for playerName in AllyList:
        try:
            r =requests.get(activePlayerData + playerName , verify=False)
        except:
            print("\n")
            print("Failed: getting player KP!\n Make sure you are on a game!")
            exit(1)

        kills, assists = parseKP(r)
        allKills += kills

    return allKills

def getAllyName():
    AllyList = []
    Team = ""

    try:
        r =requests.get(playerList, verify=False)
    except:
        print("\n")
        print("Failed: Couldn't retrieve allied username")
        exit(1)
    
    jsonPlayerList = json.loads(r.text)

    ### Get player team
    for player in jsonPlayerList:
        playerName = player["summonerName"]
        if playerName == Username:
            Team = player["team"]

    ### Get teammate
    for player in jsonPlayerList:
        playerName = player["summonerName"]
        if playerName != Username and player["team"] == Team:
            AllyList.append(playerName)
    return AllyList

def calcKP(kills, assists, allKills):
    global nowPlaying, overlay

    try:
        kp = kills + assists
        percent = (kp / allKills) * 100
        isOK = percent >= 90
    except ZeroDivisionError as e:
        print("\n No kills done. Rend les ancêtres fiers! \n")
        if nowPlaying !=  "mii":
            mii.play(-1)
        nowPlaying = "mii"
        return
    
    if isOK:
        clear_console()
        playSong(guerrier, "guerrier")
        nowPlaying = "guerrier"
        print("\n ♥ All good! You're a king!! ♥ \n")
    else:
        clear_console()
        playSong(flute, "flute")
        nowPlaying = "flute"
        print("\n WTF BRO! STOP TROLLING\n")
    overlay.update_label(f"kp: {percent}%")
    print("\nRatio: "+ str(kp) + "/" + str(allKills) + " ("+ str(percent) +")")

def clear_console():
    os.system('cls')

def playSong(song, songName):
    # song = pygame.mixer.Sound(songName)
    #song.set_volume(0.05)
    global nowPlaying
    print(nowPlaying)

    if songName == nowPlaying:
        return
    else:
        if songName == "guerrier":
            guerrier.stop()
        else:
            flute.stop()
        song.play(-1)

overlay = Overlay("NONE")

if __name__ == "__main__":
    pygame.mixer.init()

    guerrier = pygame.mixer.Sound("guerrier.mp3")
    flute = pygame.mixer.Sound("flute.mp3")
    mii = pygame.mixer.Sound("mii.mp3")

    guerrier.set_volume(0.03)
    flute.set_volume(0.03)
    mii.set_volume(0.03)
    overlay.run()
    exit(0)
