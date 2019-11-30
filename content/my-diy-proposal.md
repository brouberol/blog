Title: My DIY proposal
Date: 2019-11-30
Category: DIY
Description: Who said that geeks couldn't be creative and romantic?
TwitterImg: https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/proposal/chest-4.jpeg
status: draft

You know how everyone wants their proposal to be special, thoughtful, original, and above all, wants to avoid being cliché? Well, I wanted all that. I also wanted it to be DIY and geeky. With all that in mind, and because my SO is such a Zelda fan, I decided to propose to her by having her open an Ocarina of time themed treasure chest, which would light up from the inside and play the famous music when it opens.

<div class="vid-container">
    <iframe class="video" src="https://www.youtube.com/embed/69AyYUJUBTg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

I started googling for instructions for a DIY Zelda treasure chest and found this perfect [tutorial](https://www.instructables.com/id/Legend-of-Zelda-Treasure-chest-with-sound/). Now, being perfectly honest, I have to admit that I'm not a very gifted craftsman. The idea of making a chest myself from wood got me a little worried, as I felt that I really needed to be precise and prepared, whereas I tend to lean to the more yolo side of things.

To that end, I started by creating a [3D model](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/proposal/Chest.FCStd) of the chest itself, using [FreeCAD](https://www.freecadweb.org/), which I had to learn from scratch, by using the dimensions (in imperial freedom units) from the [instructables tutorial](https://www.instructables.com/id/Legend-of-Zelda-Treasure-chest-with-sound/).

![3dModel](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/proposal/chest-3d.png)

I finally ended up with something looking pretty good, that I could export to a plan with precise dimensions reported in mm.

![chest-plan](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/proposal/chest-plan.png)

At that point, the easy part was done and I needed to get to the actual building. I found a [fablab](https://fabmanager.astech-fablab.fr) in my area that looked pretty nice, but I couldn't find enough time to sneak around there and actually get to it. Time passed, and I one day noticed a big stack of cardboard lying around in our flat. I finally decided to make the chest out of that, as it would be easier to sneakily work on during the day.

I followed the plan as best as I could, and ended up with something looking really good! (albeit a little wonky)

![chest4](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/proposal/chest-4.jpeg)

![chest2](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/proposal/chest-2.jpeg)
![chest3](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/proposal/chest-3.jpeg)

At that point, I had a nice looking chest, but I also wanted music and light to beam out of it when it was being opened. I investigated a setup based on an Arduino with external speakers, a lever switch and an external LED for a while, but I soon realized that my phone was all I needed to make it work! All I needed to do was write an app that would play an mp3 and light up the phone's LED when it detected an ambient brightness increase. As the brightness sensor needed to face upwards, that'd mean that the LED would face downwards and beam the light towards the bottom of the chest. I decided to put a small mirror in the chest, and go with that.

I taught myself [Kotlin](https://kotlinlang.org/) and Android development on [Udemy](https://udemy.com) (thanks to Datadog for providing employees with an account!), by following [Kotlin for Android: Beginner to Advanced](https://datadog.udemy.com/course/devslopes-android-kotlin/learn/lecture/7866294), by [Devslopes](https://www.youtube.com/channel/UClLXKYEEM8OBBx85DOa6-cg/featured), which I can't recommend enough. I ended up with that small [application](https://github.com/brouberol/OpenChest) installed on my phone, and I was _finally_ all set.

<div class="vid-container">
    <video class="video" controls>
        <source
            src="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/proposal/chest-opening.webm"
            type="video/webm">
    </video>
</div>

The ring was a ruby, obviously.

Oh and she said yes!