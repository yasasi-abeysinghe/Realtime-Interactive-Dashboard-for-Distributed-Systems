import paho.mqtt.client as mqtt


class PublisherClient:
    MQTT_HOST = "localhost"
    MQTT_PORT = 1883
    topic = "weather"

    def on_publish(self, client,userdata,result):             #create function for callback
        print("data published \n")
        pass

    def on_connect(self, client, userdata, flags, rc):
        global Connected
        if rc == 0:
            print("Connected to broker")
            Connected = True  # Signal connection

        else:
            print("Connection failed")

    def connect(self):
        # Create an MQTT client and connect to the broker
        client = mqtt.Client("MQTT")
        client.on_connect = self.on_connect
        client.on_publish = self.on_publish
        client.connect(self.MQTT_HOST, port=self.MQTT_PORT)

    def publish_data(self, payload):
        self.client.publish(self.topic, payload)
