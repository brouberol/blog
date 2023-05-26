{% from 's3.j2' import s3_url %}
{% from 'note.j2' import note, warning %}
{% from 'youtube.j2' import youtube_embed %}
---
Title: My DIY Dungeons and Dragons ambiance mixer
Date: 2022-09-24
Category: Dungeons and Dragons
Description: A walkthrough of the design of my DIY hardware sound mixer, inspired by the Launchpad, allowing me to create a great sound ambiance at the D&D table.
Summary: <img src="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/diy-sound-mixer/keypad.jpg"> I find that an immersive sound ambiance is key to helping tabletop RPG players engage. It can increase their stress and sense of urgency during a fight, galvanize them during a harrowing speech, or break their heart when they realize they've just lost something and there's no getting it back. In that article, I will walk you through the design of my fully DIY sound mixer, inspired by the [Launchpad](https://novationmusic.com/en/launch/launchpad-x), allowing me to create a great sound ambiance at the table.
Image: https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/diy-sound-mixer/keypad.jpg
hide_image: True
Tags: Python, DIY
Keywords: DIY, programming, circuitpython, pico, launchpad
---

![keyapd](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/diy-sound-mixer/keypad.jpg)

I find that an immersive sound ambiance is key to helping tabletop RPG players engage. It can increase their stress and sense of urgency during a fight, galvanize them during a harrowing speech, or break their heart when they realize they've just lost something and there's no getting it back.

I have been thinking about using a [Launchpad](https://novationmusic.com/en/launch/launchpad-x) to control and mix the ambiance while we play, but the more I read about its design, the less it seemed to fit. The [cheapest Launchpad](https://store.focusrite.com/en-gb/product/launchpad-mini-mk3-/NOVLPD11~NOVLPD11) starts at 110€, and it is a full fledged  MIDI controller. What I wanted was something simpler: a way to play different long sound ambiance tracks at the same time, and adjust their respective volume to create an immersive atmosphere.

The project started to take shape when I stumbled upon the [Pimoroni RGB Keypad](https://shop.pimoroni.com/products/pico-rgb-keypad-base), a 4x4 rainbow-illuminated keypad that I could program using a [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/), for a budget of about 30€.

![pimoroni keypad](https://camo.githubusercontent.com/9ff5aa6dd7396118c6ac313e7aac199098ebae3654923a987fc6797fe025d0e3/68747470733a2f2f63646e2e73686f706966792e636f6d2f732f66696c65732f312f303137342f313830302f70726f64756374732f7069636f2d6164646f6e732d325f3130323478313032342e6a70673f763d31363131313737393035)

The color and brightness of the LEDs under the keys is [programmable](https://github.com/martinohanlon/pico-rgbkeypad), meaning I could go for the look and feel of a Launchpad, while keeping my budget and the overall complexity in check.

The main idea would be to use 12 of the available 16 keys to start and stop audio tracks, and use the 4 remaining keys as controls (increase/decrease volume, pause all tracks).

![idea](https://user-images.githubusercontent.com/480131/190859070-7c1365d8-d062-462d-a73c-69e2f6cabcc1.png)

## Getting started

If you, like myself, want to program a Raspberry Pi Pico in Python, you have two options:

- [MicroPython](https://micropython.org/)
- [CircuitPython](https://circuitpython.readthedocs.io/)

It took me a while to figure out that these are more or less [the same](https://core-electronics.com.au/videos/circuitpython-vs-micropython-key-differences). In the end, I went with the CircuitPython [starting-up guide](https://learn.adafruit.com/welcome-to-circuitpython), and was ready to make these keys light up.

A CircuitPython main program lives in a `code.py` file, that is executed when the board is plugged in. Any dependency can be put under the `lib/` directory, itself placed at the root of the board filesystem.

I downloaded the [`rgbkeypad.py`](https://github.com/martinohanlon/pico-rgbkeypad/blob/main/rgbkeypad/rgbkeypad.py) library, placed it under `lib/` and wrote the following program in `code.py`

```python
from rgbkeypad import RGBKeypad

keypad = RGBKeypad()

# make all the keys red
keypad.color = (255, 0, 0)  # red
keypad.brightness = 0.5

# turn a key blue when pressed
while True:
    for key in keypad.keys:
        if key.is_pressed():
            key.color = (0, 0, 255)  # blue
```

I then copied `code.py` and `lib/rgbkeypad.py` under the `CIRCUITPY` volume that is mounted when the keypad gets plugged into the computer, and _voilà_.

![red-blue]({{ s3_url("diy-sound-mixer", "red-blue.webp")}})


## Reacting to key presses

Now that I knew how to program the key colors, brightness as well as knowing what keys were being pressed, I still needed a way to map these key events to starting audio tracks, and I was facing an immediate problem: the Pico has no way to play sound, even less on a Bluetooth-connected speaker. You know what can do all that really well though? My laptop.

So, if I could send messages from the Pico to my laptop (on which the Pico is connected for power anyway) and have a program running on my laptop receive them, I could then start thinking about how to play sounds.

It turns out that this was way easier than I thought, thanks to CircuitPython sending anything `print`-ed as binary data over the serial port. Using [`pyserial`](https://pyserial.readthedocs.io/en/latest/), I can write a program that connects to the same serial port the Pico is connected to, and receive the data.

```python
# code.py, running on the Raspberry Pi Pico
from rgbkeypad import RGBKeypad

keypad = RGBKeypad()

# make all the keys red
keypad.color = (255, 0, 0)  # red
keypad.brightness = 0.5

# turn a key blue when pressed
while True:
    for key in keypad.keys:
        if key.is_pressed():
            key.color = (0, 0, 255)  # blue
            print(f"Key ({key.x}, {key.y} pressed!") # <-- that message will be sent over USB
```


```python
# usb_listener.py, running on the laptop
from serial import Serial

# /dev/tty.usbmodem14201 is the name of the serial port the Pico was connected to
# on my mac. Your mileage may vary.
usb_device = Serial("/dev/tty.usbmodem14201")
for line in usb_device:
    print(line.decode("utf-8"))
```

I can now run `usb_listener.py` and press a key on the keypad to see the following:

```console
$ python usb_listener.py
Key (1, 0) was pressed

Key (1, 0) was pressed

Key (1, 0) was pressed
...
```

## Sending structured data from the keypad

Sending text data is fine, but we should probably send data that can be serialized on the keypad size and deserialized on the event listener side, as we will probably send the key ID, a state (`pressed`, `stop`, `volume_up`, etc). JSON is simple enough, and while the `json` package isn't available in CircuitPython, it's pretty easy to hand-encode JSON data:

```python
# code.py, running on the Raspberry Pi Pico
from rgbkeypad import RGBKeypad

keypad = RGBKeypad()

# make all the keys red
keypad.color = (255, 0, 0)  # red
keypad.brightness = 0.5

# turn a key blue when pressed
while True:
    for key in keypad.keys:
        if key.is_pressed():
            key.color = (0, 0, 255)  # blue
            key_id = 4 * key.x + key.y
            print(f'{"key": %d, "state": "pressed"}' % (key_id))
```

```python
# usb_listener.py, running on the laptop
import json

from serial import Serial

# /dev/tty.usbmodem14201 is the name of the serial port the Pico was connected to
# on my mac. Your mileage may vary.
usb_device = Serial("/dev/tty.usbmodem14201")
for line in usb_device:
    print(json.loads(line.decode("utf-8").strip()))
```

## Playing sounds after a keypress

Playing multiple sounds at the same time in Python isn't something many packages allow you to do simply. In the end, I could only make it reliably work with [`pygame`](https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound), which was developped to ease the creation of video games in Python. The package provides us with 2 different APIs to work with sound tracks:

- [`pygame.mixer.music`](https://www.pygame.org/docs/ref/music.html), which allows an audio track to be played while streamed. This was intended to play some background music.
- [`pygame.mixer.Sound`](https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound), which allows you to play an audio track on a specific audio channel. Mutiple `Sound`s can be played over different audio Channels.

Using `pygame.mixer.Sound`, we manage to react to a keypress and start the associated audio track


```python
import pygame
pygame.init()

import json

from serial import Serial
from pygame import mixer
from pygame.mixer import Sound, Channel

key_id_to_audio_tracks = {
    0: Sound("example0.ogg"),
    1: Sound("example1.ogg"),
    2: Sound("example2.ogg"),
}

channels = [Channel() for _ in key_id_to_audio_tracks]
mixer.set_num_channels(len(channels))

usb_device = Serial("/dev/tty.usbmodem14201")
for line in usb_device:
    key_event = json.loads(line.decode("utf-8").strip())
    key_id = key_event['key_id']
    sound = key_id_to_audio_tracks[key_id]
    channel = channels[key_id]
    channel.play(sound)  # will play in the background
```

(The actual code can be inspected [here](https://github.com/brouberol/pico-mixer/blob/main/pico_mixer/mixer.py)).

While it works rather well, this approach has a fundamental issue. Because `mixer.Sound` does not support streaming the sound, as `mixer.music` does, it requires that all sounds be fully loaded in memory at startup. As the ambiance tracks that I'm planning to use all last between 30 minutes and 2h, the actual load time takes a couple of minutes. Using `pygame.music` would solve that issue, except for the fact that it only supports streaming of a single audio file at the same time.

I'm only left with `mixer.Sound` and loading hours of audio files in memory at startup, which means that the whole ambiance would take a lot of time to restart in case of a crash, and the energy around the table might deflate like a soufflé.

_Sigh_

Back to the whiteboard.

Alright, so, what program do I already have on my laptop that is good at streaming sound? What about an Internet browser? Youtube videos don't have to fully load before they start, and the same goes for audio files, so that might just work! I'd need a way to propagate these key events to a web page, so that it can then start/stop the audio files, change their volume, etc. Enter websockets.


## Let's rub some web on it

The mixer would be composed of 3 different systems:

- the keypad, running the CircuitPython code
- a webpage, listening for key events over a websocket, in charge of playing the audio files and adjusting their individual volume
- an HTTP server in charge of receving the events over USB and propagating them to the websocket (ergo, to the browser), and serving the local audio files to the webpage. I'll use `Flask` and `Flask-sock` for this.

![new design](https://user-images.githubusercontent.com/480131/190913995-a27c2385-ea1d-491a-8cc8-84a14d738a49.png)

So what happens now when I press a key:

- a JSON-formatted message is sent from the pico to the serial port
- the message is received by the webserver process, and propagated to the browser on a websocket
- the browser deserializes the message, and takes action, depending on the content of the event

The browser-side message handler looks like this:

```javascript
ws.addEventListener('message', event => {
  const keyEvent = JSON.parse(event.data);
  const usbStatus = document.getElementById("usb_status");

  if (keyEvent.state === "usb_disconnected") {
    usbStatus.textContent = "🔌 🚫";
  } else if (keyEvent.state === "usb_connected") {
    usbStatus.textContent = "🔌 ✅";
  } else if (keyEvent.state === "init") {
    colorizeTracksKbdElements(keyEvent.colors);
  } else if (keyEvent.state === "pause") {
    pauseAllPlayingTracks();
  } else if (keyEvent.state === "unpause") {
    unpauseAllPlayingTracks();
  } else {

    const trackProgressBar = document.getElementById(`progress_track_${keyEvent.key}`);
    const audioElement = document.getElementById(`audio_track_${keyEvent.key}`);

    if (audioElement === null) {
      return;
    }

    switch (keyEvent.state) {
      case "on":
        startTrack(keyEvent.key, audioElement, trackProgressBar);
        break;
      case "off":
        stopTrack(keyEvent.key, audioElement, trackProgressBar);
        break;
      case "vol_up":
        increaseTrackVolume(audioElement, trackProgressBar);
        break;
      case "vol_down":
        decreaseTrackVolume(audioElement, trackProgressBar);
        break;
    }
  }
}
```

## The finishing touch

I have added a couple of features that will help me stay as focused on the storytelling as possible while I'm DMing, instead of thinking about the sound mixing process:

- a [configuration-based tagging system](https://github.com/brouberol/pico-mixer/blob/main/config.json), allowing me to get reminded of the main features for each individual track (is that an ambiance or combat music? Is it dark, light, opressing, eerie, etc?)
- I'm also propagating the key colors to the associated volume bar, allowing me to quickly identify the key that I need to press to start/pause/adjust a given audio track.


![webapp](https://user-images.githubusercontent.com/480131/191582090-3d54a629-ce9f-4f26-9178-f8311c55de6d.png)


{{ note("The key colors were generated from [iwanthue](https://medialab.github.io/iwanthue/) and are stored in the `COLORS` list, in [`code.py`](https://github.com/brouberol/pico-mixer/blob/main/pico/code.py). Any changes to the colors will be reflected in the web UI, as they are advertised to the web-server at propagated to the UI when the keypad starts.")}}

## Demo time

{{ youtube_embed("https://www.youtube.com/embed/cdB_y9KhCgY") }}

## I have the hardware! How can I run it?

Getting started instructions are available [here](https://github.com/brouberol/pico-mixer#getting-started-on-windows) for Windows users, and [here](https://github.com/brouberol/pico-mixer#getting-started-on-macos-and-linux) for macOS and Linux users.

{{ warning("Don't hesitate to read the comments if you have any doubt, as a fair share of questions have already be answered there.") }}

---

## Closing words

The final iteration of that project is available [here](https://github.com/brouberol/pico-mixer/tree/main/pico) (for the keypad code) and [here](https://github.com/brouberol/pico-mixer/tree/main/pico_mixer_web) (for the webserver and webapp code). The black casing was 3D-printed using the `rgb_keypad_-_bottom.stl` file from this [Thingiverse](https://www.thingiverse.com/thing:4883873/files) model.

{{ note("I am grateful to [tom's Hardware](https://www.tomshardware.com/news/raspberry-pi-pico-adds-ambience-to-tabletop-adventures), [Adafruit](https://blog.adafruit.com/2022/10/05/a-raspberry-pi-pico-dd-keyboard-circuitpython-raspberrypi-keyboard-tomshardware-raspberry_pi/), [all3dp](https://all3dp.com/1/best-raspberry-pi-projects/#rpg-ambiance-soundboard), [hackster](https://www.hackster.io/news/balthazar-rouberol-s-raspberry-pi-pico-powered-ambience-mixer-adds-a-new-element-to-d-d-sessions-620dd9bf5c80), [Game News 24](https://game-news24.com/2022/10/05/raspberry-pi-pico-delivers-ambience-to-tabletop-adventures/), [msn](https://www.msn.com/en-gb/money/technology/best-raspberry-pi-projects-february-2023/ar-AA1657Me) and [weareteachers](https://www.weareteachers.com/raspberry-pi-projects/) to have featured and shared this project to their audience.") }}
