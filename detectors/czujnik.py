import json
import time
import threading
import sys
import mosquitto

humidity = int(sys.argv[1])
rain_or_sprinkling = False if sys.argv[2] == "False" else True
time_to_dry = float(sys.argv[3])
mqqtc_server = sys.argv[4]
id = int(sys.argv[5])
sector_id = None
desired_humidity = None

mqttc = mosquitto.Mosquitto()

def on_connect(mqttc, obj, rc):
    print("rc: "+str(rc))

def on_message(mqttc, obj, msg):
    global sector_id, desired_humidity, rain_or_sprinkling
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    if msg.topic == "agh/iot/project9/config":
        try:
            msg_dict = json.loads(msg.payload)
            for sector in msg_dict["sectors"]:
                if sector["sensor_id"] == id:
                    sector_id = int(sector["id"])
                    desired_humidity = int(sector["desired_humidity"])
                    mqttc.subscribe("agh/iot/project9/simulation/area/"+str(sector_id)+"/rain", 0)

        except Exception as e:
            print("json with incorrect format, "+str(e))

    elif msg.topic == "agh/iot/project9/sensor/"+str(id)+"/request":
        mqttc.publish("agh/iot/project9/sensor/"+str(id)+"/humidity", str(humidity), 0, False)
    elif msg.topic == "agh/iot/project9/simulation/area/"+str(sector_id)+"/rain":
        if msg.payload == b"water":
            rain_or_sprinkling = True
        else:
            rain_or_sprinkling = False




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
        time.sleep(time_to_dry)


mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log
mqttc.connect(mqqtc_server, 1883, 60)

mqttc.subscribe("agh/iot/project9/sensor/"+str(id)+"/request", 0)
mqttc.subscribe("agh/iot/project9/config", 0)

new_thread = threading.Thread(target=humidity_thread)

new_thread.start()

mqttc.loop_forever()
 