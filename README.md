# Real-time Interactive Dashboard for Distributed Systems

This repository contains the code for real-time visualization dashboard for a distributed system using Python.

## Instructions

### Setup

* **Python version: 3.11** 

### Instal Requirements

```commandline
pip install -r requirements.txt
```

### Publisher Client

As a proof-of-concept we use a sample application of visualizing real-time weather data collected from multiple publishers in a distributed system. We provide a Publisher client which can be used to connect to the MQTT broker, subscribe to a topic, and publish the weather data into the topic.

In each producer in the distributed system, you can import PublisherClient from publisher_client.py, connect, and publish data as below. 
```commandline
from publisher_client import PublisherClient

publisher = PublisherClient.connect()
publisher.publish(payload)
```

* Run sample weather data publisher at `sample_weather_data_publisher.py`

### Dashboard Client

this visualization dashboard, we plot different weather data such as temperature, wind speed, humidity, etc. over time by location in real-time. Hvplot.pandas allows us to create interactive dataframes. Panel has a lot of dashboarding templates which allows us to easily layout visualizations together. Using the following code snippet we can design the layout of our visualisation dashboar
