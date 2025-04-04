{% from 'img.j2' import side_by_side_images %}
{% from 's3.j2' import s3_img, responsive_s3_img %}
{% from 'note.j2' import note %}
{% from 'picture.j2' import picture_light_dark %}
---
Title: My dungeon master toolkit
Date: 2024-04-28
Category: Dungeons and Dragons
Description: One of my favourite aspect of being a dungeon master is building my own tools. I do this with a single goal in mind: improving the immersion by removing much of the in-game friction. This article will walk you through these tools and provide you with the resources you need should you want to use them as well.
Summary: One of my favourite aspect of being a dungeon master is building my own tools. I do this with a single goal in mind: improving the immersion by removing much of the in-game friction. This article will walk you through these tools and provide you with the resources you need should you want to use them as well.
Image: https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/dm-toolkit/dm-toolkit.jpeg
Tags: python, DIY
Keywords: Dungeon Master, TTRPG, D&D, Python, DIY
---


One of my favourite aspect of being a dungeon master is building my own tools. I do this with a single goal in mind: improving the immersion by removing much of the in-game friction. This article will walk you through these tools and provide you with the resources you need should you want to use them as well.

## Physical accessories

I draw all of my maps on a [basic Pathfinder Flip-Mat](https://paizo.com/products/btpy8oto?Pathfinder-FlipMat-Basic). I find it to be the perfect compromise between theater-of-the-mind and combat visualisation. We play with minis that I collected over the years, some painted, some not, some 3D printed, as well as cardboard tokens from the [Pathfinder Beginner Box](https://paizo.com/pathfinder/beginnerbox). I make sure to keep a healthy stock of pencils, erasers as well as a pencil sharpener.

I also own a physical healing potion, as well as a couple of DIY flasks, that are always fun to give around whenever players find an unidentified potion.
Finally, I have a couple of coins and seals to give whenever someone is awarded an inspiration point.

{{ responsive_s3_img("dm-toolkit", "potions") }}

I think this helps remind players that they _have_ these resources at their disposal, as they're not lost in a sea of information in their character sheet.

## Soundboard and ambiance mixer

My [previous article](https://blog.balthazar-rouberol.com/my-diy-dungeons-and-dragons-ambiance-mixer) goes into all the gory details, but the gist is: I built a soundboard allowing me to overlay multiple sound ambiances. I can seamlessly start a combat playlist, then add up some dragon screams when the beast starts hovering over the fight, and amp up the tension by switching to a faster paced-track as the combat ramps up.

{{ side_by_side_images("dm-toolkit", "keypad.webp", "pico-mixer.webp")}}

I pretty quickly realized that I also wanted a way to easily add new ones to my `pico-mixer` config.

I was introduced to [tabletopaudio.com](https://tabletopaudio.com) and the plethora of freely available ambiances to choose from. I found myself thinking about the atmosphere I wanted for my next game, listened to a couple of tracks, and once I found the perfect one, downloaded it and added it to my `pico-mixer` config file. While that worked well, I ended up building a [tool](https://gist.github.com/brouberol/afdd5e947f835fdc06ee4c91e79c8f92) [automating](https://xkcd.com/1319/) these steps, to make it even easier for myself.

{{ picture_light_dark("dm-toolkit/tabletopaudio-dl-light.webp") }}

{{ note("I am a patron of the Tabletop Audio project, and I encourage you to [become one](https://www.patreon.com/tabletopaudio/posts) as well. Please don't take original content without a compensation nor attribution.") | subrender }}

This setup has proven _very_ efficient: my players usually don't even consciously notice the change, but very much feel its effects. That ultimately helps them help me keep tension alive.

## Initiative tracker

The process of tracking initiative at my table was always a little bit ad-hoc and painful. We would usually start writing the players initiative on the battlemap, and then would cram the monster initiative in between, where appropriate. This would result in the turn order being sometimes barely legible, which would in turn break combat immersion as we would try to figure out who was next.

I found this process painful enough to spend time to improve it. I wanted to build an initiative tracker that would be easy to see from both sides of the table, easy to reorganize as the combat evolved, and easy to reuse game night after game night.

I drew a simple flag on a piece of paper, took a picture of it and [converted](https://stackoverflow.com/a/12608376) to jpg to an [SVG](https://balthazar-rouberol.com/public/initiative-tracker-flag.svg). I then cranked up Photoshop, placed 14 of these flags on a [2-side A4 page with cutting lines](https://balthazar-rouberol.com/public/initiative-tracker.pdf), with enough space on the left for a magnet that would allow me to place them on a vertical bar of some kind. I finally printed the page, laminated it, and cut along the lines.

Whenever we start a fight, each player writes their character name and initiative on each side of their tracker, while I do the same for the monsters. We then simply organize the trackers by initiative and start the fight.

{{ side_by_side_images("dm-toolkit", "initiative-tracker-spread.webp", "initiative-tracker.webp", style_2="flex:53%")}}

Because the paper is laminated, I can dry-erase whatever I wrote on each tracker at the end of the fight.


## Spell cards

After a few game nights, I started to notice that one of my players (who was a first-timer) was spending a lot of time looking at his phone under the table. When I pointed this out, he said that he was actually reading his spells descriptions. He was feeling a bit overwhelmed by the number of spells he needed to master, and was afraid of not thinking of the "right" spell to use. As a consequence, he had issues following the game, because he was distracted by his spells under the table, instead of focusing on what was happening _at_ the table.

To remedy this issue, [Etienne](https://etnbrd.com/) and I worked on a way to print physical spell cards to gift each spellcaster. We had several goals for this project:

- the text should be in french but the tooling should be able to export the english spells version as well
- it should be easy to visually sort the spells by level
- it should be easy to determine the type of spell (utility, healing, damage dealing, buff, debuff, control, etc)
- it should be easy to know what dice to roll (I noticed that new players had difficulties knowing which of their dice was the d8, d10 or d12)
- they would need to look nicer than the [Gale Force Nine ones](https://dnd.gf9games.com/gameAcc/tabid/87/entryid/92/spellbook-cards-arcane-73915.aspx)

I wanted my players to not only be able to quickly decide what spell to use, but to feel empowered do this publicly using game props, instead of their phone under the table.

We ended up with tarot-sized cards looking like [this](https://balthazar-rouberol.com/public/rpg-cards.pdf).

{{ responsive_s3_img("dm-toolkit", "cards-recto") }}
{{ responsive_s3_img("dm-toolkit", "cards-verso") }}

{{ note("This is still a WIP, and we're actively improving the design. I'm planning to communicate about the tooling we used when we decide it is ready to be shared.") }}

Not only were my players really happy about being gifted a prop, but they really seemed to be engaging with their spellbook much more than with the condensed list of spells on their character sheet, and ended up being more creative with their abilities! I made sure to have them laminated, so they could for example put a small dot on a card to indicate that the spell was prepared, and dry-erase it it was no longer the case. It also looks generally cooler.


## Physical tokens

I love my minis, but I also wanted to be able to bring more realistic renditions of monsters on the table when I could, especially as my players are about to enter the Underdark and start facing Mind Flayers. I wanted them to be able to see horror face to face, so to speak.

I found this [great video](https://www.youtube.com/watch?v=LBZPi4oKlCQ) from [JP Coovert](https://www.youtube.com/@JPCoovert), who makes all kinds of fun D&D/DIY videos, about how to draw monsters and create physical tokens out of the drawings, using a [hole puncher](https://www.amazon.fr/dp/B007211GS0?psc=1&ref=ppx_yo2ov_dt_b_product_details), [magnets](https://www.amazon.fr/Baker-Ross-disques-magn%C3%A9tiques-Autocollants/dp/B07H5PC1X1/ref=pd_bxgy_thbs_d_sccl_2/261-9604968-9320149?pd_rd_w=W7vAc&content-id=amzn1.sym.7c6a734e-8527-40ee-abbf-1b6b03d9c343&pf_rd_p=7c6a734e-8527-40ee-abbf-1b6b03d9c343&pf_rd_r=NT13QX2CX29ZK0R9B0RW&pd_rd_wg=N5L6h&pd_rd_r=e7d7f9a9-731a-4932-992e-4a991a02ceb6&pd_rd_i=B07H5PC1X1&psc=1) and small [token epoxy covers](https://www.amazon.fr/HEALLILY-Autocollants-Artisanat-Pendentifs-Fabrication/dp/B08XTG1SCQ?pd_rd_w=aM7TK&content-id=amzn1.sym.ccfa293c-eedb-4137-a11f-3633168fdf16&pf_rd_p=ccfa293c-eedb-4137-a11f-3633168fdf16&pf_rd_r=02MHG5DF94MPP03SDBXE&pd_rd_wg=rODEx&pd_rd_r=d0d29265-bc98-44ae-bd0c-2c955955edcf&pd_rd_i=B08XTG1SCQ&psc=1&ref_=pd_bap_d_grid_rp_0_1_ec_pd_gwd_bag_pd_hp_d_atf_rp_1_i).

I first built a tiny [script](https://gist.github.com/brouberol/b5ce880fd02cdc1b8415bde938432a22) using `imagemagick` to create a token out of a square image.

{{ responsive_s3_img("dm-toolkit", "tokenize") }}

Being the crafty programmer that I am, I then created another [CLI tool](https://github.com/brouberol/dnd5e-token-exporter) to automatically layout monster tokens on a page (A4 or A3). The are either local images or automatically scrapped. I could then print it, and punch hole after hole until I got a pretty sizeable collection.

{{ responsive_s3_img("dm-toolkit", "physical-tokens") }}

By default, the CLI will fit 70 tokens on a A4 page (and 140 on an A3), and leave you enough margin to be able to punch-hole cleanly.

By doing this, I can create beautiful and durable tokens for abouy 30c a piece. Thanks again to [JP Coovert](https://www.youtube.com/@JPCoovert) for the inspiration.

## Conclusion

I believe in the power of using physical accessories to ground a theater-of-the-mind experience, especially if these accessories are beautiful to look at, feel cool to use, as well as hide or remove mechanical friction. These accessories help me run a smooth game in which I can build and maintain dramatic tension.
