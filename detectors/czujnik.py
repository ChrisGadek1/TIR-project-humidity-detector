#!/usr/bin/python

# This shows a simple example of an MQTT subscriber.

import sys
import threading
import serial

import mosquitto

def on_connect(mqttc, obj, rc):
    print("rc: "+str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    scaled_temp = 2 * int(msg.payload) - 32
    ser.write(chr(scaled_temp))

def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

def thread_fun():
    ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
    while True:
        cc = ser.read(1)
        if len(cc) > 0:
            ch = ord(cc)
            if ch >= 64 and ch <= 127:
                temp = ch//4
                mqttc.publish("temp/floor1/room1/pref2", str(temp), 0, True)
                print(temp)




# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mosquitto.Mosquitto() 
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.will_set("temp/floor1/room1/pref2", "pref2:disconnect", 0, True)
# Uncomment to enable debug messages
mqttc.on_log = on_log
#mqttc.connect("127.0.0.1", 1883, 60)

# setting testament for that client
mqttc.will_set("temp/floor1/room1/pref2", "", 0, True)
ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
ser.write(chr(128 + 32 + 16 + 8 + 4 + 1))

mqttc.connect("192.168.17.36", 1883, 60)

mqttc.subscribe("temp/floor1/room1", 0)


new_thread = threading.Thread(target=thread_fun)

new_thread.start()

# publishing message on topic with QoS 0 and the message is not Retained
# mqttc.publish("temp/floor1/room1/pref2", "20", 0, False)

mqttc.loop_forever()
 