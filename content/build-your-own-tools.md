---
Title: Build your own tools
Date: 2025-04-30
Category: Programming
Description: A love letter to the act of building your own tools, aimed at solving your own problems.
Summary: A love letter to the act of building your own tools, aimed at solving your own problems.
Image: https://images.pexels.com/photos/112897/pexels-photo-112897.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1
hide_image: True
Tags: DIY
Keywords:
---

Whenever I set on building myself a new tool, I get unreasonably excited, because it means that I get to practice my craft of problem-solving through writing code to scratch
an itch. It also means that through this practice, I get to improve my own comfort by solving that particular issue.

For example, the last tool I built is [`epub-optimizer`](https://github.com/brouberol/epub-optimizer), a simple CLI tool aimed at reducing the size of an overly large epub file.
I decided to write it because one book I recently bought was sent to me in the form of a 33MB epub file. Surely, we're not talking about 33MB of text (that would be about 4 million words, for reference),
so what is taking all that space?

Turns out there were many large PNG RGB images, as well as an un-used font bundled in that epub. I then decided to write `epub-optimizer` that would reduce the epub size by performing the following steps:

- unzip the epub (turns out an epub is just a fancy zip with metadata)
- remove unused image files
- convert all png images to black and white images
- run [`jpegoptim`](https://www.mankier.com/1/jpegoptim) on all jpg images
- remove unused font files
- zip the modified file tree with the highest level of compression

And just like that, 2 things happened. I was able to reduce my epub size from 33MB to 11MB without impacting my reading comfort, and I learn quite a lot about how an epub is structured in the process.

I then ran it against my ebook library and reduced its overall size by ~2.

Building my own tools has really shifted my perspective on every day life, as it has given me a sense of control. The same kind of control you feel when you know you can repair your own car, build your own shelf or
rewiring your old electrical panel. It is a way to both acquire knowledge and practice a craft, while improving your own comfort. It removes some of the mystique of technology.

Looking back, I realized that I had built quite the collection of such small tools over the last decade.

- [`5esheets`](https://github.com/brouberol/5esheets):  Visualize and update your D&D 5e character sheets in your browser (abandonned)
- [`blog`](https://github.com/brouberol/blog): this very blog was heavily customized from a [Pelican](https://pelican.readthedocs.org) template
- [`bo`](https://github.com/brouberol/bo): a minimalistic [text editor](https://blog.balthazar-rouberol.com/metaprocrastinating-on-writing-a-book-by-writing-a-text-editor), in which I'm writing this post
- [`cleanup-dungeondraft-asset-packs`](https://github.com/brouberol/cleanup-dungeondraft-asset-packs): CLI tool to cleanup empty tags [from a Dungeondraft asset pack](https://blog.balthazar-rouberol.com/cleaning-up-the-dungeondraft-tag-list)
- [`dnd5e-card-generator`](https://github.com/brouberol/dnd5e-card-generator): Scrape data from aidedd.org to generate [D&D 5e player cards](https://blog.balthazar-rouberol.com/my-dungeon-master-toolkit#spell-cards)
- [`dnd5e-token-exporter`](https://github.com/brouberol/dnd5e-token-exporter):  Export d&d5e [creature tokens](https://blog.balthazar-rouberol.com/my-dungeon-master-toolkit#physical-tokens) onto a page, for printing
- [`generate-ttrpg-maps`](https://blog.balthazar-rouberol.com/making-a-diy-book-of-terrains): generate a [DIY book of TTRPG terrains](https://blog.balthazar-rouberol.com/making-a-diy-book-of-terrains)
- [`grand-cedre`](https://github.com/brouberol/grand-cedre): admininistration tooling for a soft medicine space owned by my mother
- [`infrastructure`](https://github.com/brouberol/infrastructure): personal [infrastructure management tooling](https://blog.balthazar-rouberol.com/managing-my-infra-like-its-2019)
- [`izk`](https://github.com/brouberol/izk): interactive zookeeper shell, with autocompletion, syntax highlighting and history
- [`kafkacfg`](https://github.com/brouberol/kafkacfg): CLI to analyze, query and inspect Kafka configuration tunables between versions
- [`mojo`](https://github.com/brouberol/mojo): Get notified by email when new positions of interest open up at Mozilla
- [`OpenChest`](https://github.com/brouberol/OpenChest): an Android App used to [propose to my girlfriend](https://blog.balthazar-rouberol.com/my-diy-proposal) (now wife!)
- [`page`](https://github.com/brouberol/page): the source code to my [personal page](https://balthazar-rouberol.com)
- [`phable`](https://github.com/brouberol/phable): CLI to manage [Phabricator](https://phabricator.wikimedia.org/) tasks and automate some personal workflows
- [`pico-mixer`](https://github.com/brouberol/pico-mixer): A Dungeons and Dragons [ambiance mixer](https://blog.balthazar-rouberol.com/my-diy-dungeons-and-dragons-ambiance-mixer)
- [`prettymaps`](https://github.com/brouberol/prettymaps): CLI to generate [beautiful maps](https://blog.balthazar-rouberol.com/generating-pretty-maps-ready-to-be-gift-wrapped) centered on a specific address.
- [`srtoffset`](https://github.com/brouberol/srtoffset): CLI to adjust subtitles to the audio track of a movie

As you can see, some of these are work-related, some of these are for hobbies or personal life, or somewhere in between. Some are abandoned, as they served their purpose.
Some are used by others, most of them aren't.

All taught me something, and solved an issue I had at the time.

