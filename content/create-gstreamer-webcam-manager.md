Title: Create a webcam manager using pyGTK and Gstreamer
Category: Programming
Date: 2012-02-29


## Introduction
I recently joined the [Strongsteam](http://www.strongsteam.com) project for a 6 month internship. Our main goal is to provide some _"artificial intelligence and
data mining APIs to let you pull interesting information out of images, video and audio."_
We will be doing a presentation at [Pycon 2012](https://us.pycon.org/2012/), the 9th of March, during the [Startup Row weekend](https://us.pycon.org/2012/community/startuprow/).
On this occasion,  I had to implement a desktop GUI allowing to display a webcam video stream and to capture snapshots, with the following constraints:

 * GUI written with [wxPython](http://wxpython.org/) or [pyGTK](http://www.pygtk.org/)
 * the webcam stream must be integrated in the wxPython/pyGTK window
 * the webcam must not be handled with the [OpenCV](http://opencv.willowgarage.com/wiki/PythonInterface) python module (the installation can be painful on Mac OS X)
 * the snapshots default format and resolution must be JPG and 640x480px

## How to handle the webcam ?
My initial research led me to consider two different solutions:

 * using [PyGame](http://www.pygame.org), a set of python modules adding functionality on top of the [SDL](http://www.libsdl.org/) library
 * using [Gstreamer](http://gstreamer.freedesktop.org/), a pipeline-based multimedia framework allowing _"to create a variety of media-handling components, including simple audio playback, audio and video playback, recording, streaming and editing"_ (quote: wikipedia article). Gstreamer is used by a bunch of multimedia applications, like [Cheese](https://live.gnome.org/Cheese), [Amarok](http://amarok.kde.org/), [Pitivi](http://pitivi.sourceforge.net/), ...

I quickly turned to PyGame, because of the simplicify of the snapshot operation : all we have to do is to use the [`pygame.camera.Camera.get_image()`](http://www.pygame.org/docs/ref/camera.html#pygame.camera.Camera) function. However, the integration of the PyGame surface into a pyGTK interface turned out to be pretty complicated. I found a couple of [StackOverflow posts](http://stackoverflow.com/questions/25661/pygame-within-a-pygtk-application) stating that even though this integration was possible, it was not advised. Indeed, some erratic behaviours seem to be observed when using different OS.

I thus considered Gstreamer, and quicky found this [encouraging project](http://pygstdocs.berlios.de/pygst-tutorial/webcam-viewer.html). This code allowed to start and stop a webcam video stream embedded in a pyGTK interface : I was definitlely in the right place !

## Why doesn't it work with my webcam ?
If you experience some problems testing the project introduced into the previous part (black screen, first run successful and following run leading to black screen, ...) check if your webcam is UVC (USB Video Class) Linux compliant. To do that, type in

```shell
$ lsusb
```

in a terminal and locate the line describing your webcam.

My laptop integrated webcam was described as `Bus 001 Device 003: ID 05ca:1814 Ricoh Co., Ltd HD Webcam`. The reference `05ca:1814` doesn't appear on the [UVC](http://www.ideasonboard.org/uvc/) website. That could explain why I experienced so many problems with it (it appears that Ricoh webcams are poorly UVC compliant).

I hence bought a Logitech QuickCam Pro 9000, known for being well supported. Everything ran smoothly with this one.

## How to use Gstreamer ?
If you don't know how to use Gstreamer, I'd advise you to have a look these pages :

 * [Gstreamer cheat sheet](http://wiki.oz9aec.net/index.php/Gstreamer_Cheat_Sheet)
 * [A weekend with Gstreamer](http://www.oz9aec.net/index.php/gstreamer/345-a-weekend-with-gstreamer)

The main idea is to construct a **pipeline**, by connecting various data sources, sinks and processing blocks (bins) in a data flow graph.

In our case, we are going to use the following pipeline to display the webcam stream:

> `v4l2src ! video/x-raw-yuv,width=640,height=480,framerate=30/1 ! xvimagesink`

 * `v4l2src` : Video for Linux input : your webcam (the default device is `/dev/video0`, but if you are using an external webcam, use `v4l2src device=/dev/video1`)
 * `video/x-raw-yuv` : video colorspace specific to webcam
 * `width=640,height=480` : your webcam resolution (check that it is compatible with your webcam)
 * `framerate=30/1` : number of frames per second
 * `xvimagesink` : video sink

Let's see how to do that in Python:

```python
def create_video_pipeline(self):
    """Set up the video pipeline and the communication bus bewteen the video stream and gtk DrawingArea """
    video_pipeline = 'v4l2src device=/dev/video1 ! video/x-raw-yuv,width=640,height=480,framerate=30/1 ! xvimagesink'
    self.video_player = gst.parse_launch(video_pipeline) # create pipeline
    self.video_player.set_state(gst.STATE_PLAYING)       # start video stream

    bus = self.video_player.get_bus()
    bus.add_signal_watch()
    bus.connect("message", self.on_message)
    bus.enable_sync_message_emission()
    bus.connect("sync-message::element", self.on_sync_message)

def on_message(self, bus, message):
    """ Gst message bus. Closes the pipeline in case of error or end of stream message """
    t = message.type
    if t == gst.MESSAGE_EOS:
        print "MESSAGE EOS"
        self.video_player.set_state(gst.STATE_NULL)
    elif t == gst.MESSAGE_ERROR:
        print "MESSAGE ERROR"
        err, debug = message.parse_error()
        print "Error: %s" % err, debug
        self.video_player.set_state(gst.STATE_NULL)

def on_sync_message(self, bus, message):
    """ Set up the Webcam <--> GUI messages bus """
    if message.structure is None:
        return
    message_name = message.structure.get_name()
    if message_name == "prepare-xwindow-id":
        # Assign the viewport
        imagesink = message.src
        imagesink.set_property("force-aspect-ratio", True)
        # Sending video stream to gtk DrawingArea
        imagesink.set_xwindow_id(self.movie_window.window.xid)

```
Now, we have a live video stream displayed into a pyGTK interface, but still no way of capturing a snapshot.

## How do we capture a snapshot ?
I encountered many StackOverflow open questions about this part, but no satisfactory answer...

At first, I wanted to use Gstreamer for that too, but I couldn't find any way to dynamically modify the pipeline to add a frame extraction, jpg encoding and a filesink (to save the snapshot). I thus tried this ugly hack : when the *'take snapshot'* button is clicked

 * stop the video stream
 * start the following pipeline:  `v4l2src device=/dev/video1 ! video/x-raw-yuv,width=640,height=480,framerate=30/1 ! ffmpegcolorspace !  video/x-raw-rgb,framerate=1/1 ! ffmpegcolorspace ! jpegenc snapshot=true ! filesink location=snap.jpeg`, which will extract a single frame, encode it to jpg and save it to a file.
 * stop this image pipeline
 * re-start the video stream

That was of course ugly, and resulted into a ~2s flicker when taking the snapshot... Back to square one.

I'll save you the suspens, the right solution is to use the `gtk.DrawingArea.window.get_colormap()` method, as shown here:

```python
def take_snapshot(self):
    """ Capture a snapshot from DrawingArea and save it into a image file """
    drawable = self.movie_window.window
    # self.movie_window is of type gtk.DrawingArea()
    colormap = drawable.get_colormap()
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, 0, 8, *drawable.get_size())
    pixbuf = pixbuf.get_from_drawable(drawable, colormap, 0,0,0,0, *drawable.get_size())
    pixbuf = pixbuf.scale_simple(self.W, self.H, gtk.gdk.INTERP_HYPER) # resize
    # We resize from actual window size to wanted resolution
    #  gtk.gdk.INTER_HYPER is the slowest and highest quality reconstruction function
    # More info here : http://developer.gnome.org/pygtk/stable/class-gdkpixbuf.html#method-gdkpixbuf--scale-simple
    filename = 'snap.jpg'
    filepath = relpath(filename)
    pixbuf.save(filename, self.snap_format)
```
This snippet does the following operations:

 * extract the last frame from the `gtk.DrawingArea`
 * encode it to RGB
 * resize it to 640x480px
 * save it to `snap.jpg`

And that's done, without even a teeny-tiny flicker! Yay! We now have a perfecly functional snapshot operation.

## Project source code & Git repository
All the code can be encountered on my [GitHub](https://github.com/BaltoRouberol/Gstreamer-webcam-tool).
