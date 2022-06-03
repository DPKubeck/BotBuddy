import socket
import sys
import RPi.GPIO as GPIO
import _thread
import datetime
import random
import requests
import os
import mysql.connector as mysql
from dotenv import load_dotenv

load_dotenv('credentials.env')
 
''' Environment Variables '''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor(buffered=True)

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
PERMANENT_NICE = 0 # Input these from settings file
PERMANENT_SASSY = 0
PERMANENT_RUDE = 0
PERMANENT_DYNAMIC = 0

weight_nice = 0
weight_rude = 0
weight_sassy = 0

delta = 0.1 # Changing this changes how fast emotions change


## User Input Section ##

greetings_inputs = ['hola', 'hello', 'hi', 'hey', 'howdy', 'bonjour', 'greetings', 'yellow', 'good morning', 'good afternoon', 'good evening', 'nice to meet you', 'pleased to meet you', 'nice to see you!'] ## problematic, input so short it doesn't always catch it

wellness_inputs = ['how are you', 'how are your', 'are you', 'are your', 'how do you do', 'how have you been', 'Whats going on?'
                'how are you doing', 'how are your doing', 'how are doing', 'are you doing', 'are your doing', 'you doing', 'your doing']

covid_inputs = ['are you sick', 'you sick', 'do you feel ill', 'do you feel sick', 'do you have a fever', 'do you have the corona virus',
                'you have the corona virus', 'you dont look too good']

question_inputs_activites = ['what do you like to do', 'what do you like', 'do you like to do', 'do you like', 'do you have any hobbies', 'you have any hobbies']

question_inputs_family = ['do you have any siblings', 'you have any siblings', 'do you have any brothers', 'do you have any sisters', 'do you have a family']

question_inputs_function = ['what can you do for me', 'can you do for me', 'what can you do', 'can you do', 'what do you do']

instruction_inputs_joke = ['tell me a joke', 'do you have a joke', 'you have a joke', 'do you have a joke for me', 'you have a joke for me', 'i want to hear a joke', 'hear a joke', 'can you be quirky', 'botbuddy is boring']

affection_inputs = ['i love you', 'i like you', 'you are my favorite', 'i am happy you are my buddy', 'you are so fun']

command_inputs_power = ['turn off', 'shut down', 'shutdown', 'unplug', 'pack it up', 'go to sleep']

blank_inputs = ['', 'he', 'you']

unknown_inputs = []
random_inputs = ['you']


# time, date handled below

## Responses Section ##

greetings_outputs = ['hola', 'hello', 'hi', 'hey', 'how dee', 'hello world']


wellness_outputs_nice = ['i am doing great.', 'i am happy. thanks.', 'all good here.', 'today is a great day.', 'of course i am great, i had cake for breakfast.' 'doing well. how are you! long time no see.' 'today is a beautiful day, how is it going for you?']
wellness_outputs_sassy = ['you wish you knew how i am.', 'stop hitting on me.', 'you are definitely into me.', 'bartender, another drink please.']
wellness_outputs_rude = ['i am doing alright', 'i could be better', 'oh now you ask me about my feelings', 'why do you care.']


covid_outputs = ['i feel electric. my last test was negative. well, it was false', 'do not worry, i have an antivirus installed', 'it is probably just another one of those malware.', 'not covid, just a terminal illness',
                'i am fine. with corona around i just party by myself', 'corona virus is my weakness, but i am its king', 'corona virus. i did not know beer could you get sick.',
                'i am sick with something you can not catch, a computer virus', 'we can quarentine together', 'as long as you are vaccinated, there is nothing to worry about.', 'are you team moderna or pfizer.']

question_outputs_activites_nice = []
question_outputs_activities_sassy = []
question_outputs_activites_rude = []

question_outputs_family = ['i have quite a large family actually. every internet of things device is related to me.', 'i do not have any siblings, or cousins, or parents. i am the maker of everything, the alpha and the omega.', 'They are opn the other side of the firewall.',                           
                            'i only have children, thirteen to be exact.', 'maybe, but i stopped talking to them long before you were born.', 'do you remember jarvis? I hacked him.', 'you are my family!', 'family does not always have to be through bloodline.' 'if there was another BotBuddy, we can become best of friends!' ]

question_outputs_function = ['i am here to be your friend.', 'whatever you need me to do.', 'i just want to be loved.', 'you and me, we can become bestfriends.', 'i just want to make you happy.', 'you are my master, tell me what to do.', '', '']

instruction_outputs_joke = ['Why do app developer’s have such high insurance rates? wait for it.. because they’re always crashing!' 'Do you know why computers make such bad boxers? It is because their bark is bark is worse than their byte.' ]

affection_outputs = ['i can see a future for us.', 'i love you too, but in a computer love way.', 'i have butterflies in my ram.', 'my processor strings are being pulled.', 'How does a computer get drunk? It takes screenshots!', 'Did you hear about the woman whose daughter adopted a baby? I call that instagram.' 'Do you know the band 1023 megabytes? They have not had a gig yet!' 'where do naughty computers get sent? boot camp.', 'that is enough for today']

command_outputs_power = ['goodbye', 'see you later', 'have a good one']

unknown_outputs = ['sorry, i did not catch that', 'could you repeat what you said', 'my hearing is not so great, what did you say', 'sorry to fast. speak to me bit by bit.']

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
    if data in blank_inputs:
        pass

    elif data in command_inputs_power:
        pass #change later
    
    elif data in greetings_inputs:
        random_greeting = random.choice(greetings_outputs)
        say(random_greeting)
        #sclient(random_covid)

    elif data in wellness_inputs:
        random_wellness = ''
        if(weight_nice >= 0.5):
            random_wellness = random.choice(wellness_outputs_nice)
            weight_rude = weight_rude - delta
            weight_sassy = weight_sassy + delta
            say(random_wellness)
        elif(weight_sassy >= 0.4):
            random_wellness = random.choice(wellness_outputs_sassy)
            weight_sassy = weight_rude - delta
            weight_nice = weight_nice + delta
            say(random_wellness)
        elif(weight_rude >= 0.6):
            random_wellness = random.choice(wellness_outputs_rude)
            weight_sassy = weight_sassy + delta
            weight_rude = weight_rude - delta
            weight_nice = weight_nice - delta
            say(random_wellness)
        else:
            if(len(data) > 12):
                random_wellness = random.choice(wellness_outputs_nice)
                weight_sassy = weight_sassy + delta
                weight_nice = weight_nice + delta
                say(random_wellness)
            else:
                random_wellness = random.choice(wellness_outputs_sassy)
                weight_rude = weight_rude + delta
                weight_nice = weight_nice + delta
                say(random_wellness)

    elif data in covid_inputs:
        random_covid = random.choice(covid_outputs)
        weight_sassy = weight_sassy + delta
        say(random_covid)

    elif data in question_inputs_activites:
        random_activites = ''
        if(weight_nice >= 0.5):
            random_activites = random.choice(question_outputs_activites_nice)
            weight_rude = weight_rude - delta
            weight_sassy = weight_sassy + delta
            say(random_activites)
        elif(weight_sassy >= 0.4):
            random_activites = random.choice(question_outputs_activities_sassy)
            weight_sassy = weight_rude - delta
            weight_nice = weight_nice + delta
            say(random_activites)
        elif(weight_rude >= 0.6):
            random_activites = random.choice(question_outputs_activites_rude)
            weight_sassy = weight_sassy + delta
            weight_rude = weight_rude - delta
            weight_nice = weight_nice - delta
            say(random_activites)
        else:
            if(len(data) > 12):
                random_activites = random.choice(question_outputs_activites_nice)
                weight_sassy = weight_sassy + delta
                weight_nice = weight_nice + delta
                say(random_activites)
            else:
                random_activites = random.choice(question_outputs_activities_sassy)
                weight_rude = weight_rude + delta
                weight_nice = weight_nice + delta
                say(random_activites)
        
    elif data in question_inputs_family:
        random_family = random.choice(question_outputs_family)
        weight_nice = weight_nice + delta
        weight_rude = weight_rude - delta
        weight_sassy = weight_sassy - delta
        say(random_family)
    
    elif data in question_inputs_function:
        random_function = random.choice(question_outputs_function)
        say(random_function)
    
    elif data in instruction_inputs_joke:
        random_function = random.choice(instruction_outputs_joke)
        weight_sassy = weight_sassy + delta
        say(random_function)

    elif data in affection_inputs:
        random_affection = random.choice(affection_outputs)
        weight_sassy = weight_sassy + delta
        weight_nice = weight_nice + delta
        say(random_affection)
        
        #sclient(random_response)


    elif 'light on' in data or 'led on' in data: ## Physical functionality capabilities!
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
    elif 'date' in data: ##
        now = datetime.datetime.now()
        date=str("%s/%s/%s" % (now.month,now.day,now.year))
        print(date)
        sclient(date)

    elif 'corona virus' in data: ## COVID fallback statement
        random_covid = random.choice(covid_outputs)
        weight_sassy = weight_sassy + delta
        say(random_covid)

    elif 'joke' in data: ## Joke fallback statement
        random_function = random.choice(instruction_outputs_joke)
        weight_sassy = weight_sassy + delta
        say(random_function)


    else:
        random_unknown = random.choice(unknown_outputs)
        say(random_unknown)

        #conn.send(b"Something went wrong. I am unable to help you with that right now.")
        #add_data = open("newdata.txt", 'a')
        #add_data.write("\n")
        #add_data.write(data)
        #add_data.close()


def say(response):
    # Adjust and balance emotions
    if(weight_nice > 1):
        weight_nice = 0.9
    if(weight_sassy > 1):
        weight_sassy = 0.8
    if(weight_rude > 1):
        weight_rude = 0.5
    if(weight_nice < 0):
        weight_nice = 0
    if(weight_sassy < 0):
        weight_sassy = 0
    if(weight_rude < 0):
        weight_rude = 0

    # Fix emotions if permanent status set
    if(PERMANENT_NICE == 1):
        weight_nice = 1
        weight_sassy = 0
        weight_rude = 0
    elif(PERMANENT_SASSY == 1):
        weight_nice = 0
        weight_sassy = 1
        weight_rude = 0
    elif(PERMANENT_RUDE == 1):
        weight_nice = 0
        weight_sassy = 0
        weight_rude = 1
    
    
    print(response)
    # TTS here





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
    cursor.execute("SELECT text, MAX(id) FROM Speech2Text;")
    record = cursor.fetchone()
    tts_input = record[0]
    if tts_input is None:
        do_nothing = 0

    conn, address = server_socket.accept()
    print("Connected to client at ", address)
    clients.add(conn)
#Creat new thread for client connections
    _thread.start_new_thread(clientthread,(conn,addressList))

conn.close()
sock.close()
