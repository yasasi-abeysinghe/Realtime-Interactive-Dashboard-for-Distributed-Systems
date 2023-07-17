import paho.mqtt.client as mqtt
import json


MQTT_HOST = "localhost"
MQTT_PORT = 1883
topic = "weather"
payload = json.dumps({"temp": "84", "feels_like": "90", "wind": "5", "uv": "0", "humidity": "70", "loc": "Florida"})


def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass


def on_connect(client, userdata, flags, rc):
    global Connected
    if rc == 0:
        print("Connected to broker")
        Connected = True  # Signal connection

    else:
        print("Connection failed")


# Create an MQTT client and connect to the broker
client = mqtt.Client("MQTT")
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(MQTT_HOST, port=MQTT_PORT)

client.publish(topic, payload)
