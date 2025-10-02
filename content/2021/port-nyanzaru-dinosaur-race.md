{% from 'note.j2' import note %}
{% from 's3.j2' import s3_img %}
---
Title: Running the Port Nyanzaru Dinosaur Race
Date: 2021-04-10
Category: TTRPG
Description: My custom rules for the Port Nyanzaru dinosaur race, in the Tomb of Annihilation DnD5e campaign
Summary: When I was preparing for Port Nyanzaru, in [Tomb of Annihilation](https://dnd.wizards.com/products/tabletop-games/rpg-products/tomb-annihilation), I started reading what other Dungeons Masters had to say about the city. A lot of them would mention that the dinosaur race was a must-do, and that if done properly, it could really be a high point in the start of the adventure. The problem was, I felt that the official rules regarding this race were, well, underwhelming, to say the least. Each player rolls a dice, gets some points or not, repeatedly until the end of the race. If that race was going to be something to remember, I felt that I needed to spice it up a bit.
Image: https://i.pinimg.com/originals/2a/8d/42/2a8d424a5f734afd5a388e75f627f656.png
Tags: D&D5e, Tomb of Annihilation
Keywords: dnd, toa, dinosaur, nyanzaru
---

When I was preparing for Port Nyanzaru, in [Tomb of Annihilation](https://dnd.wizards.com/products/tabletop-games/rpg-products/tomb-annihilation), I started reading what other Dungeons Masters had to say about the city. A lot of them would mention that the dinosaur race was a must-do, and that if done properly, it could really be a high point in the start of the adventure. The problem was, I felt that the official rules regarding this race were, well, underwhelming, to say the least. Each player rolls a dice, gets some points or not, repeatedly until the end of the race. If that race was going to be something to remember, I felt that I needed to spice it up a bit.

The way I designed the race was as a mix between the official rules, the Game of the Goose and Mario Kart. You win if you are the first to complete 2 full laps around the city.  Each lap is made of 48 squares, and starts/finishes at the Coliseum, marked with an X.

{{ s3_img("nyanzaru-race", "nyanzaru-race.webp", "board") }}

The players roll initiative to determine the order in which they'll play. We however consider that they all move at the same time, meaning that if 2 dinosaurs cross the finish line during the same round, they'll be considered ex aequo.

A player's turn goes as follows:

* the jockey rolls an animal handling check against the dinosaur's DC to see if they can control it
    * if successful, the dinosaur moves using its high speed dice
    * if unsuccessful, the dinosaur moves its low speed dice. The jockey could however choose to hit its mount with its whip to coerce it into running faster (using its high speed dice).
        * The dinosaur needs to make a successful CON DD10 check for that.
        * If unsuccessful, it moves at half speed for the rest of the turn.
        * For the more aggressive dinosaurs (the ones marked with an asterisk), if the CON check failed by more than 5 points, it stops moving for 2 rounds, in protest.
* If a dinosaur moves through or stops on a red square (on a bridge), it could attempt to trip another dinosaur located on the same square.
    * If the other dinosaur fails a DD 10 DEX check, it's considered prone for a turn.
* If a dinosaur stops (or _chooses_ to stop) on a blue square, the jockey can decide to pick up some loot box. These boxes can have positive or negative effects, either instantaneous or to possibly be used later, anytime during the player's turn (think Mario Kart loot boxes).

I've kept the same dinosaur stats as given in the book, and used the official [stats block](https://5e.tools/bestiary.html#velociraptor_vgm) for the Velociraptor.

| Dinosaur                  | Race          | Jockey <abbr title="Wisdom">WIS</abbr> | Low speed dice | High speed dice | Animal Handling DC | <abbr title="Constitution">CON</abbr>    | <abbr title="Dexterity">DEX</abbr>    |
|---------------------------|---------------|------------|----------------|-----------------|--------------------|--------|--------|
| Un Tej et l'Addition      | Triceratops   | 14(+2)     | 1d6            | 1d4+6           | 14                 | 15(+2) | 9(-1)  |
| Aubrion du Gers           | Hadrosaurus   | 12(+1)     | 1d6            | 1d2+6           | 10                 | 13(+1) | 10(0)  |
| Mambo Mambo King of Tango | Tyrannosaurus | 17(+3)     | 1d6            | 1d6+6           | 18*                | 17(+3) | 10(0)  |
| Brigadier Gérard          | Dimetrodon    | 13(+1)     | 1d4            | 1d4+4           | 8                  | 15(+2) | 12(+1) |
| Fanfreluche               | Allosaurus    | 16(+2)     | 1d6            | 1d4+6           | 16*                | 15(+2) | 13(+1) |
| Pourquoi il pleure?       | Deinonychus   | 17(+3)     | 1d6            | 1d2+6           | 12*                | 14(+2) | 15(+2) |
| Excelsior VII             | Ankylosaurus  | 16(+2)     | 1d4            | 1d6+4           | 13                 | 16(+2) | 11(+0) |
| Irène                     | Velociraptor  | 15(+2)     | 1d8            | 1d2+8           | 12                 | 13(+1) | 14(+2) |


Here are the loot boxes that I came up with.

| Effect                                                                                                                                                                                                                        | Instantaneous? |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| An insect swarm scares off your mount. Your next move will use your low speed dice.                                                                                                                                           | Yes            |
| You find a juicy spider. When given to your mount, it will run using its high speed dice.                                                                                                                                     | No             |
| You injure yourself on an hallucinogenic vine. Your next animal handling check will be performed at a disadvantage.                                                                                                           | Yes            |
| A reflex potion, when consumed, will give you an advantage at the next DEX check.                                                                                                                                             | No             |
| This net will allow you to immobilize an adversary located on the same square than you during a whole turn if they fail a DEX check DC 12.                                                                                                                        | No             |
| This blessing potion will allow you to add 1d4 to your next skill check or saving throw.                                                                                                                                      | No             |
| These beads allow you to trip all dinosaurs located on the same square than you or the square before you. A dinosaur trips if it fails a DEX check DC 13. In case of failure, its speed is divided by 2 during its next turn. | No             |
| A blinding bomb explodes in your face. If you fail a WIS saving throw DC 13, your next 2 animal handling checks will be performed at a disadvantage.                                                                          | Yes            |
| An appetizing chicken heart will allow you to relaunch your speed dice, after consumption.                                                                                                                                    | No             |
| You get teleported on the same square than the penultimate dinosaur.                                                                                                                                                          | Yes            |

Each player had to pay 20 gold to enter the race. The first finisher gets 100 gold, the second one gets 50 gold and the third one gets 20 gold. The players are obviously free to bet on anything they like, and the DM is responsible for giving them appropriate odds.

I hope these rules will help you run a fun race, or at least give you ideas to create your own set of rules! Feel free to tell me what worked and what didn't if you ran with these!

{{ note("For those of you using Foundry, Steve Vlaminck has created a [plugin](https://gitlab.com/mikedave/foundryvtt-macros/-/tree/master/dino-racing) implementing those very rules!") }}
