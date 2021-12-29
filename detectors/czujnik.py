#!/usr/bin/python

# This shows a simple example of an MQTT subscriber.

import time
import threading
import sys
import mosquitto

humidity = int(sys.argv[1])
rain_or_sprinkling = False if sys.argv[2] == "False" else True
time_to_update = float(sys.argv[3])
mqqtc_server = sys.argv[4]
id = sys.argv[5]


def on_connect(mqttc, obj, rc):
    print("rc: "+str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    #if msg.topic == "project9/config":


def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

def humidity_thread():
    global humidity, rain_or_sprinkling
    while True:
        if humidity > 0 and not rain_or_sprinkling:
            humidity -= 1
        elif humidity < 100 and rain_or_sprinkling:
            humidity = humidity + 5 if humidity + 5 < 100 else 100
        print("current humidity: "+str(humidity))
        print("is raining or sprinkling: "+str(rain_or_sprinkling))
        print("========================")
        time.sleep(time_to_update)


mqttc = mosquitto.Mosquitto()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log
mqttc.connect(mqqtc_server, 1883, 60)

# setting testament for that client
#mqttc.will_set("temp/floor1/room1/pref2", "", 0, True)

mqttc.subscribe("project9/sensor/"+id+"/request", 0)
mqttc.subscribe("project9/config", 0)

new_thread = threading.Thread(target=humidity_thread)

new_thread.start()

# publishing message on topic with QoS 0 and the message is not Retained
# mqttc.publish("temp/floor1/room1/pref2", "20", 0, False)

mqttc.loop_forever()
 