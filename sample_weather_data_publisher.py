import random
import time
import numpy as np
import json
from publisher_client import PublisherClient

publisher = PublisherClient.connect()

while True:
    temp = random.randint(50, 100)
    feels_like = temp - random.randint(0, 10)
    wind = random.uniform(0, 40)
    uv = random.randint(0, 12)
    humidity = random.randint(0, 100)
    location = np.random.choice(["New York", "Houston", "LA"])
    payload = json.dumps({"temp": temp, "feels_like": feels_like, "wind": wind, "uv": uv, "humidity": humidity,
                          "loc": location})
    publisher.publish(payload)
    time.sleep(1)
