{% from 'img.j2' import side_by_side_images %}
---
Title: Merging multiple mp3 files into an audiobook with chapters
Date: 2023-05-08
Category: TIL
Description: A quick walkthough of how to convert multiple mp3 files into a fully-fledged audiobook m4b file, with chapters and metadata.
Summary: A quick walkthough of how to convert multiple mp3 files into a fully-fledged audiobook m4b file, with chapters and metadata.
Keywords: audiobook, ffmpeg, docker
---

I recently found the 3 Lord of the Rings audiobooks I bought from [Phil Dragash](https://www.phildragash.com/index.html) some years back, as I was digging through my NAS. Each book is split into about 20 mp3 files, which makes it a bit unwieldy for me. As I mostly listen to audiobooks when I'm going to sleep, I oftentimes have to find the last part I remember listening to and start again from there the next day.

Luckily, [BookPlayer](https://apps.apple.com/fr/app/bookplayer/id1138219998) solves this for me, as there's a "Stop after this chapter" feature. However, to import these books into the app, I needed to merge the mp3 files into a full-fledge audiobook [m4b](https://fileinfo.com/extension/m4b) file, with chapter metadata.

After digging a little bit, this is what I found:

```shell
$ docker run \
    -it \  # to see the output of the containerized process in the terminal
    --rm \  # delete the container once the conversion ends
    -u $(id -u):$(id -g) \  # Use the same UID and GID than in the host to avoid permission issues
    -v "$(pwd)/audiobooks":/mnt \  # mount the ./audiobooks folder into /mnt in the container via a docker volume
	sandreas/m4b-tool:latest \  # cf https://hub.docker.com/r/sandreas/m4b-tool
		merge \  # subcommand in charge of merging mp3 into m4b
			"/mnt/The Fellowship of the Ring" \  # directory in which the audio files are located
			--output-file "/mnt/The Fellowship of the Ring.m4b" \  # name of the generated m4b file
			--series "The Lord of the Rings" \  # name of the book series
            --name="The Fellowship of the Ring" \  # title of the book
			--series-part=1 \  # book number in the series
			--artist "J.R.R Tolkien" \  # writer's name
            --albumartist="Phil Dragash" \  # narrator's name
			--use-filenames-as-chapters \  # generate a chapter per mp3 file
			--cover "/mnt/The Fellowship of the Ring/cover.jpg" \  # path to the cover image
			--jobs=8 \  # I used number of CPUs - 2
			--audio-channels=2 \  # 1=mono, 2=stereo
			--audio-samplerate=44100  # I used the same as in the input files
```
Here's the result after I imported the result m4b file into BookPlayer.

{{ side_by_side_images("audiobook", "IMG_7318.webp", "IMG_7319.webp") }}