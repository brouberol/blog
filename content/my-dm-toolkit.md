{% from 'img.j2' import side_by_side_images %}
{% from 's3.j2' import s3_img %}
{% from 'note.j2' import note %}
---
Title: My dungeon master toolkit
Date: 2024-04-28
Category: Dungeons and Dragons
Description: One of my favourite aspects of being a dungeon master is building my own tools, with a single goal in mind: improving the immersion by removing much of the in-game friction. This article will walk you through these tools and provide you with the resources you need should you want to replicate them.
Summary: One of my favourite aspects of being a dungeon master is building my own tools, with a single goal in mind: improving the immersion by removing much of the in-game friction. This article will walk you through these tools and provide you with the resources you need should you want to replicate them.
Image: https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/dm-toolkit/dm-toolkit.jpeg
Tags: python, DIY
Keywords: Dungeon Master, TTRPG, D&D, Python, DIY
status: draft
---

**TODO improve main picture**

One of my favourite aspects of being a dungeon master is building my own tools, with a single goal in mind: improving the immersion by removing much of the in-game friction. This article will walk you through these tools and provide you with the resources you need should you want to replicate them.

## Physical accessories

I draw all of my maps on a [basic Pathfinder Flip-Mat](https://paizo.com/products/btpy8oto?Pathfinder-FlipMat-Basic). I find it to be the perfect compromise between theater-of-the-mind and combat visualisation. We play with minis that I collected over the years, some painted, some not, as well as cardboard tokens from the [Pathfinder Beginner Box](https://paizo.com/pathfinder/beginnerbox). I make sure to keep a healthy stock of pencils, erasers as well as a pencil sharpener, for my players.

I also own a physical healing potion, as well as a couple of DIY flasks, that are always fun to give players whenever they find an unidentified potion.
Finally, I have a couple of coins and seals to give my players whenever I award them an inspiration point.

**TODO picture of potions and coins**

## Soundboard and ambiance mixer

My [previous article](https://blog.balthazar-rouberol.com/my-diy-dungeons-and-dragons-ambiance-mixer) goes into all the gory details, but the gist is: I built a soundboard allowing me to overlay multiple sound ambiances. I can seamlessly start a combat playlist, then add up some dragon screams when the beast starts hovering over the fight, and amp up the tension by switching to a track with a faster beat as the combat ramps up.

{{ side_by_side_images("diy-sound-mixer", "keypad.jpg", "pico-mixer.webp")}}

Once I had a way to overlay sound ambiances, I wanted a way to easily add new ones to my pico-mixer config.

I quicky discovered [tabletopaudio.com](https://tabletopaudio.com) and the plethora of freely available ambiances to choose from. I found myself thinking about the atmosphere I wanted for my next game, listened to a couple of tracks, and once I found the perfect one, downloaded it and added it to my `pico-mixer` config. While that worked well, I quickly built a [tool](https://gist.github.com/brouberol/afdd5e947f835fdc06ee4c91e79c8f92) to [automate](https://xkcd.com/1319/) these steps, to make it even easier for myself.

{{ s3_img("dm-toolkit", "tabletopaudio-dl.webp") }}

{{ note("I am a patron of the Tabletop Audio project, and I encourage you to [become one](https://www.patreon.com/tabletopaudio/posts) as well. Please don't take original content without a compensation nor attribution. {{ s3_img('dm-toolkit', 'tabletopaudio-patreon.webp') }} ") | subrender }}

This setup has proven _very_ efficient: my players usually don't even consciously notice the change, but very much feel its effects, which helps them help me keep tension alive.

## Initiative tracker

The process of tracking initiative at my table was always a little bit ad-hoc and painful. We usually would start writing the players initiative on the battlemap, and then would cram the monster initiative in between, where appropriate. This would result in the turn order being sometimes barely legible, which would in turn break combat immersion as we would try to figure out who was next.

I found this process painful enough to spend an hour to improve it. I wanted to build an initiative tracker that would be easy to see from both sides of the table, easy to reorganize as the combat evolved, and easy to reuse game night after game night.

I drew a simple flag on a piece of paper, took a picture of it and [converted](https://stackoverflow.com/a/12608376) to jpg to an [SVG](https://balthazar-rouberol.com/public/initiative-tracker-flag.svg). I then cranked up Photoshop, placed 14 of these flags on a [2-side A4 page with cutting lines](https://balthazar-rouberol.com/public/initiative-tracker.pdf), with enough space at the left for the magnet that would allow me to place them on a vertical bar of some kind. I finally printed the page, laminated it, and cut it along the lines.

Whenever we start a fight, each player write their character name and initiative on each side of their tracker, and I do the same for the monsters. We then simply organize the trackers and start the fight.

{{ side_by_side_images("dm-toolkit", "initiative-tracker-spread.webp", "initiative-tracker.webp", style_2="flex:53%")}}

Because the paper is laminated, I can dry-erase whatever I wrote on each tracker at the end of the fight.

{{ note("If I ever need some new trackers, I'll probably make them a bit smaller, to make sure I can stack a bit more.") }}


## Spell cards

After a few game nights, I started to notice that one of my players (who was playing for the first time), was spending a lot of time looking at his phone under the table. When I pointed this out, he said that he was actually reading his spells descriptions. He was feeling a bit overwhelmed by the number of spells he needed to know by heart, and was afraid of not thinking of the "right" spell to use. As a consequence, he had issues following the game, because he was too focused on his spells instead of what was happening _on_ the table.

To remedy this issue, [Etienne](https://etnbrd.com/) and I worked on a way to print physical spell cards to gift each player playing spellcaster. We had several goals for this project:

- the content would need to be in french but the tooling could export the engish spells as well
- it should be easy to visually sort the spells by level
- it should be easy to determine the type of spell (utility, healing, damage dealing, buff, debuff, etc)
- it should be easy to know what dice to roll (I notice that new players had difficulties knowing which of their dice was the d8, d10 or d12)
- they would need to look nicer than the [Gale Force Nine ones](https://dnd.gf9games.com/gameAcc/tabid/87/entryid/92/spellbook-cards-arcane-73915.aspx)

I wanted my players to not only be able to quickly decide what spell to use, but to feel empowered do this publicly, using game props instead of their phone under the table.

We ended up with tarot-sized cards looking like [this](https://balthazar-rouberol.com/public/rpg-cards.pdf).

{{ s3_img("dm-toolkit", "cards-recto.webp") }}
{{ s3_img("dm-toolkit", "cards-verso.webp") }}

{{ note("This is still a WIP, and we're actively improving the design. I'm planning to communicate about the tooling we used when we decide it is ready to be shared.") }}

Not only were my players really happy about being gifted a prop, but they really seemed to be engaging with their spellbook much more than with the condensed list of spells on their character sheet, and ended up being more creative with their abilities! I made sure to have them laminated as well, so they could for example draw a small dot on them to indicate that they prepared the spell, which they could dry-erase when it's no longer needed. It also looks generally cooler.


## Conclusion

I believe in the power of using physical accessories to ground a theater-of-the-mind experience, especially if these accessories are beautiful to look at, feel cool to use, as well as hide or remove mechanical friction. Tension around the table is like a soufflé. Wait too look for someone to make a decision, and it deflates.