import os
import json
import pygame
import requests

from time import sleep
from colorama import Fore
from requests.packages.urllib3.exceptions import InsecureRequestWarning

Username = "AShayEna"

activePlayerData = "https://127.0.0.1:2999/liveclientdata/playerscores?summonerName="
playerList = "https://127.0.0.1:2999/liveclientdata/playerlist"

musicPath = "music/"

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
            print("Failed: getting player Ally!\n Make sure you are on a game!")
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
        clear_console()
        print("\n No kills done. Rend les ancêtres fiers! \n")
        if nowPlaying !=  "mii":
            mii.play(-1)
        nowPlaying = "mii"
        return None, None, None
    mii.stop()

    return isOK, kp, percent

def resultOutput(isOK, kp, percent, nowPlaying):
    if isOK:
        clear_console()
        playSong(guerrier, "guerrier", nowPlaying)
        nowPlaying = "guerrier"
        print("\n ♥ All good! You're a king!! ♥ \n")
    else:
        clear_console()
        playSong(flute, "flute", nowPlaying)
        nowPlaying = "flute"
        print("\n WTF BRO! STOP TROLLING\n")
    print("\nRatio: "+ str(kp) + "/" + str(allKills) + " ("+ str(percent) +")")
    return nowPlaying

def clear_console():
    os.system('cls')

def playSong(song, songName, nowPlaying):

    if songName == nowPlaying:
        return
    else:
        if songName == "guerrier":
            guerrier.stop()
        else:
            flute.stop()
        song.play(-1)

if __name__ == "__main__":
    pygame.mixer.init()

    guerrier = pygame.mixer.Sound(musicPath+"guerrier.mp3")
    flute = pygame.mixer.Sound(musicPath+"flute.mp3")
    mii = pygame.mixer.Sound(musicPath+"mii.mp3")

    guerrier.set_volume(0.03)
    flute.set_volume(0.03)
    mii.set_volume(0.03)

    nowPlaying = ""

    while True:
        kills, assists = getPlayerKP()
        allKills = allyKills(getAllyName()) + kills
        isOK, kp, percent = calcKP(kills, assists, allKills)
        if isOK != None:
            nowPlaying = resultOutput(isOK, kp, percent, nowPlaying)
        sleep(5)
