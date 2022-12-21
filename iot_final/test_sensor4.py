import sys
import requests
import json
import time
import threading
import numpy as np

temperature=30.0
fan=0
status=0

url_create_ae = 'http://127.0.0.1:8282/~/mn-cse'
url_create_cnt = 'http://127.0.0.1:8282/~/mn-cse/mn-name/' + sys.argv[1]
url_create_con = 'http://127.0.0.1:8282/~/mn-cse/mn-name/' + sys.argv[1] + "/DATA"
url_get_instruction = 'http://127.0.0.1:8282/~/mn-cse/mn-name/' + sys.argv[1] + "/instruction/la"

header_create_ae = {'X-M2M-Origin': 'admin:admin','Content-Type':'application/json;ty=2'}
header_create_cnt = {'X-M2M-Origin': 'admin:admin','Content-Type':'application/json;ty=3'}
header_create_con = {'X-M2M-Origin': 'admin:admin','Content-Type':'application/json;ty=4'}
header_get_instruction = {'X-M2M-Origin': 'admin:admin'}

contentinstence = "<obj> <str name=\"temperature\" val=\"on\"/> </obj>"

body_create_ae = {
   "m2m:ae": {
     "api": "app-sensor",
     "rr": "false",
     "lbl": ["Type/sensor", "Category/temperature", "Location/home"],
     "rn": sys.argv[1]
   }
 }
body_create_cnt_data = {
    "m2m:cnt": {
     "rn": "DATA"
   }
}
body_create_cnt_instruction = {
    "m2m:cnt": {
     "rn": "instruction"
   }
}

body_create_contentinstance = {
    "m2m:cin": {
     "cnf": "message",
     "con": "<obj> <str name=\"temperature\" val=\"" + str(temperature) + "\"/> </obj>"
   }
}

x=requests.post(url_create_ae,headers=header_create_ae,json=body_create_ae)
print(x.text)

y=requests.post(url_create_cnt,headers=header_create_cnt,json=body_create_cnt_data)
print(y.text)

z=requests.post(url_create_cnt,headers=header_create_cnt,json=body_create_cnt_instruction)
print(z.text)

def post_temperature():
    #print(ww)
    #while True:
    global temperature
    global fan
    body_create_contentinstance = {
        "m2m:cin": {
        "cnf": "message",
        "con": "<obj> <str name=\"temperature\" val=\"" + str(temperature) + "\"/> <str name=\"fan\" val=\"" + str(fan) + "\"/> </obj>"
    }
    }
    x = requests.post(url_create_con,headers=header_create_con, json = body_create_contentinstance)
    #print(x.text)
    #time.sleep(2)


def get_instruction():
    global temperature
    global fan
    instruction_id=''
    while True:
        x = requests.get(url_get_instruction,headers=header_get_instruction)
        #print(x.text)
        pos=x.text.find('instruction&quot; val=&quot;')
        lenght= len('instruction&quot; val=&quot;')
        instruction_name_pos = x.text.find('rn="cin_')
        lenght2=len('rn="cin_')
        instruction_name_temp = x.text[instruction_name_pos+lenght2:instruction_name_pos+lenght2+6]
        if instruction_name_temp != instruction_id:
            instruction_id = instruction_name_temp
            #instruction = x.text[pos+lenght:pos+lenght+2]
            instruction = x.text[pos+lenght:pos+lenght+2]
            #print(x.text)
            #print(instruction)
            #fan=int(instruction)
            """if instruction == 'on':
                #mutex.acquire()
                fan='on'
                #temperature = temperature -1 
                #print("on ",temperature)
                #mutex.acquire()
            else:
                fan='off'"""
            if instruction == 'up' and fan !=0:
                if fan < 3:
                    fan = fan +1 
            elif instruction == 'do' and fan !=0:
                if fan > 1 :
                    fan=fan-1
            elif instruction == 'on':
                fan=1
            elif instruction == 'of':
                fan=0
        #print('off',temperature)
        #print(x.text)
        time.sleep(2)

def env():
    global temperature
    global fan
    global status
    while True:
        if status == 1:
            temperature=temperature+0.5
        elif status == 0:
            temperature=temperature
        if fan == 1:
            temperature=temperature-0.4
            temperature = round(temperature, 1)
            #print("fan:on temperature:",temperature)
        elif fan==2:
            temperature=temperature-0.6
            temperature = round(temperature, 1)
            #print('fan:off temperature:',temperature)
        elif fan==3:
            temperature=temperature-0.8
            temperature = round(temperature, 1)
        if temperature < 15 :
            temperature = 15.0
        if temperature >90 :
            temperature = 90.0
        print("fan:",fan," temperature:",temperature)
        post_temperature()
        time.sleep(2)



#t1 = threading.Thread(target = post_temperature)
#t1.start()

t2 = threading.Thread(target = get_instruction)
t2.start()

t3 = threading.Thread(target = env)
t3.start()

while True:
    try:
        x=input()
        if x == '+':
            #mutex.acquire()
            #temperature=temperature+1
            #myobj = {'temperature': temperature}
            #mutex.acquire()
            status=1
        elif x == '-':
            status=0


        #print("temperature:",temperature)
    except:
        break



