{% from 's3.j2' import s3_img, s3_url %}
---
Title: Monitoring my solar panel power production
Date: 2023-05-03
Category: programming
Description: A walkthrough of how I managed to pull metrics from the smart plug my solar panels were connected to, and send them to Datadog.
Summary: I have recently acquired two solar panels from [Sunology](https://sunology.eu/products/sunology-play-kit-solaire) advertising a cumulated instantaneous production of up to 810W. The panels come with a smart plug emitting the data to [Tuya](https://iot.tuya.com/), in order to retain and graph historical data. However, the only available granuarity for that data is _daily_ kWh production. In order to optimize the orientation and placement of the panels, as well as measure the production efficiency (power produced / 810 * 100), I needed a much finer granularity than that. I decided to query the data myself and send it to Datadog.
Image: https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/solar-panel/dd-dash.png
hide_image: True
Tags: datadog, DIY
Keywords: solar panel,
---

I have recently acquired two solar panels from [Sunology](https://sunology.eu/products/sunology-play-kit-solaire) advertising a cumulated instantaneous production of up to 810W. The panels come with a smart plug emitting the data to [Tuya](https://iot.tuya.com/), in order to retain and graph historical data. However, the only available granuarity for that data is _daily_ kWh production. In order to optimize the orientation and placement of the panels, as well as measure the production efficiency (power produced / 810 * 100), I needed a much finer granularity than that. I decided to query the data myself and send it to Datadog.

{{ s3_img("solar-panel", "schema.webp", "information flow from plug to Datadog") }}


The first thing I needed to do was to find a working client that would be able to talk to the plug. It seems that [`tinytuya`](https://github.com/jasonacox/tinytuya) would do the job. However, it didn't seem like I could simply fetch the data from the plug locally. Instead, I first needed to create a Tuya account, a cloud project, and add the plug to the project devices to get both an API key as well as a key for the plug. That proved out to be quite tedious, as the Tuya IoT interface is very confusing and slow, but I managed thanks to these [Home-Assistant instructions](https://www.home-assistant.io/integrations/tuya/).

{{ s3_img("solar-panel", "tuya-project.webp") }}
---
{{ s3_img("solar-panel", "tuya-device.webp") }}

With that data now available, I was then able to setup the `tinytuya` client on a Raspberry Pi with network access to the plug IP.

```shell
$ python -m tinytuya wizard
TinyTuya Setup Wizard [1.12.4]


    Enter API Key from tuya.com: [REDACTED]
    Enter API Secret from tuya.com: [REDACTED]
    Enter any Device ID currently registered in Tuya App (used to pull full list) or 'scan' to scan for one: [REDACTED]
    Enter Your Region (Options: cn, us, us-e, eu, eu-w, or in): eu

>> Configuration Data Saved to tinytuya.json
>> Device Listing
>> Saving list to devices.json
    1 registered devices saved

>> Saving raw TuyaPlatform response to tuya-raw.json

Poll local devices? (Y/n): y

Scanning local network for Tuya devices...
    1 local devices discovered

Polling local devices...
    [Sunology                 ] 192.168.5.171      - [On]  - DPS: {'1': True, '9': 0, '17': 109, '18': 2704, '19': 6491, '20': 2379, '21': 1, '22': 529, '23': 26153, '24': 13705, '25': 3040, '26': 0}

>> Saving device snapshot data to snapshot.json


>> Saving IP addresses to devices.json
    1 device IP addresses found

Done.
```

At that point, the `tinytuya` wizard script had scanned the networks the Pi was connected to, found the plug, and was able to connect to it via the provided device key.

I then created a dedicated APP/API keypair on Datadog, and scheduled this python script to run every minute via cron.


```python
# Run every minute via this crontab
# * * * * * cd /home/br/tuya && /home/br/tuya/.env/bin/python exporter.py

import json
import time

import datadog
import tinytuya

datadog.initialize(
    api_key="[REDACTED]",
    app_key="[REDACTED]",
)

with open("devices.json") as device_file:
    device_data = json.load(device_file)

plug = tinytuya.OutletDevice(
    dev_id=device_data[0]["id"],
    address=device_data[0]["ip"],
    local_key=device_data[0]["key"],
    version=3.3,
)

plug_status = plug.updatedps()
data = plug_status["dps"]

now = time.time()
metrics = []
if "18" in data:
    current = data["18"]  # mA
    metrics.append(
        {
            "metric": "solarpanel.current",
            "type": "gauge",
            "points": [(now, current)],
            "tags": ["location:terrasse_1"],
        }
    )

if "19" in data:
    power = data["19"] / 10.0  # W
    metrics.append(
        {
            "metric": "solarpanel.power",
            "type": "gauge",
            "points": [(now, power)],
            "tags": ["location:terrasse_1"],
        }
    )

if "20" in data:
    voltage = data["20"] / 10.0  # V
    metrics.append(
        {
            "metric": "solarpanel.voltage",
            "type": "gauge",
            "points": [(now, voltage)],
            "tags": ["location:terrasse_1"],
        }
    )

datadog.api.Metric.send(metrics=metrics)
```

At that point, the measured current, voltage and power was sent out to Datadog every minute, and I was then able to create the following [dashboard](https://p.datadoghq.com/sb/bc352bb82-f277a5982d97a0a007ab56fbc05e0ee8):

[![Dashboard detailing electricity production over time]({{ s3_url("solar-panel", "dd-dash.webp")}})](https://p.datadoghq.com/sb/bc352bb82-f277a5982d97a0a007ab56fbc05e0ee8)

With that granularity, I realized that the panels only started to really kick in after midday, and that I should probably move them to a spot with more exposure if I wanted to produce more than 4kWh a day (measured on a hot and sunny day without any clouds). That day, I only hit 85% efficiency though, even though I had hit 99% at some point during the previous weeks. That makes me wonder if I need to wash the panel.

**Edit**: it rained that very night and I did hit 95% efficiency the next day.
