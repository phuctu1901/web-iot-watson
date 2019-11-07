from typing import List, Any
from smarthome.models import Scheduler as SchedulerModels
from django.shortcuts import render
import json
import wiotp.sdk.application
import random
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import include, path
from background_task import background
import pusher
import json
import logging
import csv
import os.path
import threading

logging.basicConfig(filename='timer.log', level=logging.INFO)
from datetime import datetime, timedelta
channels_client = pusher.Pusher(
  app_id='856813',
  key='5a13a066a0cff0149750',
  secret='fa094261cef693aecd1d',
  cluster='ap1',
  ssl=True
)

temp = 0

myConfig = { 
        "auth" :{
            "key": "a-j4fntv-g1om4djfeu",
            "token": "6Rd(EgFF4aGTdf4R_5"
            }
}

client = wiotp.sdk.application.ApplicationClient(config=myConfig)


client.connect()


oldtime = datetime.now()
oldtime_string = oldtime.strftime("%d/%m/%Y %H:%M")
skip = 0


f = open('static/data/scheduler.json', 'r')
flist = json.load(f)
# @background(schedule=20)
def scheduler():
    for item in flist:
        global oldtime_string
        global skip
        current_time = datetime.now() + timedelta(hours=7)
        dt_string = current_time.strftime("%d/%m/%Y %H:%M")
        
        # logging.info(current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])        

        # print(item)
        if item['id'] == 'cambien002':
                        if item['time'] ==  dt_string and dt_string != oldtime_string:
                                oldtime_string = dt_string
                                print("Switch button 2: ", dt_string)
                                commandData={'event':'button2', 'value':"1", 'time':current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
                                client.publishCommand('Cambien', 'cambien001', "control_device", "json", commandData)                
                # if item['id'] == 'cambien002':
                #         if item['time'] ==  dt_string and dt_string != oldtime_string:
                #                 oldtime_string = dt_string
                #                 print("Switch button 2")
                #                 commandData={'event':'button2', 'value':"1"}
                #                 client.publishCommand('Cambien', 'cambien001', "control_device", "json", commandData)

def repeatscheduler():
    while True:
        scheduler()
x = threading.Thread(target=repeatscheduler, args=())
x.start()

def myEventCallback(event):
    # str = "'%s'           [%s]  [%s]"
    # print(event.device, event.eventId, event.data)
    if (event.eventId == 'dht11Data'):
        global temp
        temp = event.data['temp']
        hum = event.data['hum']
        id = event.data['id']
        send_time = event.data['time']
        received_time = datetime.now() + timedelta(hours=7)
        date_time_1 = datetime.strptime(send_time, '%Y-%m-%d %H:%M:%S.%f')
        # date_time_2 = datetime.strptime(received_time, '%Y-%m-%d %H:%M:%S.%f')
        date_time_3 = received_time-date_time_1
        date_time_3_str = str(date_time_3)
        if (os.path.exists('device2application.csv')):
            with open('device2application.csv', mode='a') as csv_file:
                fieldnames = ['event', 'id', 'send_time','received_time','time_delta']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writerow({'event': 'DHT11DATA', 'id': id, 'send_time': send_time, 'received_time': received_time, 'time_delta': date_time_3_str})
        else:
            with open('device2application.csv', mode='a') as csv_file:
                fieldnames = ['event', 'id', 'send_time','received_time','time_delta']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'event': 'DHT11DATA', 'id': id, 'send_time': send_time, 'received_time': received_time, 'time_delta': date_time_3_str})

        channels_client.trigger('my-channel', 'my-event', {'temp': temp, 'hum':hum})
    if(event.eventId == 'buttonSwitch'):
        # print("Button switch")
        button = event.data['button']
        value = event.data['value']
        channels_client.trigger('my-channel', 'button_switch', {'button': button, 'value':value})
    if(event.eventId == 'lightStatus'):
        # print("GET DATA")
        channels_client.trigger('my-channel', 'getLightState', event.data)

    

client.deviceEventCallback = myEventCallback

client.subscribeToDeviceEvents()

def home_view(request):
        return render(request, 'home/index.html', {'temp':temp})

def get_urls(self):
    urls = super().get_urls()
    my_urls = [
        path('button1/', self.set_button1),
        path('button2/', self.set_button2),
    ]
    return my_urls + urls

def set_button1(self):
    commandData={'event':'button1', 'value':"1"}
    client.publishCommand('Cambien', 'cambien001', "control_device", "json", commandData)
    return HttpResponseRedirect("../")

def set_button2(self):
    commandData={'event':'button2', 'value':"1"}
    client.publishCommand('Cambien', 'cambien001', "control_device", "json", commandData) 
    return HttpResponseRedirect("../")


def getLightState(self):
    commandData={'event':'getLightState'}
    client.publishCommand('Cambien', 'cambien001', "control_device", "json", commandData) 
    return HttpResponseRedirect("../")


