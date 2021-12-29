#!/usr/bin/python

# This shows a simple example of an MQTT subscriber.

import time
import threading
import mosquitto

humidity = 100
rain_or_sprinkling = False

def on_connect(mqttc, obj, rc):
    print("rc: "+str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

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
        time.sleep(2.0)





# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
#mqttc = mosquitto.Mosquitto()
#mqttc.on_message = on_message
#mqttc.on_connect = on_connect
#mqttc.on_publish = on_publish
#mqttc.on_subscribe = on_subscribe
#mqttc.will_set("temp/floor1/room1/pref2", "pref2:disconnect", 0, True)
# Uncomment to enable debug messages
#mqttc.on_log = on_log
#mqttc.connect("127.0.0.1", 1883, 60)

# setting testament for that client
#mqttc.will_set("temp/floor1/room1/pref2", "", 0, True)

#mqttc.connect("192.168.17.36", 1883, 60)

#mqttc.subscribe("temp/floor1/room1", 0)


new_thread = threading.Thread(target=humidity_thread)

new_thread.start()

# publishing message on topic with QoS 0 and the message is not Retained
# mqttc.publish("temp/floor1/room1/pref2", "20", 0, False)

#mqttc.loop_forever()
 