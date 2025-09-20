{% from 's3.j2' import responsive_s3_img, s3_url %}
{% from 'note.j2' import note %}
{% from 'img.j2' import side_by_side_images %}
---
Title: Making a DIY book of terrains
Date: 2025-02-16
Category: TTRPG
Description: I recently stumbled upon the [Giant Book of Battle Mats](https://shop.black-book-editions.fr/produit/14161/0/books-of-battlemats/big-book-of-battle-mats-vol3), which is a book of A3 laminated TTRPG battlemaps. In this article, I'll go through my process for creating a similar book that I believe displays better reusability.
Summary: I recently stumbled upon the [Giant Book of Battle Mats](https://shop.black-book-editions.fr/produit/14161/0/books-of-battlemats/big-book-of-battle-mats-vol3), which is a book of A3 laminated TTRPG battlemaps. The way I see it, the core idea of the book is to immerse the players into combat by providing a rich visual experience. The main issue I have with that book though, is that the maps are too rich in details, which impedes their reusability. The first time you run a battle on one of these maps, your players might have a lot of fun looking through everything their character can interact wit. However, the next time, they might get a sense of _déjà vu_, which in turn might impact their suspension of disbelief, and ultimately, their immersion. In this article, I'll go through my process for creating a similar book that I believe displays better reusability.
Image: https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/diy-book-of-terrains/header-image.jpg
hide_image: True
Tags: DIY, Dungeondraft
Keywords: Dungeon Master, TTRPG, D&D, Python, DIY, Dungeondraft
---

I recently stumbled upon the [Giant Book of Battle Mats](https://shop.black-book-editions.fr/produit/14161/0/books-of-battlemats/big-book-of-battle-mats-vol3), which is a book of A3 laminated TTRPG battlemaps. The way I see it, the core idea of the book is to immerse the players into combat by providing a rich visual experience. The main issue I have with that book though, is that the maps are too rich in details, which impedes their reusability. The first time you run a battle on one of these maps, your players might have a lot of fun looking through everything their character can interact with. However, the next time, they might get a sense of _déjà vu_, which in turn might impact their suspension of disbelief, and ultimately, their immersion.

In this article, I'll go through my process for creating a similar book that I believe displays better reusability.

### Creating the terrains

The first thing we need for a good book of terrains is, well, terrains. What I wanted was a set of diverse locations and colors, striking enough to be immersive, and generic enough to fit multiple encounters.

To produce these, I used [Dungeondraft](https://dungeondraft.net/), along with some asset packs from [2 minute tabletop](https://2minutetabletop.com/product-category/map-assets/dungeondraft-assets/). The Dungeondraft map should be 16x11 tiles: each tile being 1 inch, you can fit 8x11 tiles on an A4 page, and we want each map to fit a double-page. I then experimented with terrain brushes, water brushes, material brushes as well as building floors, to produce 10 maps featuring grass, snow, tiles, oceanic water, space, etc, and I exported each half (8x11 tiles) to a separate png file, at 300dpi.

{{ responsive_s3_img("diy-book-of-terrains", "dungeondraft-grass") }}

{{ note("I made sure to include `left` and `right` in the file name, to indicate whether the exported crop matched the left or right side of the map. This will become handy later.")}}

### Turning terrains into pages

Now that we have our terrains, we need to turn them into actual book pages, meaning that we need to make sure to fill the entire page to avoid any white margin. The issue being that 8x11 inch does not fill the entire A4 page, which is 8.3x11.7 inch. What I've decided to do is to superimpose the map onto a zoomed-in/gaussian-blurred version of iself. This way, we fill the remaining space with a visually consistent background.

Depending on whether we're dealing with the left or right part of the map, we also need to make sure to leave appropriate space for the book ring. As such, we need to leave more space at the right of the left page and the left of the right page.

{{ side_by_side_images("diy-book-of-terrains", "ocean-left-8x11-A4.webp", "ocean-right-8x11-A4.webp") }}

I created a [python script](https://gist.github.com/brouberol/689b3aadda9d3476ae7b1a83d5963fc8) to automate this whole process using [`pillow`](https://pillow.readthedocs.io/en/stable/) to save me from some tedious Photoshoping. The output images are actually a bit larger than a normal A4 page, as I added 2mm of extra margin space, to account for the [bleed area](https://packoi.com/blog/bleed-and-margin-in-printing/#elementor-toc__heading-anchor-0).

{{ note("In the following example, all the Dungeondraft maps are located under `~/Documents/TTRPG/DIY/Book of Terrains/v1/maps`.") }}

```console
~/Documents/TTRPG/DIY/Book of Terrains ❯ ./generate-pages.py -i v1/maps/*.png -o v1/
Generating page for v1/maps/broken-tiles-left-8x11.png
Generating page for v1/maps/broken-tiles-right-8x11.png
Generating page for v1/maps/grass-left-8x11.png
Generating page for v1/maps/grass-right-8x11.png
Generating page for v1/maps/limestone-left-8x11.png
Generating page for v1/maps/limestone-right-8x11.png
Generating page for v1/maps/moon-left-8x11.png
Generating page for v1/maps/moon-right-8x11.png
Generating page for v1/maps/ocean-left-8x11.png
Generating page for v1/maps/ocean-right-8x11.png
Generating page for v1/maps/sea-left-8x11.png
Generating page for v1/maps/sea-right-8x11.png
Generating page for v1/maps/snow-left-8x11.png
Generating page for v1/maps/snow-right-8x11.png
Generating page for v1/maps/tiles-left-8x11.png
Generating page for v1/maps/tiles-right-8x11.png
Generating page for v1/maps/lava-left-8x11.png
Generating page for v1/maps/lava-right-8x11.png
Generating page for v1/maps/void-left-8x11.png
Generating page for v1/maps/void-right-8x11.png
```

### Exporting the book layout

Now that we have the individual pages, we need to assemble them into the final book layout. I used [Scribus](https://wiki.scribus.net/canvas/Scribus) for that, which happens to be free. I made sure to configure a 2mm bleed on all sides, which should cut a bit into the gaussian blurred margin, but not in the actual grid.

{{ responsive_s3_img("diy-book-of-terrains", "scribus-layout") }}

I then exported the book to a PDF file without compression, and took it to the printer.

{{ note("I created a 4-page [template](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/diy-book-of-terrains/Book-of-Terrains-Template.sla) that you can download and  add pages to, should you want to replicate this for yourself. Don't forget that the first page in the book should be the right part of a double page, and that the last page in the book should be its left counterpart.") }}


### Final product

Once all pages were printed, I got them laminated (to make it possible to erase whatever was drawn during the encounter) and bound using a simple metallic book ring, and _voilà_!
The grid being 1 inch, it fits perfectly with any standard-size mini you can buy out there, as well as with my [token exporter tooling](https://github.com/brouberol/dnd5e-token-exporter).

{{ responsive_s3_img("diy-book-of-terrains", "IMG_1841") }}
{{ responsive_s3_img("diy-book-of-terrains", "IMG_1842") }}
{{ responsive_s3_img("diy-book-of-terrains", "IMG_1843") }}

The whole thing did cost me about 15€ at my friendly local printer for a 10 double page book. Should you want to do away with the whole DIY project and just get the same book printed, feel free to download it from [there]({{ s3_url("diy-book-of-terrains", "Book-of-Terrains-v1.pdf") }})!
