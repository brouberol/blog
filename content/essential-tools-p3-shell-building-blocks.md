Title: The shell's building blocks
Date: 2020-04-04
Category: Essential Tools and Practices for the Aspiring Software Developer
Description: Something I still find striking after years of using a shell almost daily is how simple yet powerful its building blocks are. Chapter 1 covered commands, I/O streams and pipes. This chapter will cover environment variables, aliases and functions.
Summary: Something I still find striking after years of using a shell almost daily is how simple yet powerful its building blocks are. Chapter 1 covered commands, I/O streams and pipes. This chapter will cover environment variables, aliases and functions.
Image: https://p1.pxfuel.com/preview/880/869/94/lego-build-building-blocks-toys.jpg
Tags: terminal
Keywords: shell, bash, zsh, environment variables, functions, aliases
chapter: 3

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

- [Environment variables](#environment-variables)
- [Aliases](#aliases)
- [Functions](#functions)
- [Real life examples](#real-life-examples)
- [Summary](#summary)
- [Going further](#going-further)

<!-- /MarkdownTOC -->



# The shell's building blocks

As we have seen in the <a href="https://blog.balthazar-rouberol.com/discovering-the-terminal">previous chapters</a>, the shell is a program
allowing you to run other programs. It is an invaluable tool in the life
of a software engineer, as it provides you with a simple text-based
interface to control your computer and any program you might install or
write.

Something I still find striking after years of using a shell almost
daily is how simple yet powerful its building blocks are.

<a href="https://blog.balthazar-rouberol.com/discovering-the-terminal">Chapter 1</a> covered commands, I/O streams and pipes. This chapter will
cover environment variables, aliases and functions.

<a id="environment-variables"></a>
## Environment variables

Environment variables are key/value pairs that affect how running
programs behave. Another way to say that would be that environment
variables can allow you to tweak and personalize how certain programs,
amongst which your shell, work. They can also define what programs will
be called to perform a certain task.

Here are a few examples:

-   `SHELL` defines what shell your terminal runs (‘/bin/bash',
    `/bin/zsh`, `/bin/fish`, etc)
-   `HOME` defines where your home directory is located
-   `EDITOR` defines what text editor program should be used to edit
    text within your terminal (eg `nano`, `vim`, `emacs`, etc)

### Displaying an environment variable's value

To display the value of given environment variable, you can use the
`echo` command, followed by a dollar sign and the name of the variable:

``` extbash
$ echo $SHELL
/bin/zsh
```

You can use the `printenv` command to list all environment variables
along with their value.

``` extbash
$ printenv
USER=br
HOME=/home/br
LC_TERMINAL=terminator
SHELL=/bin/zsh
EDITOR=vim
PWD=/home/br/
PAGER=less
```

For the sake of brevity, I've only displayed a subset of the environment
variables defined on my computer. These variables tell the following
story:

-   my username is `br`
-   all my personal data is stored in my *home directory*, located at
    `/home/br`
-   my default terminal is called `terminator`
-   and whenever I open `terminator`, it runs the commands via the `zsh`
    shell
-   my default text editor is `vim`
-   I am currently located in my home directory
-   my default pager program is `less`

### Changing an environment variable

What is interesting about these environment variables is that they can
be changed, and with them, the behavior of other programs.

For example, let's change the value of our `HOME` environment variable,
defining where our home directory is.

``` extbash
$ HOME=/tmp
$ cd
$ pwd
/tmp
```

In the first line, I redefined the value of my `HOME` environment
variable from `/home/br` to `/tmp`. Remember when you learned that
running `cd` without arguments would take you back to your home
directory? Well, it's actually using the `HOME` environment variable to
figure out where your home directory is. Now that `HOME` has changed, so
has `cd`'s behavior.

Another example is `PAGER`. We saw that my environment had `PAGER=less`
defined by default, which explains why you find yourself reading text
within `less` when you open a man page. `man` fetches the actual
documentation and displays it in a pager, which itself is specified by
the `PAGER` environment variable. If you were to change that variable to
something else, like `more` or `bat`,[^1] it would then change `man`'s
behavior.

<div class="Note" markdown="1">

There is a difference between `SHELL` and `$SHELL`. The first one is the
name of an environment variable, and the latter represents its value.
Consequently, when we executed `echo $SHELL`, we told our shell to
lookup what value was associated with the `SHELL` environment variable,
and then display it to the screen via the `echo` command. `$` is what we
call a *dereference operator* in that context.

</div>

### Defining new variables

Not only can you change an existing environment variable, but you can
also define a new one. If a non-existing variable is `echo`-ed, it will
simply be replaced by an empty string.

``` extbash
$ echo $NEW_VAR

$ NEW_VAR=my-new-env-var
$ echo $NEW_VAR
my-new-env-var
```

If you define an environment variable this way, it will only be visible
by the shell itself, but not by any command executed by your shell (also
called *subprocesses*). To make an environment variable visible by a
subprocess, you need to define it after the `export` keyword.

To illustrate that, we will create our first *shell script*: a program
executing shell commands one after the others.

``` extbash
$ cat <<EOF > echo_var.sh
echo $NEW_VAR
EOF
$ cat echo_var.sh
echo $NEW_VAR
```

As you can see, the `echo_var.sh` *script* only contains one shell
command: `echo $NEW_VAR`.

To execute that bash script, we can run `bash echo_var.sh`, and all
instructions within that script will be executed by `bash`. Let's have a
look at what executing that script displays on the screen with and
without `export`-ing that variable.

``` extbash
$ NEW_VAR=my-new-var
$ echo $NEW_VAR
my-new-var
$ bash echo_var.sh

$ export NEW_VAR=my-new-var
$ echo $NEW_VAR
my-new-var
$ bash echo_var.sh
my-new-var
```

As you can see, the `echo_var.sh` subprocess can see the `NEW_VAR`
environment variable after it has been `export`-ed by its parent shell.

This can very useful if you write programs: some parameters can have a
sane default value but can also be overridden by specifying an
environment variable. `grep` does this for example: reading the `grep`
`man` page, we see:

> `GREP_OPTIONS` May be used to specify default options that will be
> placed at the beginning of the argument list.

### Removing environment variables

You can remove an environment variable by using the `unset` keyword:

``` extbash
$ unset NEW_VAR
$ bash echo_var.sh

$ echo $NEW_VAR

$
```

### The case of `PATH`

Until that point, we've executed commands in the shell, and things
happened. It was a simple world and it was nice. You might wonder *what
would happen if I gave the shell a non-existent command though?*. Well,
I'm glad you asked. Ten points for Gryffindor.

``` extbash
$ cmdnotfound
zsh: command not found: cmdnotfound
```

The `cmdnotfound` command, like its name implies, is not found. But what
makes a command be found then? What makes the shell happily comply when
we type `ls`, and makes it complain when we type `cmdnotfound`? It turns
out that this is due to an environment variable called `PATH`, listing
all directories in which executable programs can be found.

``` extbash
$ echo $PATH
/home/br/bin:/home/br/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
```

This means that for any command passed to the shell, it will look into
these directories (separated by a colon) in search for the program I'm
trying to run.

For example, if I type

``` extbash
$ ls
```

into my shell, it will look into `/home/br/bin`, `/home/br/.local/bin`,
`/usr/local/sbin`, etc, until it finds it in `/bin`.

``` extbash
$ ls /bin
...
chmod      dd         ed        ls         ps         sh         tcsh       zsh
```

If the command is not found in any of the directories listed in `PATH`,
then it is not found.

This means that you can also redefine `PATH` to force your shell to look
into new directories. In fact, this is exactly what I've done to make it
look into `/home/br/bin`, where I store tools of my making.

<div class="Warning" markdown="1">

You can mess with up your shell by running `unset PATH`.

``` extbash
$ unset PATH
$ ls
zsh: command not found: ls
```

However, calling a command by using its absolute or relative path still
works, as `PATH` is only used to look for commands that only have been
invoked by name.

``` extbash
$ unset PATH
$ /bin/ls
bin    code    Documents  ..
...
```

</div>

There is a useful command you can use to know what a program is and
where it is found: `which`.

``` extbash
$ which less
/usr/bin/less
$ which bash
/usr/local/bin/bash
$ which ls
ls: aliased to ls -G
```

Wait. What? What's an alias?

<a id="aliases"></a>
## Aliases

An *alias* allows you to define custom commands. In the previous
example, running `ls` would actually run `ls -G`, which enables
colorized output.

You can define an alias by using the `alias` keyword.

``` extbash
$ alias ls='ls -G'
```

There are a couple of reasons you might want to define aliases:

-   redefining a command's behavior (ex: always using `ls` with the `-G`
    option)
-   shortening a command's name to make it quicker to type (ex:
    `alias ..='cd ..'`)
-   creating new commands altogether (ex:
    `alias filesize='ls --size --human-readable -1'`)

To see the underlying command that will be executed by an alias, you can
type `alias <name>`.

``` extbash
$ alias filesize='ls --size --human-readable -1'
$ alias filesize
alias filesize='ls --size --human-readable -1'
```

Aliases are very simple yet powerful. They allow you to customize your
shell to your liking, create new commands without having to remember a
lot of options, and decrease the time you spend typing, all of which
should make you feel more productive.

<div class="Note" markdown="1">

Aliases can be “nested”. If you define `ls` as an alias of `ls -G` and
`filesize` as an alias of `ls --size --human-readable -1`, your shell
will unwrap both aliases and execute `ls -G --size --human-readable -1`
when you type `filesize`.

</div>

When we're executing `filesize bin`, the shell will see that `filesize`
is an alias for `ls --size --human-readable -1` and will actually
execute the command `ls --size --human-readable -1 bin` behind the
scenes. This simply is done by replacing the alias by its definition in
the command itself. Aliases can however fall short if we want to do
something a more complex than this.

For example, one of my favorite productivity tools is `mkcd`, which
creates a directory and steps into it right after. It saves you from
typing

``` extbash
$ mkdir new-dir
$ cd new-dir
```

where you can just type

``` extbash
$ mkcd new-dir
```

An alias can't really help here, because we are talking about aliasing
two commands with a single alias, which does not work. Enter
*functions*.

<a id="functions"></a>
## Functions

According to the `bash` `man` page:

> A shell function is an object that is called like a simple command and
> executes a compound command with a new set of positional parameters.

Let's see what that looks like in practice. A function is declared this
way.

``` extbash
function name {
    # ...
}
```

If your function is expecting arguments, these can be accessed by using
`$n` where `n` is a number. For example, `$1` is the first function
argument, `$2` its second argument, etc. With that in mind, we can now
declare our `mkcd` function.

``` extbash
function mkcd {
    mkdir -p $1
    cd $1
}
```

Let's now see `mkcd` in action!

``` extbash
$ function mkcd {
    local target=$1
    mkdir -p $target
    cd $target
}
$ pwd
/home/br
$ mkcd test
$ pwd
/home/br/test
```

You can use the `typeset -f` command to see how a function was defined
(or `which <function-name>`, although that only works in `zsh`).

``` extbash
$ typeset -f mkcd
mkcd () {
    mkdir -p $1
    cd $1
}
```

<a id="real-life-examples"></a>
## Real life examples

These are some of the environment variables, aliases and functions I
have defined for myself.

### Shorter navigation aliases

``` extbash
alias ..='cd ..'
alias ...='cd ../..'
```

### Colorize commands output

``` extbash
alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias ip='ip --color'
```

### Alias commands I never remember

``` extbash
# https://xkcd.com/1168/
alias untar='tar -zxvf'
```

### Have `$HOME/bin` be part of `PATH`

``` extbash
export PATH=$PATH:$HOME/bin
```

By extending my `PATH` this way, I can then put every single tool I
create into `$HOME/bin` and have it be usable right-away.

### A backup function

``` extbash
function bak {
    cp -r $1 $1.bak
}
```

This function can be used to backup a file or directory. I regularly use
this when I'm about to edit a critical file and I want to make sure I
can revert my changes if needed.

### Password generation function

This function generate a password composed of alphanumeric characters,
of default length 32.

``` extbash
$ function genpass {
    local passlen=${1:-32}
    # Note: LC_ALL=C is needed for macos compatibility
    LC_ALL=C tr -cd '[:alnum:]' < /dev/urandom | fold -w $passlen | head -n1
}
$ genpass
GQROc0tnABqfYH0qpMMwSPYFgcY7OANB
$ genpass 50
WkeQ14E8FIQZN7XlN7yPkYK4yhMOvpAuNzZivKwODNkskh0uq0
```

### The weather in your terminal

``` extbash
function weather {
    curl "wttr.in/${1:-lyon}?m"
}
```

This function uses `curl` to send an HTTP request to the
`http://wttr.in` website, that displays weather forecasts in a
terminal-friendly way. So I can just type `weather mycity` and *voila*:

    $ weather lyon
    Weather report: lyon

         \   /     Sunny
          .-.      17 °C
       ― (   ) ―   ↖ 6 km/h
          `-'      10 km
         /   \     0.0 mm
                                                           ┌─────────────┐
    ┌──────────────────────────────┬───────────────────────┤  Sat 04 Apr ├───────────────────────┬──────────────────────────────┐
    │            Morning           │             Noon      └──────┬──────┘     Evening           │             Night            │
    ├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
    │    \  /       Partly cloudy  │    \  /       Partly cloudy  │    \  /       Partly cloudy  │    \  /       Partly cloudy  │
    │  _ /"".-.     7..8 °C        │  _ /"".-.     13 °C          │  _ /"".-.     13 °C          │  _ /"".-.     10..11 °C      │
    │    \_(   ).   ← 5-6 km/h     │    \_(   ).   ↙ 5 km/h       │    \_(   ).   ← 5-10 km/h    │    \_(   ).   ↖ 8-17 km/h    │
    │    /(___(__)  10 km          │    /(___(__)  10 km          │    /(___(__)  10 km          │    /(___(__)  10 km          │
    │               0.0 mm | 0%    │               0.0 mm | 0%    │               0.0 mm | 0%    │               0.0 mm | 0%    │
    └──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
                                                           ┌─────────────┐
    ┌──────────────────────────────┬───────────────────────┤  Sun 05 Apr ├───────────────────────┬──────────────────────────────┐
    │            Morning           │             Noon      └──────┬──────┘     Evening           │             Night            │
    ├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
    │     \   /     Sunny          │     \   /     Sunny          │     \   /     Sunny          │    \  /       Partly cloudy  │
    │      .-.      10..12 °C      │      .-.      16 °C          │      .-.      14..15 °C      │  _ /"".-.     10..12 °C      │
    │   ― (   ) ―   ↖ 14-18 km/h   │   ― (   ) ―   ↑ 23-27 km/h   │   ― (   ) ―   ↑ 15-25 km/h   │    \_(   ).   ↑ 13-26 km/h   │
    │      `-'      10 km          │      `-'      10 km          │      `-'      10 km          │    /(___(__)  10 km          │
    │     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │               0.0 mm | 0%    │
    └──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
                                                           ┌─────────────┐
    ┌──────────────────────────────┬───────────────────────┤  Mon 06 Apr ├───────────────────────┬──────────────────────────────┐
    │            Morning           │             Noon      └──────┬──────┘     Evening           │             Night            │
    ├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
    │     \   /     Sunny          │     \   /     Sunny          │     \   /     Sunny          │     \   /     Clear          │
    │      .-.      12..13 °C      │      .-.      16 °C          │      .-.      14..15 °C      │      .-.      11 °C          │
    │   ― (   ) ―   ↖ 18-22 km/h   │   ― (   ) ―   ↑ 22-28 km/h   │   ― (   ) ―   ↑ 14-24 km/h   │   ― (   ) ―   ↑ 8-16 km/h    │
    │      `-'      10 km          │      `-'      10 km          │      `-'      10 km          │      `-'      10 km          │
    │     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │     /   \     0.0 mm | 0%    │
    └──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
    Location: Lyon, Métropole de Lyon, Circonscription départementale du Rhône, Auvergne-Rhône-Alpes, France [45.7578137,4.8320114]

<a id="summary"></a>
## Summary

Environment variables, aliases and functions are simple yet powerful to
change the shell's behavior into something that feels more intuitive.
You feel like `nano` is not shiny enough and prefer using `vim` instead?
Sure. Define `PAGER=vim`. Any command interacting with an editor would
then use `vim` instead of `nano`.

Aliases are a great way to reduce mental friction in the shell by hiding
away complex commands, or just reducing the amount of typing you have to
do. When aliases start being not powerful enough because you want to
execute multiple commands, you can then have a look at functions
instead.

Everything we have seen so far however had an ephemeral effect, as
changes you made would disappear when you close your shell session. In
the next chapter, we will go dive into how to persistently configure
your shell to improve your day-to-day experience and productivity.

<a id="going-further"></a>
## Going further

**3.1**: Write a `cat` alias that displays `meow` on screen.

**3.2**: Write a `restorebak` function that takes a filename as only
argument and renames `$1.bak` into `$1`.

**3.3**: Unset the `PATH` environment variable and then export it back
so that you can use `ls` again.

[^1]: <https://github.com/sharkdp/bat>


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
