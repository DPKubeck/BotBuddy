import socket
import sys
import RPi.GPIO as GPIO
import _thread
import datetime
import random
import requests
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)

#Leave host address blank
host = ''
#Set host port
port = 8888
address = (host, port)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(5)
#Variable for the number of connections
numbOfConn = 0

#Name of list used for connections
addressList = []
clients = set()



## Responses Section ##

greetings = ['hola', 'hello', 'hi', 'hey', 'howdy', 'bonjour', 'botbuddy']

wellness_questions = ['how are you', 'how are you doing', 'are you okay', 'how was your day']
wellness_responses = ['i am doing great', 'i am fine. thanks', 'all good here', 'today is a great day']
covid_questions = ['where have you been', 'have you gone out anywhere', 'did you walk around']
covid_answers = ['with corona around i do not dare to keep a foot out', 'corona virus is my weakness']

database={
    'botbuddy':'hello,sir how can i help you',
    'name':'botbuddy',
    'what is your name':'my name is botbuddy',
    'hello botbuddy':'hello,friend how can i help you',
    'what can you do for me':'i can do many things..'
}

print("Listening for client ..........")

## Chat code processing ##
def chatback(data):
    if data in covid_questions:
        random_covid = random.choice(covid_answers)
        print(random_covid)
        sclient(random_covid)
    elif data in wellness_questions:
        random_response = random.choice(wellness_responses)
        print(random_response)
        sclient(random_response)
    elif data in greetings:
        random_greeting = random.choice(greetings)
        print(random_greeting)
        sclient(random_greeting)
    elif 'light on'in data or 'led on' in data: ## Physical functionality capabilities!
        sclient("light turn on")
        GPIO.output(11,True)
        print("Light on")
    elif 'light off' in data or 'led off' in data:
        sclient("light turn off")
        GPIO.output(11,False)
        print("Light Off")
    elif 'time' in data:
        now = datetime.datetime.now()
        time=str(now.hour)+":"+str(now.minute)
        print(time)
        sclient(time)
    elif 'date'in data:
        now = datetime.datetime.now()
        date=str("%s/%s/%s" % (now.month,now.day,now.year))
        print(date)
        sclient(date)
    else:
        conn.send(b"Something went wrong. I am unable to help you with that right now.")
        add_data = open("newdata.txt", 'a')
        add_data.write("\n")
        add_data.write(data)
        add_data.close()

#Send reply
def sclient(mess):
    for c in clients:
        try:
            c.send(mess.encode())
        except:
            c.close()

#Server code
def clientthread(conn,addressList):
     while True:
        output = conn.recv(2048);
        if output.strip() == "disconnect":
            conn.close()
            sys.exit("Received disconnect message.  Shutting down.")
            conn.send("connection loss")
        elif output:
            print("Message received from client:")
            data = output.decode()
            data=str(data).lower()
            print(data)
            print("Reply from the server:")
            chatback(data)

while True:
#Accept connections
    conn, address = server_socket.accept()
    print("Connected to client at ", address)
    clients.add(conn)
#Creat new thread for client connections
    _thread.start_new_thread(clientthread,(conn,addressList))

conn.close()
sock.close()
