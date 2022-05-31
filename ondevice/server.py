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

## Emotion Weights Initialization ##
weight_happy = 0
weight_sad = 0
weight_sassy = 0
weight_mean = 0


## User Input Section ##

greetings_inputs = ['hola', 'hello', 'hi', 'hey', 'howdy', 'bonjour'] ## problematic, input so short it doesn't always catch it

wellness_inputs = ['how are you', 'how are your', 'are you', 'are your',
                'how are you doing', 'how are your doing', 'how are doing', 'are you doing', 'are your doing', 'you doing', 'your doing']

covid_inputs = ['are you sick', 'you sick', 'do you feel ill', 'do you feel sick', 'do you have a fever', 'do you have the corona virus',
                'you have the corona virus']

question_inputs_activites = ['what do you like to do', 'what do you like', 'do you like to do', 'do you like', 'do you have any hobbies', 'you have any hobbies']

question_inputs_family = ['do you have any siblings', 'you have any siblings', 'do you have any brothers', 'do you have any sisters', 'do you have a family']

question_inputs_function = ['what can you do for me', 'can you do for me', 'what can you do', 'can you do']

instruction_inputs_joke = ['tell me a joke', 'do you have a joke', 'you have a joke', 'do you have a joke for me', 'you have a joke for me']

affection_inputs = ['i love you', 'i like you', 'you are my favorite']

random_inputs = ['you']

unknown_inputs = []

# time, date handled below

## Responses Section ##

greetings_outputs = ['hola', 'hello', 'hi', 'hey', 'howdy', 'bonjour']


wellness_outputs_happy = ['i am doing great', 'i am happy. thanks', 'all good here', 'today is a great day', 'of course i am great, i had cake for breakfast']
wellness_outputs_sad = ['i am doing alright', 'i could be better', '']
wellness_outputs_sassy = ['you wish you knew how i am', 'stop hitting on me', 'you are definitely into me', 'bartender, another drink please']
wellness_outputs_mean = ['oh now you ask me about my feelings']

covid_outputs = ['i feel electric. my last test was negative. well, it was false', 'do not worry, i have an antivirus installed',
                'i am fine. with corona around i just party by myself', 'corona virus is my weakness, but i am its king', 'corona virus. i did not know beer could get sick',
                'i am sick with something you can not catch, a computer virus']


question_outputs_activites = []
question_outputs_family = ['i have quite a large family actually. every internet of things device is related to me', 'i dont have any siblings, or cousins, or parents. i am the maker of everything, the alpha and the omega',
                            'i only have children, thirteen to be exact', 'maybe, but i stopped talking to them long before you were born']
question_outputs_function = []

instruction_outputs_joke = []

affection_outputs = ['i can see a future for us', 'i love you too, but in a computer love way', 'i have butterflies in my ram', 'my processor strings are being pulled']

database={
    'botbuddy':'hello,sir how can i help you',
    'name':'botbuddy',
    'what is your name':'my name is botbuddy',
    'hello botbuddy':'hello OWNER_NAME how can i help you',
    'what can you do for me':'i can do many things..'
}

print("Listening for client ..........")

## Chat code processing ##
def chatback(data):
    ## Direct input-to-response section
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

    ## Indirect response finder section
    elif 'time' in data:
        now = datetime.datetime.now()
        time=str(now.hour)+":"+str(now.minute)
        print(time)
        sclient(time)
    elif 'date'in data: ##
        now = datetime.datetime.now()
        date=str("%s/%s/%s" % (now.month,now.day,now.year))
        print(date)
        sclient(date)
    elif 'corona virus' in data: ## COVID fallback statement
        print()
    elif 'joke' in data: ## Joke fallback statement
        print()
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
