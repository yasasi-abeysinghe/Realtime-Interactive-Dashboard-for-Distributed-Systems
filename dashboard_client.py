import paho.mqtt.client as mqtt
import pandas as pd
import hvplot.pandas
import panel as pn
from tornado.ioloop import IOLoop
import threading
import asyncio
import hvplot.streamz
from streamz import Stream
from streamz.dataframe import DataFrame as sDataFrame
from datetime import date, datetime
import json


MQTT_HOST = "localhost"
MQTT_PORT = 1883
topic = "weather"
Connected = False
playing = True

data_stream = Stream()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(data)
    stream_data(data)


client = mqtt.Client()
client.connect(MQTT_HOST, 1883, 60)

client.on_connect = on_connect
client.on_message = on_message


def stream_data(data):
    global playing
    df = pd.DataFrame({'Temp': int(data["temp"]), 'Feels_Like': int(data["feels_like"]), 'Wind_Speed': int(data["wind"]),
                       'UV': int(data["uv"]), 'Humidity': int(data["humidity"]), 'Location': data["loc"],
                       'Timestamp': pd.Timestamp.now()}, index=[0])
    if playing:
        data_stream.emit(df)


def button_on_click(event):
    global playing
    playing = False if playing else True


# Start the IOLoop to run the server and listen for incoming messages
def start_server():
    pn.extension('vega')

    global data_stream

    index = pd.DatetimeIndex([])
    weather_example = pd.DataFrame(
        {'Temp': [], 'Feels_Like': [], 'Wind_Speed': [], 'UV': [], 'Humidity': [], 'Location': [], 'Timestamp': []},
        columns=['Temp', 'Feels_Like', 'Wind_Speed', 'UV', 'Humidity', 'Location', 'Timestamp'],
        index=[])
    sdf = sDataFrame(data_stream, example=weather_example)

    line_plot_temp = sdf[['Temp', 'Location', 'Timestamp']].hvplot(
        x='Timestamp', y='Temp', xlabel='Timestamp', ylabel='Temperature (F)', by='Location',
        width=500, height=255)

    line_plot_feels_like = sdf[['Feels_Like', 'Location', 'Timestamp']].hvplot(
        x='Timestamp', y='Feels_Like', xlabel='Timestamp', ylabel='Temperature (F)', by='Location',
        width=500)

    line_plot_wind = sdf[['Wind_Speed', 'Location', 'Timestamp']].hvplot(
        x='Timestamp', y='Wind_Speed', xlabel='Timestamp', ylabel='Wind Speed (mph)', by='Location',
        title='Wind Speed', width=500)

    line_plot_uv = sdf[['UV', 'Location', 'Timestamp']].hvplot(
        x='Timestamp', y='UV', xlabel='Timestamp', ylabel='UV Index', by='Location',
        title='UV Index', width=500)

    line_plot_humidity = sdf[['Humidity', 'Location', 'Timestamp']].hvplot(
        x='Timestamp', y='Humidity', xlabel='Timestamp', ylabel='Humidity (%)', by='Location',
        title='Humidity', width=500)

    button = pn.widgets.Button(name='Play/Pause', button_type='primary')
    button.on_click(button_on_click)

    today = str(datetime.now().strftime('%A')) + ", " + str(date.today())

    # Layout using Template
    template = pn.template.FastListTemplate(
        title='Real-time Interactive Dashboard for Data in a Distributed System',
        sidebar=[pn.pane.Markdown("# Weather Dashboard"),
                 pn.pane.Markdown("### Visualization of real-time weather data collected from multiple locations."),
                 pn.pane.PNG('logo.png', sizing_mode='scale_both'),
                 pn.pane.Markdown('<br/><br/><br/>'),
                 pn.pane.Markdown('### Date:'),
                 today,
                 pn.pane.Markdown('### Settings'),
                 button],
        main=[pn.Row(pn.Column(pn.Tabs(
                                    ("Tempterature", line_plot_temp),
                                    ("Feels Like Temperature", line_plot_feels_like),
                                    dynamic=True)
                     ),
                     pn.Column(line_plot_humidity)
        ),
              pn.Row(pn.Column(line_plot_wind), pn.Column(line_plot_uv))],
        accent_base_color="#88d8b0",
        header_background="#88d8b0",
    )

    template.show()
    IOLoop.current().start()


# Define a function to run the MQTT client loop
def run_mqtt_client():
    client.loop_forever()


mqtt_thread = threading.Thread(target=run_mqtt_client)
mqtt_thread.start()

asyncio.run_coroutine_threadsafe(start_server(), asyncio.get_event_loop())

# Wait for the event loop thread to finish
mqtt_thread.join()
