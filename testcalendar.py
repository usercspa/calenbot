import os
import sys
import speech_recognition as sr
import pyttsx3
import glob
import numpy as np
import json

r = sr.Recognizer()


def getSpeech():
    text = "unknown"
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    return text

def loadcalendar():
    c = json.load(open("calendar.json","r"))
    print ("calendar loaded")
    print ("************************")
    print (c)
    return c

def dictatecalendar(c):
    eng = pyttsx3.init()
    for i in c['schedule']:
        eng.say("entry number " + str(i['id']))
        eng.runAndWait()
        eng.say(str(i['name']))
        eng.runAndWait()
        eng.say("date is " + str(i['date']))
        eng.runAndWait()
        eng.say("at " + str(i['time']))
        eng.runAndWait()

def savecalendar(c):
    json.dump(c, open("calendar.json","w"))

def retrieveeventbyname(c, name):
    for i in c['schedule']:
        if i['name'].lower() in name.lower():
            return i
    nullevent = {}
    nullevent['id'] = -1
    return nullevent

def removeeventbyname(c, name):
    found = 0
    obj = c['schedule']
    for i in range(len(obj)):
        if obj[i]["name"] in name:
            obj.pop(i)
            c['schedule'] = obj
            return 1

    return 0


def retrieveeventsbydate(c, date):
    found = 0
    print(date)
    eng = pyttsx3.init()
    for i in c['schedule']:
        if i['date'].lower() in date.lower():
            found = 1
            eng.say(str(i['name']))
            eng.runAndWait()
            eng.say("date is " + str(i['date']))
            eng.runAndWait()
            eng.say("at " + str(i['time']))
            eng.runAndWait()

            # return i
    if found == 0:
        eng.say("sorry, no events found on that date")
        eng.runAndWait()



def saymenu():
    eng = pyttsx3.init()
    eng.say("main menu ")
    eng.runAndWait()
    eng.say("please choose one of the following options ")
    eng.runAndWait()
    eng.say("say load calendar to load the calendar, say add entry to add an entry, say remove entry to delete an entry, say dictate to listen to calendar, say save calendar to save")
    eng.runAndWait()
    eng.say("say look up entry or retrieve entry to retrieve an event ")
    eng.runAndWait()
    eng.say("say exit to exit the program ")
    eng.runAndWait()


exit = 0
loaded = 0
c = {}
n = 0
eng = pyttsx3.init()
eng.say("hello how may i help you? please say menu or help to get the system menu ")
eng.runAndWait()


while (exit == 0):
    # saymenu()
    
    sentence = getSpeech()
    
    if 'help' in sentence or 'menu' in sentence:
        saymenu()
        continue
    
    if 'remove' in sentence or 'delete' in sentence:
        if loaded == 0:
                print("load calendar first!")
                eng.say("please load the calendar first by saying load calendar ")
                eng.runAndWait()
                continue

        print("remove ")
        # eng.say("ok, tell me the name of the entry you want to remove. for example, say doctor appointment to remove that single event")
        eng.say("warning, entries removed cannot be recovered. are you sure?")
        eng.runAndWait()
        sentence2 = getSpeech()
        if 'yes' in sentence2 or 'Yes' in sentence2:
            sen = sentence.lower()
            sen = sen.split("remove",1)[1]
            print(sen)
            entry =  removeeventbyname(c, sen) 
            if entry == 0:
                eng.say("sorry, no such entry was found in the calendar ")
                eng.runAndWait()
                continue
            print(entry)
            eng.say("entry removed successfully")
            eng.runAndWait()
            continue 
        eng.say("removal cancelled")
        eng.runAndWait()
        continue 
    
    if 'when' in sentence or 'When' in sentence:
        if loaded == 0:
            print("load calendar first!")
            eng.say("please load the calendar first by saying load calendar ")
            eng.runAndWait()
            continue


        sen = sentence.lower()
        sen = sen.split("when is",1)[1]
        print(sen)
        entry =  retrieveeventbyname(c, sen) 
        if entry['id'] == -1:
            eng.say("sorry, no such entry was found in the calendar ")
            eng.runAndWait()
            continue
        print(entry)
        eng.say(str(entry['name']))
        eng.runAndWait()
        eng.say("date is " + str(entry['date']))
        eng.runAndWait()
        eng.say("at " + str(entry['time']))
        eng.runAndWait()
        continue


    if "all" in sentence or "All" in sentence:
        if loaded == 0:
            print("load calendar first!")
            eng.say("please load the calendar first by saying load calendar ")
            eng.runAndWait()
            continue

        sen = sentence.split("on",1)[1] 
        print(sen)
        retrieveeventsbydate(c, sen)
        continue




    if 'retrieve' in sentence or 'look up' in sentence:
        if loaded == 0:
            print("load calendar first!")
            eng.say("please load the calendar first by saying load calendar ")
            eng.runAndWait()
            continue

        print("look up ")
        eng.say("ok, do you want to get a specific entry or a specific date? for example, say give me all events on September 4th for events on that day, or say when is my doctor appointment to get the date and time for that single event")
        eng.runAndWait()
        sentence = getSpeech()
        if 'when' in sentence or 'When' in sentence:
            sen = sentence.lower()
            sen = sen.split("when is",1)[1]
            print(sen)
            entry =  retrieveeventbyname(c, sen) 
            if entry['id'] == -1:
                eng.say("sorry, no such entry was found in the calendar ")
                eng.runAndWait()
                continue
            print(entry)
            eng.say(str(entry['name']))
            eng.runAndWait()
            eng.say("date is " + str(entry['date']))
            eng.runAndWait()
            eng.say("at " + str(entry['time']))
            eng.runAndWait()
            continue
        if "all" in sentence or "All" in sentence:
           sen = sentence.split("on",1)[1] 
           print(sen)
           retrieveeventsbydate(c, sen)
           continue
  
    if 'exit' in sentence:
        exit = 1
        break
    if 'load' in sentence:
        c = loadcalendar()
        loaded = 1
        for i in c['schedule']:
            n = i['id']
        n = n + 1
        continue
    if 'dictate' in sentence:
        if loaded == 0:
            print("load calendar first!")
            eng.say("please load the calendar first by saying load calendar ")
            eng.runAndWait()
            continue
        else:
            dictatecalendar(c)
            continue
    if 'save' in sentence:
        if loaded == 0:
            print("load calendar first!")
            eng.say("please load the calendar first by saying load calendar ")
            eng.runAndWait()
            continue
        else:
            savecalendar(c)
            continue
    if 'add' in sentence:
        if loaded == 0:
            print("load calendar first!")
            eng.say("please load the calendar first by saying load calendar ")
            eng.runAndWait()
            continue
        else:
            entry = {}
            entry['id'] = n
        
            
            eng.say("please say name of entry ")
            eng.runAndWait()
            sentence = getSpeech()
            entry['name'] = sentence
            eng.say("please say date of entry ")
            eng.runAndWait()
            sentence = getSpeech()
            entry['date'] = sentence
            eng.say("please say time of entry ")
            eng.runAndWait()
            sentence = getSpeech()
            entry['time'] = sentence
            c['schedule'].append(entry)
            continue
    
    eng.say("sorry, i didnt get that ")
    eng.runAndWait()


eng = pyttsx3.init()
eng.say("goodbye ")
eng.runAndWait()
print("goodbye")
eng.stop()


