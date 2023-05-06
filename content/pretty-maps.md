{% from 's3.j2' import s3_url %}
{% from 'note.j2' import note %}
---
Title: Generating pretty maps ready to be gift-wrapped
Date: 2023-05-06
Category: programming
Description:
Summary: <img title="Lyon, France" alt="Lyon, France" src="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/prettymaps/lyonfrance-3000-A3-square-default.jpg" />I have been toying with the idea of generating a visually pleasing map, centered on a given address, to have it printed it and framed. The way I see it, it would make an original and personalised gift for the person living there. So when Marcelo de Oliveira Rosa Prates' [`prettymaps`](https://github.com/marceloprates/prettymaps) blew up on Reddit, I decided to try it.
Image: https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/prettymaps/lyonfrance-3000-A3-square-default.jpg
hide_image: True
Tags: DIY, Python
Keywords: maps, generative art
---

<img title="Lyon, France" alt="Lyon, France" src="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/prettymaps/lyonfrance-3000-A3-square-default.jpg" />

I have been toying with the idea of generating a visually pleasing map, centered on a given address, to have it printed it and framed. The way I see it, it would make an original and personalised gift for the person living there. So when Marcelo de Oliveira Rosa Prates' [`prettymaps`](https://github.com/marceloprates/prettymaps) blew up on Reddit, I decided to try it.

The library was great and the visuals looked incredible, yet, I felt it was lacking a couple of features if I were to print the maps.

- a CLI to make it easy to generate maps on the fly
- easily changing the color scheme of buildings (and allowing black and white)
- enabling the generation of rectangular maps, on top of circle and square
- changing the output format of the figure to make it fit into a standard page (A3, A4, etc)
- ensuring a 300dpi output
- set the CLI command used to generate the map as the map title, for autodocumentation purposes

My good friend [Etienne](https://etnbrd.com/) solved the [rectangular map generation](https://github.com/marceloprates/prettymaps/pull/105) in a _beautifully_ laid out PR, that has been sadly sitting there for a while without attention. It _seems_ that the repository owner got issues with NFT con "artists", and pretty much abandonned the project, which hasn't seen activity for the last 5 months.

Seeing this, I decided to [fork the project](https://github.com/brouberol/prettymaps), and work on the remaining ideas.

Here are a couple of examples of maps that I've generated and printed for people in my entourage.

{{ note("The command used to generate each map is displayed as the map title") }}

{{ responsive_image(

    s3_url("prettymaps", "248ruedespyrénées_75020_paris_france-2000-A3-square-RdPu.webp"),
    suffix_to_size={30: 1448, 50: 2480},
    max_width=1500,
    alt="Paris 20e, France",
)}}
{{ responsive_image(

    s3_url("prettymaps", "2impassedel'ancienneposte71100chalonsursaône_france-2000-A3-square-RdPu.webp"),
    suffix_to_size={30: 1392, 50: 1984},
    max_width=1448,
    alt="Chalon-sur-Saône, France",
)}}
{{ responsive_image(

    s3_url("prettymaps", "19ruegustavebalny_60320_béthisy-saint-martin-3000-A3-square-RdPu.webp"),
    suffix_to_size={30: 1392, 50: 1984},
    max_width=1448,
    alt="Béthisy Saint-Martin, France",
)}}
{{ responsive_image(

    s3_url("prettymaps", "40all.jeanjaurès31000toulouse_france-2000-A3-circle-default.webp"),
    suffix_to_size={30: 1392, 50: 1984},
    max_width=1448,
    alt="Toulouse, France",
)}}

The color schemes are only applied to buildings, and are automatically generated from [`matplotlib` colormaps](https://matplotlib.org/stable/gallery/color/colormap_reference.html). This was an quick and easy to generate themes "for free". I also added a couple of Scottish tartan inspired themes, that I used to print a map for a lovely franco-scottish couple who was getting married.

My local printer bills me about 1.5€ for each print, which makes for an original and yet remarkably cheap gift. I recommend a thick and matte paper, without any texture, as it might collide with the map dotted background.

If you'd like to give it a try, feel free to have a look at the [repository](https://github.com/brouberol/prettymaps)!