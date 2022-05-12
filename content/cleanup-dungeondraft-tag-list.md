Title: Cleaning up the Dungeondraft tag list
Date: 2021-08-31
Category: Dungeons and Dragons
Description: I wrote a tool to cleanup the Dugeondraft tag list
Summary: I have spent quite a lot of time using [Dungeondraft](https://dungeondraft.net) recently, as I've designed many homebrewed places and encounters. The more maps I created, the more assets pack I bought from [CartographyAssets](https://cartographyassets.com), to further enrich and improve them. I quickly started to realize that some of these asset packs caused the tag list to be filled with entries that weren't linked to any assets at all. This made the asset discovery process quite frustrating.
Image: https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/cleaning-up-dungeondraft-tag-list/cleaned-up-taglist.jpg
Tags: Dungeondraft
Keywords: dnd, dungeondraft

I have spent quite a lot of time using [Dungeondraft](https://dungeondraft.net) recently, as I've designed many homebrewed places and encounters.
The more maps I created, the more assets pack I bought from [CartographyAssets](https://cartographyassets.com), to further enrich and improve them.
I quickly started to realize that some of these asset packs caused the tag list to be filled with entries that weren't linked to any assets at all. This made the asset discovery process quite frustrating.

![board](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/cleaning-up-dungeondraft-tag-list/empty-assets.webp)

Luckily, I found out about [`Dungeondraft-GoPackager`](https://github.com/Ryex/Dungeondraft-GoPackager), a tool that allows anyone to unpack a Dungeondraft asset pack, and inspect its metadata. I discovered that some asset packs would ship with tag entries linked to an empty asset list:

```bash
$ dungeondraft-unpack 2M\ Forest\ Floor\ Assets.dungeondraft_pack .
$ cd 2M\ Forest\ Floor\ Assets
$ cat data/default.dungeondraft_tags | jq .
# ... snip
    "Magic": [],
    "Mattresses": [],
    "Mill": [],
    "Mine": [],
    "Mirror": [],
    "Molds and Stains": [],
    "Mushroom": [],
    "Obstacle": [
      "textures/objects/forestfloor_cliff_1.webp",
      "textures/objects/forestfloor_cliff_2.webp",
      "textures/objects/forestfloor_cliff_3.webp"
    ],
    "Ocean": [],
    "Ottomans": [],
    "Paddles": [],
    "Paper and Books": [],
    "Pillar": [],
    "Pillows": [],
    "Pine Trees": [],
    "Planks and Debris": [],
# ...
```

I suspect the author does that because they export the same list of tag for each asset pack they release. However, having only bought a couple, that caused my tag list to be pretty spotty.

I decided to create a script that would automate the process of unpacking asset packs, removing these empty metadata entries, and then repacking everything up. While the process is pretty simple conceptually, it can become tedious when the number of packs grows.

The result of that work is [`cleanup-dungeondraft-asset-packs`](https://github.com/brouberol/cleanup-dungeondraft-asset-packs), that you can install by running the following command:

```bash
$ pip3 install --user cleanup-dungeondraft-asset-packs
Collecting cleanup-dungeondraft-asset-packs
  Downloading cleanup_dungeondraft_asset_packs-0.1.0-py3-none-any.whl (4.2 kB)
Installing collected packages: cleanup-dungeondraft-asset-packs
Successfully installed cleanup-dungeondraft-asset-packs-0.1.0
```

Once installed, you just have to point it to your assets directory, and _voilà_:

```bash
$ cleanup-dungeondraft-asset-packs --assets-dir ~/Documents/DnD/DungeonDraft/Assets
INFO:root:Unpacking /Users/br/Documents/DnD/DungeonDraft/Assets/CH-Forest-Demo.dungeondraft_pack
INFO:root:Repacking tmp/CH-Forest-Demo
WARN[0000] overwriting file                              id=kt201FMq name="CH - Forest Demo" outPackagePath="/Users/br/Documents/DnD/DungeonDraft/Assets/cleaned/CH - Forest Demo.dungeondraft_pack" path=/Users/br/Documents/DnD/DungeonDraft/Assets/tmp/CH-Forest-Demo
INFO:root:Unpacking /Users/br/Documents/DnD/DungeonDraft/Assets/AS-Forest-apmh1i.dungeondraft_pack
INFO:root:Skipping, as no dungeondraft_tags file is found
INFO:root:Repacking tmp/AS-Forest-apmh1i
WARN[0000] overwriting file                              id=qxhzAkxg name="AS Forest" outPackagePath="/Users/br/Documents/DnD/DungeonDraft/Assets/cleaned/AS Forest.dungeondraft_pack" path=/Users/br/Documents/DnD/DungeonDraft/Assets/tmp/AS-Forest-apmh1i
INFO:root:Unpacking /Users/br/Documents/DnD/DungeonDraft/Assets/2M Forest Floor Assets.dungeondraft_pack
INFO:root:Skipping empty tag Administration
INFO:root:Skipping empty tag Animals
INFO:root:Skipping empty tag Armchairs
INFO:root:Skipping empty tag Armor
...
```


Now, re-open Dungeondraft, and point it to the `cleaned` directory that `cleanup-dungeondraft-asset-packs` created, in which it placed all cleaned assets.

![cleaned-assets](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/cleaning-up-dungeondraft-tag-list/dungeondraft-assets-cleaned.webp)


At that point, your tag list should only contain entries linked to _actual_ assets!

![cleaned-up-taglist](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/cleaning-up-dungeondraft-tag-list/cleaned-up-taglist.webp)

There you go, I hope that helps! Happy Dungeondrafting!
