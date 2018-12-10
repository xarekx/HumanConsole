from tkinter import *
import os
import subprocess
import psutil
import urllib
from urllib.parse import urlencode
import webbrowser
import json
import googlemaps
import speech_recognition as sr
import pathlib
import tkinter.filedialog as fdialog


window = Tk()
window.geometry('{}x{}'.format(460, 350))


regFind = r'^((Z|z)najdz) (.*)?$'
regOpen = r'^(((W|w)łącz)*|((O|o)dpal)*|((U|u)ruchom)*) (.*)?$'
regKill = r'^(((Z|z)niszcz)*|((Z|z)abij)*|((W|w)yrzuc)*) (.*)?$'
regSite = r'^((O|o)tworz) (.*)?$'
regDire = r'^((W|w)yznacz) (.*)?$'


programs = ['opera','Opera','Chrome','chrome','notepad','Notepad','Notatnik','notatnik','Slack','slack','Ccleaner','ccleaner','Postman','postman']
site = ['stronę','strone']
roz = ['txt','docx','rtf']

def line_numbers(file_path, word_list):
    wordList = re.sub("[^\w]", " ",  file_path).split()
    for openword in word_list:
        for word in wordList:
            if(word ==openword):
                openFile(word)
                            
def line_numbersClose(file_path, word_list):
    wordList = re.sub("[^\w]", " ",  file_path).split()
    for openword in word_list:
        for word in wordList:
            if(word == openword):
                close_program(word)
#Wyznacz trase z Poznań do Gostyń
#GoogleMaps
def googleDirection(placeFrom,placeTo):
    webbrowser.open("https://www.google.com/maps/dir/?api=1&origin="+placeFrom+"&destination="+placeTo)

#Otwórz stronę kwejk.pl
#Otwieranie przeglądarki
def openWebBrowser(url_path):
    site = url_path.split(" ")
    webbrowser.open(""+site[1])
    
#Uruchom notepad, notatnik,opera,Ccleaner
#Otwieranie aplikacji .exe   
def openFile(program):
    try:
       os.startfile(program+'.exe')
    except Exception as e:
        print (str(e))

#Znajdz openMe.txt, 
#otwieranie plików txt,docx
def openDoc(docs):
    try:
        os.startfile(docs)
    except Exception as e:
        pass

#zabij notepad
#zabijanie aplikacji
def close_program(programClose):
    subprocess.call("taskkill /f /IM "+programClose+".exe")
    print(programClose)

    
def buttonClk(event):
    if(re.match(regOpen,entryText.get()) is not None):
        line_numbers(entryText.get(),programs)
    elif (re.match(regFind,entryText.get()) is not None):
        if(entryText.get().endswith(('.docx', '.txt', '.rtf'))):
            takeName=entryText.get().split()[len(entryText.get().split())-1:len(entryText.get().split())]
            openDoc(takeName[0])
        else:
            takeName=entryText.get().split()[len(entryText.get().split())-1:len(entryText.get().split())]
            window.fileName = fdialog.askopenfilename(initialdir="C:/Users/Szef/Desktop/projektPJN",filetypes = ( ( "ext files","*.docx"),("All files","*.*")))
            openDoc(""+window.fileName)
    elif(re.match(regKill,entryText.get()) is not None):
        print("Zabijam program...")
        line_numbersClose(entryText.get(),programs)
    elif(re.match(regSite,entryText.get()) is not None):
        print("Otwieranie strony...")
        openWebBrowser(entryText.get())
    elif(re.match(regDire,entryText.get()) is not None):
        print("szukam trasy....")
        for i in entryText.get().split():
            if(i == "z"):
                Tablica = []
                for z in range(entryText.get().split().index(i),len(entryText.get().split())):
                    Tablica.append(entryText.get().split()[z])
                    if(len(Tablica)==5):
                        place = Tablica[1]+"+"+Tablica[2]
                        googleDirection(place,Tablica[4])
                    elif(len(Tablica)==4):
                        googleDirection(Tablica[1],Tablica[3])
                    elif(len(Tablica)==6):
                        place1 = Tablica[1]+"+"+Tablica[2]
                        place2 = Tablica[4]+"+"+Tablica[5]
                        googleDirection(place1,place2)

#Rozpoznawanie głosu
def voiceButton(event):
    print("Powiedzże coś do laptopa no...")
    r = sr.Recognizer()
    mic = sr.Microphone(device_index = 1, sample_rate = 44100, chunk_size = 512)
    with mic as source:
        audio = r.listen(source)
        anwser = r.recognize_google(audio,language="pl-PL")
        if(re.match(regOpen,anwser) is not None):
            line_numbers(anwser,programs)
        elif (re.match(regFind,anwser) is not None):
           print("bartek")
        elif(re.match(regKill,anwser) is not None):
            print("darek")
            line_numbersClose(anwser,programs)
        elif(re.match(regSite,anwser) is not None):
            print("Otwieranie strony...")
            openWebBrowser(anwser)
        elif(re.match(regDire,anwser) is not None):
            print("szukam trasy....")
            for i in anwser.split():
                if(i == "z"):
                    Tablica = []
                    for z in range(anwser.split().index(i),len(anwser.split())):
                        Tablica.append(anwser.split()[z])
                        if(len(Tablica)==5):
                            place = Tablica[1]+"+"+Tablica[2]
                            googleDirection(place,Tablica[4])
                        elif(len(Tablica)==4):
                            googleDirection(Tablica[1],Tablica[3])
                        elif(len(Tablica)==6):
                            place1 = Tablica[1]+"+"+Tablica[2]
                            place2 = Tablica[4]+"+"+Tablica[5]
                            googleDirection(place1,place2)
            
    
        #route = entryText.get().split()[len(entryText.get().split())-4:len(entryText.get().split())]
        #googleDirection(route[1],route[3])
top_frame = Frame(window, width = 450, height = 50, pady = 3)

labelText = Label(window, text="Wpisz coś")

labelText.grid(row=0,column=0)

textValue = StringVar()
entryText = Entry(window,textvariable=textValue, width=50)
entryText.grid(row=0,column=1)


b1=Button(window,text="Działaj !",width=20)
b1.grid(row=1,column=1)
b2=Button(window,text="Włącz mówienie",width=20)
b2.grid(row=3,column=1)
d = b1.bind("<ButtonPress-1>",buttonClk)
e = b2.bind("<ButtonPress-1>",voiceButton)


window.mainloop()
