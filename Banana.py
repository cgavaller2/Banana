import socket, time, threading, pyttsx3, pigpio, os, pygame, random, lcddriver, datetime
from Settings import *
from Data import *
from PhoneticAPI import *
from datetime import datetime
os.system("sudo pigpiod")
time.sleep(.5)
HOST = "irc.chat.twitch.tv"
PORT = 6667
recentmsg = ""
mouthStatus = 0
pi = pigpio.pi()
engine = pyttsx3.init()
display = lcddriver.lcd()
now = datetime.now()
pygame.mixer.init()
engine.setProperty('rate', 140)
engine.setProperty('volume', 2)
engine.setProperty('voice', 'english+m3')
pi.set_servo_pulsewidth(27, 850)

def music():
    song = 1
    while True:
        pygame.mixer.music.load(str(song)+'.wav')
        pygame.mixer.music.play()
        time.sleep(180)
        pygame.mixer.music.fadeout(4000)
        time.sleep(15)
        if song == 2:
            song = 0
        song = song+1
        
def dance():
    print("Dancing Function Loaded.")
    while True:
        time.sleep(1.25)
        if mouthStatus == 1:
            pi.set_servo_pulsewidth(27, 850)
        else:
            pi.set_servo_pulsewidth(27, 700)
            time.sleep(1.25)
            if mouthStatus == 1:
                pi.set_servo_pulsewidth(27, 850)
            else:
                pi.set_servo_pulsewidth(27, 1000)

def ping():
    print("Pinging Started.")
    while True:
        time.sleep(60)
        s.send(bytes("PONG :tmi.twitch.tv\r\n", "UTF-8"))
        print("PING Sent.")

def send_message(msg):
    s.send(bytes("PRIVMSG #" + CHANNEL + " :" + msg + "\r\n", "UTF-8"))

def mouth(mouthOpen):
    if mouthOpen == 1:
        mouthStatus = 1
        pi.set_servo_pulsewidth(22, 1250)
        return
    else:
        if mouthOpen == 0:
            mouthStatus = 0
            pi.set_servo_pulsewidth(22, 2000)
            return

def warn():
    print(username + ', Has been warned for saying a blacklisted word!')
    warned.append(username)
    send_message(username + ", Don't say that again or you will be perm-banned!")
    for x in range(0, 10):
        send_message("/tempban " + username + " 240")
    return

def ban():
    print(username + ', Has been banned for saying a blacklisted word multiple times!')
    banned.append(username)
    for x in range(0, 10):
        send_message("/ban " + username)
    return

def say(talk):
    print(username + " said: " + message)
    api_reply = api_request(APIKEY, talk, ['nigger','nigga','faggot','fag','nicker','nigur','monkey','gurney'])
    if debug == True:
        print(api_reply)
    code = api_reply['code']
    if code == 1 and not '*' in talk: 
        print('Message is clean!')
        pygame.mixer.music.pause()
        time.sleep(.3)
        mouth(1)
        time.sleep(.5)
        engine.say(talk)
        engine.runAndWait()
        mouth(0)
        pygame.mixer.music.unpause()
        time.sleep(3)
    else:
        print('Bad word detected!')
        if username in warned and ban_on_badword == True:
            ban()
        else:
            if warn_on_badword == True:
                warn()

print("Connecting to host.")
s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + CHANNEL + " \r\n", "UTF-8"))
print("connected to host")

checkdelay = threading.Thread(target=ping)
music = threading.Thread(target=music)
dancing = threading.Thread(target=dance)
music.start()
checkdelay.start()
dancing.start()
time.sleep(1)

while True:
    for line in str(s.recv(1024)).split('\\r\\n'):
        parts = line.split(':')
        if len(parts) < 3:
            continue

        message = parts[2][:len(parts[2])]
        usernamesplit = parts[1].split("!")
        username = usernamesplit[0]
        if debug == True:
            print(time.strftime("%H:%M:%S"), username + ": " + message)
        if recentmsg == message:
            break
        else:
            recentmsg = message
            mouthStatus = 1
            time.sleep(.2)
            display.lcd_display_string(username, 1)
            say(message)
            mouthStatus = 0
            display.lcd_clear()
            
            break
