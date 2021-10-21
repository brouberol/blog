Title: To the Underdark and back
Date: 2021-10-21
Category: Dungeons and Dragons
Description: My DM notes for a 2 session detour into the Underdark that I designed from scratch.
Summary: I've recently designed a 2 session long (6h) detour into the Underdark, that would feed into one of my player's character's backstory. The goal was to allow him to meet his long-disappeared father, while introducing both the players and the characters to the strange and dangerous land that is the Underdark.
Tags: Tomb of Annihilation
Image: https://media.dnd.wizards.com/styles/news_banner_header/public/images/news/Underdark_Header_0.jpg
Keywords: dnd, toa, underdark

I've recently designed a 2 session long (6h) detour into the Underdark, that would feed into one of my player's character's backstory. The goal was to allow her to meet her long-disappeared father, while introducing both the players and the characters to the strange and dangerous land that is the Underdark. 

The way I prepared these sessions was an interesting process. I wanted these sessions to be mostly focused on exploration and roleplay, with a single (intense) fight, as well as a puzzle. I tried to design a sandboxed environement with enough lore and backstory to make sure the players enjoy themselves and have a reason to interact with the NPCs. I wanted them to care and have the necessary space and freedom to express themselves.

Following are my session design notes, that lasted me 2 whole sessions. These were as much a way to create the world as reminders about key elements or creature capabilities that I should remember mid-fight. They ended up being quite short, because I tried really hard to paint a picture, and prepare some colorful moments, but not to anticipate my player's reactions. _They_ mostly filled the gaps and brought life to that setting.


_<a id=lang-switcher>Click here to switch to the <span id=lang-switcher-flag>🇫🇷</span> version.</a>_

<picture>
    <source srcset="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/underdark/en/dark/1.png"
    media="(prefers-color-scheme: dark)">
    <img class=dark src="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/underdark/en/light/1.png" />
</picture>

<picture>
    <source srcset="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/underdark/en/dark/2.png"
    media="(prefers-color-scheme: dark)">
    <img class=dark src="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/underdark/en/light/2.png" />
</picture>

<picture>
    <source srcset="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/underdark/en/dark/3.png"
    media="(prefers-color-scheme: dark)">
    <img class=dark src="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/underdark/en/light/3.png" />
</picture>

<picture>
    <source srcset="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/underdark/en/dark/4.png"
    media="(prefers-color-scheme: dark)">
    <img class=dark src="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/underdark/en/light/4.png" />
</picture>

<picture>
    <source srcset="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/underdark/en/dark/5.png"
    media="(prefers-color-scheme: dark)">
    <img class=dark src="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/underdark/en/light/5.png" />
</picture>

<script>
const langSwitcher = document.querySelector('#lang-switcher');
const flag = document.querySelector('#lang-switcher-flag');
const pictures = document.getElementsByTagName("picture");
var currentLang = "en";

function toggleLangInUrl(url, currentLang) {
    if (currentLang == "fr") {
        return url.replace("/fr/", "/en/");
    } else {
        return url.replace("/en/", "/fr/");
    }
}

function toggleCurrentLang(currentLang) {
    if (currentLang == "fr") {
        return "en";
    }
    return "fr";
}

langSwitcher.addEventListener('click', event => {
    for (i=0; i<pictures.length; i++) {
        pic = pictures[i];
        source = pic.getElementsByTagName("source")[0];
        img = pic.getElementsByTagName("img")[0];
        source.srcset = toggleLangInUrl(source.srcset, currentLang);
        img.src = toggleLangInUrl(img.src, currentLang) 
    }
    if (currentLang == "en") {
        flag.textContent = "🇬🇧";
    } else {
        flag.textContent = "🇫🇷";
    }
    currentLang = toggleCurrentLang(currentLang);
});

</script>