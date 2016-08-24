# -*- coding: utf-8 -*-
#!/usr/bin/env python
import json
import urllib
import requests
from bs4 import BeautifulSoup
from flask import Flask, request
from threading import Timer

app = Flask(__name__)
params = {"access_token": "Page Access Token"}  # Token that facebook requires to access the API
headers = {"Content-Type": "application/json"}
usersblocked = {}

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
    if not request.args.get("hub.verify_token") == "Verify Token": # Your token (you need to insert it in webhook details)
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "How did you get there? Anyway, here there's nothing to see.", 200


@app.route('/', methods=['POST'])
def webook(): # function that recognise request and send it to the right function
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]
                try:
                    if messaging_event["message"]["quick_reply"]["payload"] == "Page2CL":
                        convoylist(sender_id,3,5,2)
                    elif messaging_event["message"]["quick_reply"]["payload"] == "Page3CL":
                        convoylist(sender_id,5,7,3)
                    elif messaging_event["message"]["quick_reply"]["payload"] == "Page4CL":
                        convoylist(sender_id,7,9,4)
                    elif messaging_event["message"]["quick_reply"]["payload"] == "Page5CL":
                        convoylist(sender_id,9,11,5)
                    elif messaging_event["message"]["quick_reply"]["payload"] == "Page6CL":
                        convoylist(sender_id,11,13,6)
                    elif messaging_event["message"]["quick_reply"]["payload"] == "Convoy list":
                        convoylist(sender_id,1,3,1)
                except (TypeError,KeyError) as e:
                    pass
                if messaging_event.get("message"):
                    try:
                        if "Xk<M0c6+R94gVU3nn~Q+6ppY8-v5" in messaging_event["message"]["text"]:
                            globalmessage(messaging_event["message"]["text"])
                    except KeyError:
                        pass
                if messaging_event.get("postback"):
                    if sender_id not in usersblocked or usersblocked[sender_id] == False:
                        if messaging_event["postback"]["payload"] == "Game Time":
                            gametime(sender_id)
                            block(sender_id)
                        elif messaging_event["postback"]["payload"] == "Server stats":
                            serversstats(sender_id)
                            block(sender_id)
                        elif messaging_event["postback"]["payload"] == "Convoy list":
                            convoylist(sender_id,1,3,1)
                            block(sender_id)
                        elif messaging_event["postback"]["payload"] == "streampreview":
                            gettwitch(sender_id)
                            block(sender_id)
                        elif messaging_event["postback"]["payload"] == "info":
                            getinformation(sender_id)
                            block(sender_id)
                        elif messaging_event["postback"]["payload"] == "start":
                            welcome(sender_id)
                            block(sender_id)
                    else:
                        send_message(sender_id,"Please wait some seconds.")
    return "ok", 200



def block(msg):
    global usersblocked
    usersblocked[msg] = True
    timer = Timer(3, unblock, args=(msg,))
    timer.start()

def unblock(msg):
    global usersblocked
    usersblocked[msg] = False

def gametime(msg): # function that send gametime
    time = urllib.urlopen("http://api.truckersmp.com/v2/game_time")
    time1 = time.read()
    gametime1 = json.loads(time1)
    error = gametime1["error"]
    if error == False:
        time12 = gametime1["game_time"]
        message = "Time on servers of TruckersMP ➡ "
        mintot = time12 - 1
        settimanetot = mintot / 10080.00000000 
        settimanetot1 = int(settimanetot)
        settimanefinale = settimanetot - settimanetot1
        giornitot = settimanefinale*7.00000000 
        giornitot1 = int(giornitot)
        if giornitot1 == 0:
            message += "Monday"+" "
        elif giornitot1 == 1:
            message += "Tuesday"+" "
        elif giornitot1 == 2:
            message += "Wednesday"+" "
        elif giornitot1 == 3:
            message += "Thursday"+" "
        elif giornitot1 == 4:
            message += "Friday"+" "
        elif giornitot1 == 5:
            message += "Saturday"+" "
        elif giornitot1 == 6:
            message += "Sunday"+" "
        giornifinale = giornitot- giornitot1
        oretot = giornifinale*24.00000000 
        oretot1 = int(oretot)
        message += str(oretot1)+":"
        orefinale= oretot - oretot1
        minutitot= orefinale*60
        if int(minutitot) == 0 or int(minutitot) == 1 or int(minutitot) == 2 or int(minutitot) == 3 or int(minutitot) == 4 or int(minutitot) == 5 or int(minutitot) == 6 or int(minutitot) == 7 or int(minutitot) == 8 or int(minutitot) == 9:
            message += "0" + str(int(minutitot))
        else:
            message += str(int(minutitot))
        if oretot1 == 18 or oretot1 == 19 or oretot1 == 20 or oretot1 == 21 or oretot1 == 22 or oretot1 == 23 or oretot1 == 24 or oretot1 == 0 or oretot1 == 1 or oretot1 == 2 or oretot1 == 3 or oretot1 == 4 or oretot1 == 5 or oretot1 == 6:
            message += "\n"+"🌃 It's night so please keep lights on 💡"
    else:
        message = "An error occurred."
    send_message(msg, message)

def welcome(msg):
    send_message(msg,"Welcome. Use the menu to select the thing you want to know.")
    with open("facebookdata.txt","a") as file: #remember to create facebookdata.txt with your id
        file.write(","+str(msg))

def globalmessage(text):
    file = open("facebookdata.txt")
    list0 = file.read()
    list1 = list0.split(",")
    textof = text.replace("Your Token","") # if bot receive a message with this token, the message will be sent to all users tha use the bot
    for idsa in list1:
        send_message(int(idsa),textof)

def convoylist(msg,start,end,num): #function that create and send convoys lists
    lista = urllib.urlopen("http://ets2c.com/")
    lista1 = lista.read()
    soup = BeautifulSoup(lista1, "lxml" )
    lista2 = soup.find_all("div", class_="row")[start:end]
    liste = []
    link1 = []
    for i in range(0,2):
        testopreso1 = lista2[i].getText()
        testopreso2 = testopreso1.encode("utf-8")
        listaelaborata = testopreso2.split("\n")
        liste.append(listaelaborata)
        i += 1
    for link in soup.find_all('a')[start+11:end+11]:
        link1.append(link.get('href'))
    message = "Server: " + liste[0][1] + "\n- Time: " + liste[0][2] + "\n- Location: " + liste[0][3] + "\n- Organiser: " + liste[0][4] + "\n- Language: " + liste[0][5] + "\n- Participants: " + liste[0][6] + "\n\n"
    message += "Server: " + liste[1][1] + "\n- Time: " + liste[1][2] + "\n- Location: " + liste[1][3] + "\n- Organiser: " + liste[1][4] + "\n- Language: " + liste[1][5] + "\n- Participants: " + liste[1][6]
    data = json.dumps({"recipient":{"id":msg},"message":{"attachment":{"type":"template","payload":{"template_type":"button","text":message,"buttons":[{"type":"web_url","url":"http://ets2c.com/" + link1[0],"title":"1st c. - More Info"},{"type":"web_url","url":"http://ets2c.com/" + link1[1],"title":"2nd c. - More Info"}]}}}})
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    page = ["1","2","3","4","5","6"]
    for it in page:
        if int(it) == num:
            page[int(it)-1] = "< "+it+" >"
    data = json.dumps({"recipient":{"id":msg},"message":{"text":"Other page:","quick_replies":[{"content_type":"text","title":page[0],"payload":"Convoy list"},{"content_type":"text","title":page[1],"payload":"Page2CL"},{"content_type":"text","title":page[2],"payload":"Page3CL"},{"content_type":"text","title":page[3],"payload":"Page4CL"},{"content_type":"text","title":page[4],"payload":"Page5CL"},{"content_type":"text","title":page[5],"payload":"Page6CL"}]}})
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    
def serversstats(msg): # function that send servers stats
    response = urllib.urlopen("http://api.truckersmp.com/v2/servers")
    html1 = response.read()
    html = json.loads(html1)
    poemi = html.get("response")
    inviareprimo = []
    for i in range(0,10):
        try:
            temp = {}
            if "Europe 1" in poemi[i]["name"]:
                if "ETS2" in poemi[i]["game"]:
                    if poemi[i]["online"] == True:
                        temp["title"] = "Server "+poemi[i]["name"]+"("+poemi[i]["game"]+") is online"
                        temp["image_url"] = "http://i.imgur.com/YV0CygI.jpg"
                        temp["subtitle"] = "There are "+str(poemi[i]["players"])+" players of "+str(poemi[i]["maxplayers"])
                        if poemi[i]["speedlimiter"] == 1:
                            temp["subtitle"] += "\nRemember: In this server is there is the speed limiter of 110 km/h"
                    else:
                        temp["title"] = "Server is offline"
                        temp["image_url"] = "http://i.imgur.com/YV0CygI.jpg"
                        temp["subtitle"] = "Try again later"
                else:
                    if poemi[i]["online"] == True:
                        temp["title"] = "Server "+poemi[i]["name"]+"("+poemi[i]["game"]+") is online"
                        temp["image_url"] = "http://i.imgur.com/liYpSXl.jpg"
                        temp["subtitle"] = "There are "+str(poemi[i]["players"])+" players of "+str(poemi[i]["maxplayers"])
                        if poemi[i]["speedlimiter"] == 1:
                            temp["subtitle"] += "\nRemember: In this server is there is the speed limiter of 67 mph"
                    else:
                        temp["title"] = "Server is offline"
                        temp["image_url"] = "http://i.imgur.com/liYpSXl.jpg"
                        temp["subtitle"] = "Try again later"
            elif "Europe 2" in poemi[i]["name"]:
                if "ETS2" in poemi[i]["game"]:
                    if poemi[i]["online"] == True:
                        temp["title"] = "Server "+poemi[i]["name"]+"("+poemi[i]["game"]+") is online"
                        temp["image_url"] = "http://i.imgur.com/DoIavyJ.jpg"
                        temp["subtitle"] = "There are "+str(poemi[i]["players"])+" players of "+str(poemi[i]["maxplayers"])
                        if poemi[i]["speedlimiter"] == 1:
                            temp["subtitle"] += "\nRemember: In this server is there is the speed limiter of 110 km/h"
                    else:
                        temp["title"] = "Server is offline"
                        temp["image_url"] = "http://i.imgur.com/DoIavyJ.jpg"
                        temp["subtitle"] = "Try again later"
                else:
                    if poemi[i]["online"] == True:
                        temp["title"] = "Server "+poemi[i]["name"]+"("+poemi[i]["game"]+") is online"
                        temp["image_url"] = "http://i.imgur.com/MpcDqPD.jpg"
                        temp["subtitle"] = "There are "+str(poemi[i]["players"])+" players of "+str(poemi[i]["maxplayers"])
                        if poemi[i]["speedlimiter"] == 1:
                            temp["subtitle"] += "\nRemember: In this server is there is the speed limiter of 67 mph"
                    else:
                        temp["title"] = "Server is offline"
                        temp["image_url"] = "http://i.imgur.com/MpcDqPD.jpg"
                        temp["subtitle"] = "Try again later"
            elif "Europe 3" in poemi[i]["name"]:
                if "ETS2" in poemi[i]["game"]:
                    if poemi[i]["online"] == True:
                        temp["title"] = "Server "+poemi[i]["name"]+"("+poemi[i]["game"]+") is online"
                        temp["image_url"] = "http://i.imgur.com/ep5e8zb.jpg"
                        temp["subtitle"] = "There are "+str(poemi[i]["players"])+" players of "+str(poemi[i]["maxplayers"])
                        if poemi[i]["speedlimiter"] == 1:
                            temp["subtitle"] += "\nRemember: In this server is there is the speed limiter of 110 km/h"
                    else:
                        temp["title"] = "Server is offline"
                        temp["image_url"] = "http://i.imgur.com/ep5e8zb.jpg"
                        temp["subtitle"] = "Try again later"
                else:
                    serverunknowed(poemi,i)
            elif "United States" in poemi[i]["name"]:
                if "ETS2" in poemi[i]["game"]:
                    if poemi[i]["online"] == True:
                        temp["title"] = "Server "+poemi[i]["name"]+"("+poemi[i]["game"]+") is online"
                        temp["image_url"] = "http://i.imgur.com/BH23Gsr.jpg"
                        temp["subtitle"] = "There are "+str(poemi[i]["players"])+" players of "+str(poemi[i]["maxplayers"])
                        if poemi[i]["speedlimiter"] == 1:
                            temp["subtitle"] += "\nRemember: In this server is there is the speed limiter of 110 km/h"
                    else:
                        temp["title"] = "Server is offline"
                        temp["image_url"] = "http://i.imgur.com/BH23Gsr.jpg"
                        temp["subtitle"] = "Try again later"
                else:
                    if poemi[i]["online"] == True:
                        temp["title"] = "Server "+poemi[i]["name"]+"("+poemi[i]["game"]+") is online"
                        temp["image_url"] = "http://i.imgur.com/UZCieAX.jpg"
                        temp["subtitle"] = "There are "+str(poemi[i]["players"])+" players of "+str(poemi[i]["maxplayers"])
                        if poemi[i]["speedlimiter"] == 1:
                            temp["subtitle"] += "\nRemember: In this server is there is the speed limiter of 67 mph"
                    else:
                        temp["title"] = "Server is offline"
                        temp["image_url"] = "http://i.imgur.com/UZCieAX.jpg"
                        temp["subtitle"] = "Try again later"
            elif "Hong Kong" in poemi[i]["name"]:
                if "ETS2" in poemi[i]["game"]:
                    if poemi[i]["online"] == True:
                        temp["title"] = "Server "+poemi[i]["name"]+"("+poemi[i]["game"]+") is online"
                        temp["image_url"] = "http://i.imgur.com/763orz5.jpg"
                        temp["subtitle"] = "There are "+str(poemi[i]["players"])+" players of "+str(poemi[i]["maxplayers"])
                        if poemi[i]["speedlimiter"] == 1:
                            temp["subtitle"] += "\nRemember: In this server is there is the speed limiter of 110 km/h"
                    else:
                        temp["title"] = "Server is offline"
                        temp["image_url"] = "http://i.imgur.com/763orz5.jpg"
                        temp["subtitle"] = "Try again later"
                else:
                    temp = serverunknowed(poemi,i)
            elif "South America" in poemi[i]["name"]:
                if "ETS2" in poemi[i]["game"]:
                    if poemi[i]["online"] == True:
                        temp["title"] = "Server "+poemi[i]["name"]+"("+poemi[i]["game"]+") is online"
                        temp["image_url"] = "http://i.imgur.com/R65VnAM.jpg"
                        temp["subtitle"] = "There are "+str(poemi[i]["players"])+" players of "+str(poemi[i]["maxplayers"])
                        if poemi[i]["speedlimiter"] == 1:
                            temp["subtitle"] += "\nRemember: In this server is there is the speed limiter of 110 km/h"
                    else:
                        temp["title"] = "Server is offline"
                        temp["image_url"] = "http://i.imgur.com/R65VnAM.jpg"
                        temp["subtitle"] = "Try again later"
                else:
                    temp = serverunknowed(poemi,i)
            else:
                temp = serverunknowed(poemi,i)
            inviareprimo.append(temp)
            i += 1
        except (KeyError,IndexError) as e:
            break
    data = json.dumps({"recipient":{"id":msg},"message":{"attachment":{"type":"template","payload":{"template_type":"generic","elements":inviareprimo}}}})
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def serverunknowed(poemi,i): #function that create servers stats of unknowed servers
    temp = {}
    if "ETS2" in poemi[i]["game"]:
        if poemi[i]["online"] == True:
            temp["title"] = "Server "+poemi[i]["name"]+" is online"
            temp["image_url"] = "http://i.imgur.com/2zWXZDM.jpg"
            temp["subtitle"] = "There are "+str(poemi[i]["players"])+" of "+str(poemi[i]["maxplayers"])
            if poemi[i]["speedlimiter"] == 1:
                temp["subtitle"] += "\nRemember: In this server is there is the speed limiter of 110 km/h"
        else:
            temp["title"] = "Server "+poemi[i]["name"]+" is offline"
            temp["image_url"] = "http://i.imgur.com/2zWXZDM.jpg"
            temp["subtitle"] = "Try again later."
    else:
        if poemi[i]["online"] == True:
            temp["title"] = "Server "+poemi[i]["name"]+" is online"
            temp["image_url"] = "http://i.imgur.com/YL8ji9O.jpg"
            temp["subtitle"] = "There are "+str(poemi[i]["players"])+" of "+str(poemi[i]["maxplayers"])
            if poemi[i]["speedlimiter"] == 1:
                temp["subtitle"] += "\nRemember: In this server is there is the speed limiter of 67 mph"
        else:
            temp["title"] = "Server "+poemi[i]["name"]+" is offline"
            temp["image_url"] = "http://i.imgur.com/YL8ji9O.jpg"
            temp["subtitle"] = "Try again later."
    return temp

def gettwitch(msg): #function that send stream preview
    response = urllib.urlopen("https://api.twitch.tv/kraken/streams/kat_pw")
    response1 = response.read()
    response2 = json.loads(response1)
    if response2.get("stream") == None:
        send_message(msg, "⚠" +  " Stream is offline now")
    else:
        data = json.dumps({"recipient":{"id":msg},"message":{"attachment":{"type":"image","payload":{"url":"https://static-cdn.jtvnw.net/previews-ttv/live_user_kat_pw-1280x720.jpg"}}}})
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def getinformation(msg): #function that send info
    message = "Bot created by @EdoardoGrassiXYZ (http://telegram.me/EdoardoGrassiXYZ)\n"
    message += "🔹" + "Bot version: 0.1\n"
    response = urllib.urlopen("https://api.truckersmp.com/v2/version")
    stringa = response.read()
    html = json.loads(stringa)
    message += "🔹" + "TruckersMP mod version: " + html.get("name").encode("utf-8") + " " + html.get("stage").encode("utf-8") + " \n"
    message += "🔹" + "ETS2 version supported: " + html.get("supported_game_version").encode("utf-8") + "\n"
    message += "🔹" + "ATS version supported: " + html.get("supported_ats_game_version").encode("utf-8")
    send_message(msg, message)

def send_message(recipient_id, message_text): #general function to send message
    data = json.dumps({"recipient": {"id": recipient_id},"message": {"text": message_text}})
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

if __name__ == '__main__':
    app.run(debug=True)
