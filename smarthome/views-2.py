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
from datetime import datetime, timedelta
channels_client = pusher.Pusher(
  app_id='856813',
  key='5a13a066a0cff0149750',
  secret='fa094261cef693aecd1d',
  cluster='ap1',
  ssl=True
)


# def hello():
#     current_time = datetime.now() + timedelta(hours=7)
#     dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
#     print("Hello world %s!", dt_string)



# from django.shortcuts import get_object_or_404, render, redirect
# from django_socketio import events, broadcast, broadcast_channel

# @events.on_subscribe(channel="tempvalues")
# def subscribe_to_tempvalues(request, socket, context, channel):
#         # print "Subscribed to tempvalues"

# @events.on_subscribe(channel="tempsensor")
# def subscribe_to_tempsensor(request, socket, context, channel):
# #     print "Subscribed to tempsensor"
    
# @events.on_message(channel="^tempsensor")
# def get_temperature(request, socket, context, message):
#     message = message[0]
#     value = message["value"]
#     sensor_id = message["sensor"]
#     socket.send_and_broadcast_channel({"sensor": sensor_id, "value":value}, channel="tempvalues")
    

temp = 0

myConfig = { 
        "auth" :{
            "key": "a-j4fntv-g1om4djfeu",
            "token": "6Rd(EgFF4aGTdf4R_5"
            }
}

client = wiotp.sdk.application.ApplicationClient(config=myConfig)


client.connect()





def myEventCallback(event):
    str = "'%s'           [%s]  [%s]"
    print(str % (event.device, event.eventId, event.data))
    global temp
    temp = event.data['temp']
    hum = event.data['hum']
    channels_client.trigger('my-channel', 'my-event', {'temp': temp, 'hum':hum})

client.deviceEventCallback = myEventCallback

client.subscribeToDeviceEvents()

def home_view(request):
        fscheduler(repeat_until = None)
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
    print("Xin chao")
    return HttpResponseRedirect("../")

def set_button2(self):
    commandData={'event':'button2', 'value':"1"}
    client.publishCommand('Cambien', 'cambien001', "control_device", "json", commandData) 
    print("Xin chao")
    return HttpResponseRedirect("../")

oldtime = datetime.now()
oldtime_string = oldtime.strftime("%d/%m/%Y %H:%M")
skip = 0

class Scheduler:
    def __init__(self, device, time, event, status):
        self.device = device
        self.time= time
        self.event = event
        self.status = status
        # 0: overtime, 1: loaded, 2: waiting
    def get(self):
        print("Hello my name is " + self)
    def update(self, status):
        self.status = status     

def readData(filepath):
    f = open(filepath, 'r')
    filedata = json.load(f)
# print(flist)
    schedulers = []
    for item in filedata:
    # print(item)

        current_time = datetime.now()+timedelta(hours=7)
        dt_string = current_time.strftime("%d/%m/%Y %H:%M") 
        a = datetime.strptime(item['time'], "%d/%m/%Y %H:%M")
        b = datetime.strptime(dt_string, "%d/%m/%Y %H:%M")
        if (a>=b):
            tmp = Scheduler(item['id'], item['time'], 0, 0)
            schedulers.append(tmp)
        else:
            tmp = Scheduler(item['id'], item['time'], 0, 1)
            schedulers.append(tmp)
    json_string = json.dumps([ob.__dict__ for ob in schedulers])
    with open('result.json', 'w') as fp:
        json.dump(json_string, fp)
    return schedulers

schedulers = readData('static/data/scheduler.json')

@background(schedule=0)
def fscheduler():
        s = SchedulerModels.objects.get(device='cambien001')
        print("Device name", s.device)
        schedulers = readData('static/data/scheduler.json')
        for scheduler in schedulers:
              if scheduler.device == 'cambien002':
                        current_time = datetime.now() + timedelta(hours=7)
                        dt_string = current_time.strftime("%d/%m/%Y %H:%M")
                        if scheduler.time ==  dt_string and scheduler.status == 0:
                                # oldtime_string = dt_string
                                print("Switch button 2")
                                commandData={'event':'button2', 'value':"1"}
                                client.publishCommand('Cambien', 'cambien001', "control_device", "json", commandData)
            # count = count +1
            # if (scheduler['status'] == 0):
            # print(scheduler.__dict__)
        # print(count)
        # f = open('static/data/scheduler.json', 'r')
        # flist = json.load(f)
        # for item in flist:
        #         global oldtime_string
        #         global skip
        #         current_time = datetime.now() + timedelta(hours=7)
        #         dt_string = current_time.strftime("%d/%m/%Y %H:%M")
        #         print(dt_string)


        #         # if item['id'] == 'cambien001':
        #         #         # print(datetime.now())
        #         #         if item['time'] ==  dt_string and dt_string != oldtime_string:
        #         #                 oldtime_string = dt_string
        #         #                 print("Switch button 1")
        #         #                 commandData={'event':'button1', 'value':"1"}
        #         #                 client.publishCommand('Cambien', 'cambien001', "control_device", "json", commandData)
                # if item['id'] == 'cambien002':
                #         if item['time'] ==  dt_string and dt_string != oldtime_string:
                #                 oldtime_string = dt_string
                #                 print("Switch button 2")
                #                 commandData={'event':'button2', 'value':"1"}
                #                 client.publishCommand('Cambien', 'cambien001', "control_device", "json", commandData)
