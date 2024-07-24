# import pyrebase
# import keyboard
# # import RPi.GPIO as GPIO

# # GPIO.setmode(GPIO.BOARD)

# config = {
#   "apiKey": "AIzaSyBLJURU5ZIcqswOnRIbWOVgxNztmP6qdro",
#   "authDomain": "toggle-button-4087f.firebaseapp.com",
#   "databaseURL": "https://toggle-button-4087f-default-rtdb.firebaseio.com",
#   "projectId": "toggle-button-4087f",
#   "storageBucket": "toggle-button-4087f.appspot.com",
#   "messagingSenderId": "441033032973",
#   "appId": "1:441033032973:web:98bae899e594302dc55c44",
#   "measurementId": "G-CBSWK5B3Y5"
# };

# firebase = pyrebase.initialize_app(config)
# database = firebase.database()


# Pin_Motor_1 = 1
# Pin_Motor_2 = 2
# Pin_Motor_3 = 3
# Pin_Motor_4 = 4

# Pin_Light_1 = 5
# Pin_Light_2 = 6
# Pin_Light_3 = 7
# Pin_Light_4 = 8
# Pin_Light_5 = 9

# # GPIO.setup(Pin_Motor_1, GPIO.OUT)
# # GPIO.setup(Pin_Motor_2, GPIO.OUT)
# # GPIO.setup(Pin_Motor_3, GPIO.OUT)
# # GPIO.setup(Pin_Motor_4, GPIO.OUT)

# # GPIO.setup(Pin_Light_1, GPIO.OUT)
# # GPIO.setup(Pin_Light_2, GPIO.OUT)
# # GPIO.setup(Pin_Light_3, GPIO.OUT)
# # GPIO.setup(Pin_Light_4, GPIO.OUT)
# # GPIO.setup(Pin_Light_5, GPIO.OUT)

# while True:
#     data = database.get()

#     for user in data.each():
#         print(user.key(), user.val())
#         # LED 1
#         if user.key()=="L1" and user.val()=="1":
#             print("-----------------------------------------------------------")
#             print("L1: 1")
#             # GPIO.output(Pin_Light_1, True)
#         elif user.key()=="L1" and user.val()=="0":
#             print("-----------------------------------------------------------")
#             print("L1: 0")
#             # GPIO.output(Pin_Light_1, False)
            
#         # LED 2
#         if user.key()=="L2" and user.val()=="1":
#             print("-----------------------------------------------------------")
#             print("L2: 1")
#             # GPIO.output(Pin_Light_2, True)
        
#         elif user.key()=="L2" and user.val()=="0":
#             print("-----------------------------------------------------------")
#             print("L2: 0")
#             # GPIO.output(Pin_Light_2, False)

#         # LED 3
#         if user.key()=="L3" and user.val()=="1":
#             print("-----------------------------------------------------------")
#             print("L3: 1")
#             # GPIO.output(Pin_Light_3, True)
        
#         elif user.key()=="L3" and user.val()=="0":
#             print("-----------------------------------------------------------")
#             print("L3: 0")
#             # GPIO.output(Pin_Light_3, False)
        
#         # LED 4
#         if user.key()=="L4" and user.val()=="1":
#             print("-----------------------------------------------------------")
#             print("L4: 1")
#             # GPIO.output(Pin_Light_4, True)
        
#         elif user.key()=="L4" and user.val()=="0":
#             print("-----------------------------------------------------------")
#             print("L4: 0")
#             # GPIO.output(Pin_Light_4, False)
        
#         # LED 5
#         if user.key()=="L5" and user.val()=="1":
#             print("-----------------------------------------------------------")
#             print("L5: 1")
#             # GPIO.output(Pin_Light_5, True)

#         elif user.key()=="L5" and user.val()=="0":
#             print("-----------------------------------------------------------")
#             print("L5: 0")
#             # GPIO.output(Pin_Light_5, False)

#     def on_key_event(event):
#         if event.name == 'w':
#             # GPIO.output(Pin_Motor_1, True)
#             # GPIO.output(Pin_Motor_2, False)
#             # GPIO.output(Pin_Motor_3, True)
#             # GPIO.output(Pin_Motor_4, False)
#             print("Forward")

#         if event.name == 's':
#             # GPIO.output(Pin_Motor_1, False)
#             # GPIO.output(Pin_Motor_2, True)
#             # GPIO.output(Pin_Motor_3, False)
#             # GPIO.output(Pin_Motor_4, True)
#             print("Backward")

#         if event.name == 'a':
#             # GPIO.output(Pin_Motor_1, False)
#             # GPIO.output(Pin_Motor_2, False)
#             # GPIO.output(Pin_Motor_3, True)
#             # GPIO.output(Pin_Motor_4, False)
#             print("left")
            
#         if event.name == 'd':
#             # GPIO.output(Pin_Motor_1, True)
#             # GPIO.output(Pin_Motor_2, False)
#             # GPIO.output(Pin_Motor_3, False)
#             # GPIO.output(Pin_Motor_4, False)
#             print("right")

#     # Set up the keyboard hook
#     keyboard.on_press(on_key_event)

# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

import RPi.GPIO as GPIO          
from time import sleep

in1 = 24
in2 = 23
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)

p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

while(1):

    x=input()
    
    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='l':
        print("low")
        p.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(75)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")