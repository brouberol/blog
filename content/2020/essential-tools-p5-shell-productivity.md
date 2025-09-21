---
Title: Shell productivity tips and tricks
Date: 2020-04-24
Category: Essential Tools and Practices for the Aspiring Software Developer
Description: An introduction to shell productivity features: autocompletion, keyboard shortcuts, history navigation and shell expansions.
Summary: This chapter will walk you through different features of your shell allowing you to do more while typing less, such as autocompletion, keyboard shortcuts, history navigation and shell expansions. Even mastering _some_ of these should make you immensely more productive in your shell day-to-day!
Image: https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/shell-productivity/header.jpg
Tags: terminal
Keywords: history navigation, expansions, productivity, shell, bash, zsh
chapter: 5
---

<header>
<p>
    This article is part of a self-published book project by Balthazar Rouberol and <a href=https://etnbrd.com>Etienne Brodu</a>, ex-roommates, friends and colleagues, aiming at empowering the up and coming generation of developers. We currently are hard at work on it!
</p>
<p>
  If you are interested in the project, we invite you to join the <a href=https://balthazar-rouberol.us4.list-manage.com/subscribe?u=1f6080d496af07a836270ff1d&id=81ebd36adb>mailing list</a>!
</p>
</header>

## Table of Contents

<!-- MarkdownTOC autolink="true" levels="2" autoanchor="true" -->

- [Tab completion](#tab-completion)
- [Keyboard shortcuts](#keyboard-shortcuts)
- [Navigating through history](#navigating-through-history)
- [Shell expansions](#shell-expansions)
- [Real-life examples](#real-life-examples)
- [Summary](#summary)
- [Going further](#going-further)

<!-- /MarkdownTOC -->



# Shell productivity tips

I estimate that I spend around 50% of my day working in my text editor
and my terminal. Any way I can get more productive in these environments
has a direct and measurable impact on my daily productivity as a whole.

If you spend a good chunk of your day repeatedly hitting the left and
right arrow keys to navigate in long commands or correct typos, or
hitting the up or down arrow keys to navigate your command history, this
chapter should help you get more done quicker. We will cover some shell
features you can leverage to make your shell do more of the work for
you.

On a personal level, I probably use some of these up to 30 times a day,
sometimes even without thinking about it, and it gives me a real sense
of ownership of my tool.

In the immortal words of Kimberly “Sweet Brown” Wilkins:

> Ain't nobody got time for that.

<a id="tab-completion"></a>
## Tab completion

When you are typing in your shell, I suggest you treat the
<kbd>Tab</kbd> key as a superpower. Indeed, the same way your phone
keyboard can autocomplete words for you, so can your shell. It can
suggest completions of command names and even command arguments or
options! This works by pressing <kbd>Tab</kbd> (twice for `bash` and
once for `zsh`).

<div class="Note" markdown="1">

One of the reasons `zsh` might be favored over `bash` is its more
powerful auto-completion system, giving more results out-of-the-box and
allowing you to navigate through the auto-completion options.

</div>

Here is an example of `bash` auto-completing a command name:

``` extbash
$ mkd<Tab>
mkdep  mkdir
```

Here is an example of `bash` auto-completing a command argument:

``` extbash
$ man mkd<Tab>
mkdir         mkdirat       mkdtemp       mkdtempat_np
```

And finally, an example of `bash` auto-completing a command option:

``` extbash
$ python -<Tab>
-    -3   -B   -E   -O   -OO  -Q   -R   -S   -V   -W
-b   -c   -d   -h   -i   -m   -s   -t   -u   -v   -x
```

I suggest you get used to using auto-completion as much as possible. It
can save you keystrokes, as well as make you discover command options
you didn't know about.

Pro-tip: if you are using bash, you can get install the
`bash-completion`[^1] package (using your system package-manager) in
order to enable auto-completion for a wide variety of commands that do
not support it out-of-the-box.

<a id="keyboard-shortcuts"></a>
## Keyboard shortcuts

The shell uses a library called `readline`[^2] to provide you with many
keyboard shortcuts to navigate, edit, cut, paste, search, etc, in the
command line. Mastering these will help to dramatically increase your
efficiency, instead of copying and pasting with your mouse, and
navigating the command with the <kbd>↑</kbd> and <kbd>↓</kbd> arrow
keys.

The default shortcuts are inspired by the `emacs`[^3] terminal-based
text editor. If you are already familiar with it, a lot of the default
`readline` shortcuts might feel familiar. `emacs` isn't the only famous
text editor in the history of computers though: another one, dating back
from 1976, is `vi`.[^4] `vi` and `emacs` are designed in two very
different ways, and have two very different logics. It is possible that
one might “click” more than the other for you. If you happen to be
familiar with the `vi` editor and are accustomed to its navigation
system, you can replicate it in your shell as well by adding `set -o vi`
in your shell configuration file. If you are using `zsh` with the Oh My
Zsh framework that we introduced in the previous chapter, you can also
use the `vi-mode` plugin to do this.

The advantage of using the same navigation logic and shortcuts in your
text editor and your terminal is that is blurs the line between both,
and brings consistency to your terminal environment. If you have no clue
how `emacs` or `vi` work though, I would probably suggest you don't
worry about all this for now and experiment with the default terminal
shortcuts.

### Navigating the current line

The following navigation shortcuts allow you to move quickly your cursor
in the current command saving you from relying solely on the
<kbd>→</kbd> and <kbd>←</kbd> arrows.

| Navigation                                                                |                                       Shortcut|
|---------------------------------------------------------------------------|----------------------------------------------:|
| Go to beginning of line                                                   |                 <kbd>Ctrl</kbd> - <kbd>A</kbd>|
| Go to end of line                                                         |                 <kbd>Ctrl</kbd> - <kbd>E</kbd>|
| Go to next word                                                           |                  <kbd>Alt</kbd> - <kbd>F</kbd>|
| Go to previous word                                                       |                  <kbd>Alt</kbd> - <kbd>B</kbd>|
| Toggle your cursor between its current position and the beginning of line |  <kbd>Ctrl</kbd> - <kbd>X</kbd> - <kbd>X</kbd>|

If you however prefer using the `vi` navigation system, you will first
need to type <kbd>Esc</kbd> to switch from the *Insertion* mode to an
emulation of `vi`'s *normal* mode, in which you can navigate in your
text using the following shortcuts:

| Navigation                           |      Shortcut|
|--------------------------------------|-------------:|
| Go to beginning of line              |  <kbd>^</kbd>|
| Go to end of line                    |  <kbd>$</kbd>|
| Go to next word                      |  <kbd>w</kbd>|
| Go to previous word                  |  <kbd>b</kbd>|
| Move to the end of the previous word |  <kbd>e</kbd>|

You can go back to editing your command line by hitting the `i` key.

### Deleting and editing text

These shortcuts allow you to quickly edit the current command more
efficiently than by just using the <kbd>Delete</kbd> key.

| Edition                                      |                                                       Shortcut|
|----------------------------------------------|--------------------------------------------------------------:|
| Delete current character                     |                                 <kbd>Ctrl</kbd> - <kbd>D</kbd>|
| Delete previous word                         |                                 <kbd>Ctrl</kbd> - <kbd>W</kbd>|
| Delete next word                             |                                  <kbd>Alt</kbd> - <kbd>D</kbd>|
| Edit the current command in your text editor |  <kbd>Ctrl</kbd> - <kbd>X</kbd> <kbd>Ctrl</kbd> - <kbd>E</kbd>|
| Undo previous action(s)                      |                                 <kbd>Ctrl</kbd> - <kbd>-</kbd>|

The equivalent `vi`-style shortcuts are:

| Edition                                        |                     Shortcut|
|------------------------------------------------|----------------------------:|
| Replace current character by another (ex: *e*) |  <kbd>r</kbd> - <kbd>e</kbd>|
| Delete current character                       |                 <kbd>x</kbd>|
| Delete previous word                           |  <kbd>d</kbd> - <kbd>b</kbd>|
| Delete next word                               |  <kbd>d</kbd> - <kbd>w</kbd>|
| Edit the current command in your text editor   |                 <kbd>v</kbd>|
| Undo previous action(s)                        |                 <kbd>u</kbd>|

### Cutting and pasting

The shell provides you with shortcuts to cut and paste commands quickly
without using your mouse.

| Action                                   |                        Shortcut|
|------------------------------------------|-------------------------------:|
| Cut current word before the cursor       |  <kbd>Ctrl</kbd> - <kbd>W</kbd>|
| Cut from cursor to end of line           |  <kbd>Ctrl</kbd> - <kbd>K</kbd>|
| Cut from cursor to start of line         |  <kbd>Ctrl</kbd> - <kbd>U</kbd>|
| Paste the cut buffer at current position |  <kbd>Ctrl</kbd> - <kbd>Y</kbd>|

The equivalent `vi`-style shortcuts are:

| Action                                   |                     Shortcut|
|------------------------------------------|----------------------------:|
| Cut current word before the cursor       |  <kbd>d</kbd> - <kbd>w</kbd>|
| Cut from cursor to end of line           |  <kbd>d</kbd> - <kbd>$</kbd>|
| Cut from cursor to start of line         |  <kbd>d</kbd> - <kbd>^</kbd>|
| Paste the cut buffer at current position |                 <kbd>p</kbd>|

### Controlling the terminal

Finally, these shortcuts will let you interact with the terminal itself.

| Action                                  |                        Shortcut|  Equivalent command|
|-----------------------------------------|-------------------------------:|-------------------:|
| Clear the terminal screen               |  <kbd>Ctrl</kbd> - <kbd>L</kbd>|             `clear`|
| Close the terminal screen               |  <kbd>Ctrl</kbd> - <kbd>D</kbd>|              `exit`|
| Send current command to the background. |  <kbd>Ctrl</kbd> - <kbd>Z</kbd>|                    |

Even mastering *some* of these shortcuts should make you immensely more
productive at typing commands and navigating command-line interfaces. I
suggest you take time to experiment until you feel more accustomed with
them. I can guarantee that you will feel the productivity boost!

### A unified command-line editing experience

These shortcuts do not just work in your shell, but in any application
using the `readline` library to allow the user to type and edit
commands. Learning these shortcuts will thus make you productive in all
types of command lines that you might encounter in your career, such as
`python`, `irb`, `sqlite3`, etc.

To make sure you get a smooth and homogeneous editing experience in all
command lines you use in your system, you can set your preferred mode in
the `readline` configuration file itself.

``` extbash
$ cat ~/.inputrc
set editing-mode vi  # or emacs
```

<a id="navigating-through-history"></a>
## Navigating through history

If you find yourself typing a certain command times and times again, you
should probably be aware of how to navigate and search your shell
history, in order to save time and keystrokes.

While the obvious way to re-execute a previous command might seem to
just bash on the <kbd>↑</kbd> key until you find the command you want,
there are faster and smarter ways to accomplish this.

### Searching the history

A very useful and time-saving trick is searching for a command into your
shell history instead of re-typing it from scratch. You can search your
command history by typing <kbd>Ctrl</kbd> - <kbd>R</kbd> which opens a
`reverse-i-search` (backwards search) prompt, in which you can search
for previously executed command containing a given search pattern.

Type <kbd>Ctrl</kbd> - <kbd>R</kbd> to navigate through the results,
until you find the one you were looking for and type the
<kbd>Enter</kbd> key to execute it.

``` extbash
$ <Ctrl-R>
(reverse-i-search): echo <Ctrl-R> <Enter>
$ echo "hello world"
hello world
```

If you want to stop the search, either hit
<kbd>Ctrl</kbd> - <kbd>C</kbd> or <kbd>Ctrl</kbd> - <kbd>G</kbd> to be
sent back into the regular shell prompt.

History search works by looking into the shell history file
(`~/.bash_history` for `bash` and `~/.zsh_history` for `zsh` by
default). Every time you execute a command, it will be added to your
shell history file (with a maximum number of retained commands defined
by the `HISTSIZE` environment variable).

<div class="Note" markdown="1">

The location of your shell history file can be configured by setting the
`HISTFILE` environment variable.

</div>

### Rewriting history

If you want to remove a sensitive command from your history, you can
simply edit your `$HISTFILE` history file and remove it.

``` extbash
$ secret-command --password 1234qwerty  # oh no! that should not be in my history!
$ grep secret-command $HISTFILE
secret-command --password 1234qwerty
$ sed -i '/secret-command/d' $HISTFILE  # deletion of history line containing 'secret-command'
$ grep secret-command $HISTFILE
$ # it's not in history anymore
```

You can also use the `history` built-in command to display your whole
history

``` extbash
$ history | tail -n 5
  496  mkdir test
  497  secret-command --password 1234qwerty
  498  cd
  499  man history
  500  history | tail -n 5
```

Each history line is prefixed by its index in the history. You can then
use `history -d <index>` to remove the associated line from history.

``` extbash
$ history -d 497
$ history | tail -n 7
  496  mkdir test
  497  cd
  498  man history
  499  history | tail -n 5
  500  history -d 497
  501  history | tail -n 7
```

<div class="Note" markdown="1">

This only works with `bash`, not `zsh`.

</div>

### Avoiding history

There is a trick you can use if you want to fly under the radar and
never have a command recorded in history in the first place. Simply
prefix your command by a space.

<div class="Note" markdown="1">

If you are using `zsh`, you need to add `setopt HIST_IGNORE_SPACE` in
your `~/.zshrc` to make sure that behavior is enabled.

</div>

``` extbash
$  secret-command --password 1234qwerty  # notice the space at the start of the command!
$ history | tail -n 2
  502  history | tail -n 7
  503  history | tail -n 2
```

<a id="shell-expansions"></a>
## Shell expansions

The shell can perform expansions, meaning it can replace portions of the
command before executing it. Relying on expansions allows you to type
less and rely on the shell itself to do the heavy lifting. While there
are multiple types of expansions, we will only cover 5:

-   history expansion: quickly access previous commands and arguments
    from history
-   tilde expansion: replace the `~` path prefix
-   pathname expansion: expand a path pattern into a list of files
-   braces expansion: expand a pattern between braces into a longer
    sequence
-   command expansion: replace a sub-command by its output

Expansions are extremely powerful. When used right, an expansion can
literally save you from writing a script.

<div class="Note" markdown="1">

As we only over what we think are the most useful expansions and
shortcuts, feel free to refer to the `bash` manual, section `EXPANSION`
if you want to see the full list.

</div>

### History expansion

Your shell has multiple tricks up its sleeve to allow you to quickly
reference previous commands or arguments in history with a minimum of
keystrokes. While this section only provides you with what we feel are
the most useful of them, feel free to go to the `HISTORY EXPANSION`
section of the `bash` manual.

#### Event designators

An *Event designator* is a reference to a command line entry in the
history list. It allows you to quickly refer to a previous command
without having to re-type it.

##### `!-n`

`!-n` refers to the nth latest command: `!-1` refers to the latest
command, `!-2` to the command before that, etc.

``` extbash
$ echo "hello world!"
hello world!
$ cd
$ !-2  # !-1 is "cd" and !-2 is 'echo "hello world!"'
$ echo "hello world"
hello world
```

`!!` is a shortcut for `!-1`, aka the latest command.

``` extbash
$ echo "hello world!"
hello world!
$ !!
$ echo "hello world"
hello world
```

<div class="Note" markdown="1">

`!!` is oftentimes used in conjunction with `sudo`, to re-execute the
previous command with superuser privileges when it failed, due to a lack
of permission.

``` extbash
$ vim /etc/myfile
vim: /etc/myfile: Permission denied
$ sudo !!
$ sudo vim /etc/myfile
```

</div>

##### `^string1^string2`

`^string1^string2` is used to repeat the previous command in which
`string1` is replaced by `string2`.

``` extbash
$ cat ./myfile
Just a file full of junk
$ ^cat^rm
$ rm ./myfile
```

I personally use and abuse of this technique when I'm about to
irremediably delete some resources (files, folders, containers, etc),
and I want to make sure I'm about to delete the *right* things by
listing these resources first. If you are familiar with SQL queries, it
is the equivalent of executing a `SELECT` query before changing the
`SELECT` to `DELETE` to make sure you're not going to delete more than
you wanted to.

#### Word designators

Word designators are used to select desired words from a previous
command (by default, the latest). They can be very useful when you want
to type a new command that uses arguments previously typed in a previous
command.

##### `!^`

`!^` maps to the first argument of your latest command.

``` extbash
$ touch first.txt second.txt last.txt
$ vim !^
$ vim first.txt
```

##### `!$`

`!$` maps to the last argument of your latest command.

``` extbash
$ touch first.txt second.txt last.txt
$ vim !$
$ vim last.txt
```

##### Combining event and word designators

You can even combine event and word designators in more complex shapes
by using the following syntax

    [EVENT DESIGNATOR]:[WORD DESIGNATOR]

For example, you could use the `!!` event designator to select the last
command, and the `2` word designator to select the second argument.

``` extbash
$ touch first.txt second.txt last.txt
$ vim !!:2
$ vim second.txt
```

### Tilde expansion

For each unquoted word starting with `~` in the command, all characters
preceding a forward slash (`/`) will be considered a *tilde prefix*.
Depending on its actual value, the tilde prefix can be expanded several
ways, although the simple `~` is probably its most common use.

| Tilde prefix |                        Expansion|
|--------------|--------------------------------:|
| `~`          |              Your home directory|
| `~+`         |   Your current working directory|
| `~-`         |  Your previous working directory|

**Example**

``` extbash
$ ls ~
Android                code       Downloads              Music
AndroidStudioProjects  Desktop    Dropbox                Pictures
bin                    Documents  Firefox_wallpaper.png  Videos
```

This lists the content of your home directory, and is the equivalent to
`ls $HOME`. You can combine the tilde with a suffix to compose an
absolute path to some file or folder in your home directory.

``` extbash
$ cd ~/code
$ pwd
/home/br/code
```

### Pathname expansion

Pathname expansions allow you to write an short path pattern and have it
expanded in a list of files and directories, saving you from tedious
copy-pastes or a possibly long (and error-prone) command writing.

#### `*`

The *glob*, or *wildcard* `*` character matches any string. It allows
you to give a *pattern* to the shell, that it will then expand to all
files and directories matching the pattern. The wildcard can be prefixed
or suffixed, which will further specify our pattern. For example,
`*.jpg` matches all files ending with the `.jpg` extension, and
`README.*` matches all files named `README` whatever their extension.

Let us consider the following file and directory structure.

``` extbash
$ tree
.
|-- pic1.jpg
|-- pic2.jpg
|-- pic3.jpg
|-- pic4.jpg
\__ pics
|   |-- pic5.jpg
|   |-- pic6.jpg
|   \__ pic7.jpg
\__ sounds
    \__sound1.mp3

2 directory, 8 files
```

We want to move all `jpg` files into our `pics` directory. Instead of
running 4 different `mv` commands or manually typing a long `mv`
command, we can run just one using a pathname expansion.

``` extbash
$ mv *.jpg pics
$ tree
.
\__ pics
|   |-- pic1.jpg
|   |-- pic2.jpg
|   |-- pic3.jpg
|   |-- pic4.jpg
|   |-- pic5.jpg
|   |-- pic6.jpg
|   \__ pic7.jpg
\__ sounds
    \__sound1.mp3

2 directory, 8 files
```

`*.jpg` was expanded to all files ending with `.jpg`, causing the shell
to actually run `mv pic1.jpg pic2.jpg pic3.jpg pic4.jpg pics`, causing
all 4 `jpg` files to be moved to the `pics` directory in a single
command.

<div class="Note" markdown="1">

We could have executed the following command for the same result: `mv pic*.jpg pics`. This would have moved all files with name starting by `pic` and ending with `.jpg` to the `pics` directory

</div>

You can use `*` several times within the same pattern. For example
`ls */*` will list all files and directories located in a subdirectory.

``` extbash
$ ls */*
sounds/sound1.mp3   pics/pic2.jpg       pics/pic4.jpg       pics/pic6.jpg
pics/pic1.jpg       pics/pic3.jpg       pics/pic5.jpg       pics/pic7.jpg
```

Like in our second example, we can also use `*/*.jpg` to list all `jpg`
files located in a subdirectory.

``` extbash
$ ls */*.jpg
pics/pic1.jpg   pics/pic3.jpg   pics/pic5.jpg  pics/pic7.jpg
pics/pic2.jpg   pics/pic4.jpg   pics/pic6.jpg
```

#### `**`

`**` is expanded to all files and directories in the children
directories, with a depth limit of 1.

``` extbash
$ touch README.txt
$ mkdir sounds/lyrics
$ touch sounds/lyrics/sound1.txt
$ tree
.
|-- README.txt
\__ pics
|   |-- pic1.jpg
|   |-- pic2.jpg
|   |-- pic3.jpg
|   |-- pic4.jpg
|   |-- pic5.jpg
|   |-- pic6.jpg
|   \__ pic7.jpg
\__ sounds
    \__ lyrics
    |   \__sound1.txt
    \__sound1.mp3

3 directories, 10 files
$ ls **
README.txt

pics:
pic1.jpg pic2.jpg pic3.jpg pic4.jpg pic5.jpg pic6.jpg pic7.jpg

sounds:
lyrics     sounds.mp3
```

`ls **` was expanded into `ls README.txt pics/ sounds/`, which does not
include the content of `sounds/lyrics` because of the depth limit of 1.

#### `**/`

`**/` is expanded into all directories and subdirectories with a depth
limit of 1 starting from our first directory.

``` extbash
$ tree
.
|-- README.txt
\__ pics
|   |-- pic1.jpg
|   |-- pic2.jpg
|   |-- pic3.jpg
|   |-- pic4.jpg
|   |-- pic5.jpg
|   |-- pic6.jpg
|   \__ pic7.jpg
\__ sounds
    \__ lyrics
    |   \__sound1.txt
    \__sound1.mp3


3 directories, 10 files
$ ls **/
pics/:
pic1.jpg pic2.jpg pic3.jpg pic4.jpg pic5.jpg pic6.jpg pic7.jpg

sounds/:
lyrics     sounds.mp3

sounds/lyrics/:
sound1.txt
```

`ls **/` was expanded into `ls sounds/ sounds/lyrics pics/`. It thus
listed all files located in our subdirectories.

### Brace expansion

A brace expansion is a mechanism by which the shell can generate
multiple strings based on a sequence of tokens defined within curly
braces. The brace expansion pattern can be preceded by an optional
*preamble* and followed by an optional *postscript*.

``` extbash
$ mkdir ~/test/{pics,sounds,sprites}
$ ls ~/test
pics  sounds  sprites
```

`~/test/{pics,sounds,sprites}` was expanded into
`~/test/pics ~/test/sounds ~/test/sprites` causing the shell to execute
`mkdir ~/test/pics ~/test/sounds ~/test/sprites` (which will be expanded
further into
`mkdir /home/br/test/pics /home/br/test/sounds /home/br/test/sprites` by
a tilde expansion).

We could have done the same thing by factoring the final `s` of each
token into a postscript.

``` extbash
$ mkdir ~/test/{pic,sound,sprite}s
```

A brace expansion can also have a sequence pattern `{x..y[..incr]}`
where `x` and `y` are either an integer or a single character, and
`incr` is an optional increment value.

``` extbash
$ touch ~/test/sounds/noise-{1..5}.mp3
$ ls ~/test/sounds
noise-1.mp3 noise-2.mp3 noise-3.mp3 noise-4.mp3 noise-5.mp3
```

The default increment is 1 if the sequence end is greater than its
start, and -1 otherwise. However, we could specify a custom increment
value if we want.

``` extbash
$ touch ~/test/pics/pic{1..10..2}.jpg
$ ls ~/test/pics
pic1.jpg pic3.jpg pic5.jpg pic7.jpg pic9.jpg
```

### Command expansion

Your shell can replace a command surrounded by `$()` with its output.

I personally like use to commands expansions to iterate over a
command's result, or by combining it with a heredoc redirection:

``` extbash
$ cat <<EOF > aboutme
My name is $(whoami)
and I live in $HOME
EOF
$ cat aboutme
My name is br
and I live in /home/br
```

<a id="real-life-examples"></a>
## Real-life examples

### Moving a pattern of files contained in directories and subdirectories

What is really powerful with these expansions is that, like almost
everything in the shell, they can be combined. The following example
combines a pathname expansion, a brace expansion and a tilde expansion.

``` extbash
$ tree
.
|-- README.txt
\__ pics
|   |-- pic1.jpg
|   |-- pic2.jpg
|   |-- pic3.jpg
|   |-- pic4.jpg
|   |-- pic5.jpg
|   |-- pic6.jpg
|   \__ pic7.jpg
\__ sounds
    \__ lyrics
    |   \__sound1.txt
    \__sound1.mp3
$ mv **/*.{jpg,mp3} ~/assets/
$ tree
|-- README.txt
\__ pics
\__ sounds
    \__ lyrics
        \__sound1.txt
$ ls ~/assets
pic1.jpg   pic2.jpg   pic3.jpg   pic4.jpg   pic5.jpg   pic6.jpg   pic7.jpg   sound1.mp3
```

Using these expansions, we were able to move all `jpg` and `mp3` files
located in directories and subdirectories to the `assets` directory
located in your home directory, in exactly 27 characters!

### Renaming multiple directories

We could use a `for` loop, pathname expansion and a command expansion to
rename all directories contained in the current directory to their
uppercase equivalent.

``` extbash
$ for dir in */; do
    mv "$dir" "$(echo "$dir" | tr '[:lower:]' '[:upper:]')"
  done
```

Let's decompose that command into its different steps:

-   the `*/` glob pattern is expanded over the list of
    directories, on which we iterate via a `for` loop
-   we execute `echo $dir | tr '[:lower:]' '[:upper:]'`, which will
    convert the current directory name to uppercase
-   the `$(echo $dir | tr '[:lower:]' '[:upper:]')` command is expanded
    into the uppercase directory name
-   the directory is renamed into an uppercase name
-   the `for` loop iterates over the next directory name
-   we move on to the next directory and repeat the previous steps for
    each of them

<div class="Note" markdown="1">

Iterating over paths with a `for` loop is brittle as it breaks if a path
contains a space. We will later see how to properly do it using the
`find` command.

</div>

<a id="summary"></a>
## Summary

Your shell has so many productivity tricks and shortcuts up its sleeve
it can be a little bit daunting. I suggest you don't try to learn them
all at once, but really just experiment with them and see what feels
natural. Even mastering some of them will make you more productive!

What if there is an action you find useful but you just don't like the
keyboard shortcut? Luckily for you, the next chapter will dive into how
to personalize and customize your shell.

<a id="going-further"></a>
## Going further

**5.1**: Create a directory. Use a bash expansion to move into that
directory without typing its name a second time.

**5.2**: Print your 4th last command typed into your terminal without
re-typing it.

**5.3**: Create the following empty files `README.txt`,
`requirements.txt` and `TODO.txt` in a single command, without typing
`.txt` more than once.

**5.4**: Delete all the files created in the last question without
typing `.txt` more than once.

**5.5**: Create the following directory tree in a single command.

``` extbash
files
|-- 1
|   |-- 1a
|   |-- 1b
|   |-- 1c
|   |-- 2a
|   |-- 2b
|   |-- 2c
|   |-- 3a
|   |-- 3b
|   \-- 3c
|-- 2
|   |-- 1a
|   |-- 1b
|   |-- 1c
|   |-- 2a
|   |-- 2b
|   |-- 2c
|   |-- 3a
|   |-- 3b
|   \-- 3c
\-- 3
    |-- 1a
    |-- 1b
    |-- 1c
    |-- 2a
    |-- 2b
    |-- 2c
    |-- 3a
    |-- 3b
    \-- 3c
```

**5.6**: Remove all subdirectories starting with `3` created in the
previous command, while keeping the top `3` directory.

**5.7**: Re-execute the command from exercise 5.3 by looking backwards
into your shell history.

[^1]: <https://github.com/scop/bash-completion>

[^2]: <https://tiswww.case.edu/php/chet/readline/rltop.html>

[^3]: <https://www.gnu.org/software/emacs/>

[^4]: <https://en.wikipedia.org/wiki/Vi>


<footer>
<p>
<em>Essential Tools and Practices for the Aspiring Software Developer</em> is a self-published book project by Balthazar Rouberol and <a href=https://etnbrd.com>Etienne Brodu</a>, ex-roommates, friends and colleagues, aiming at empowering the up and coming generation of developers. We currently are hard at work on it!
</p>
<p>The book will help you set up a productive development environment and get acquainted with tools and practices that, along with your programming languages of choice, will go a long way in helping you grow as a software developer.
  It will cover subjects such as mastering the terminal, configuring and getting productive in a shell, the basics of code versioning with <code>git</code>, SQL basics, tools such as <code>Make</code>, <code>jq</code> and regular expressions, networking basics as well as software engineering and collaboration best practices.
</p>
<p>
  If you are interested in the project, we invite you to join the <a href=https://balthazar-rouberol.us4.list-manage.com/subscribe?u=1f6080d496af07a836270ff1d&id=81ebd36adb>mailing list</a>!
</p>
</footer>
