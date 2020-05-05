Title: Text processing in the shell
Date: 2020-03-14
Category: Essential Tools and Practices for the Aspiring Software Developer
Description: A quick overview of the most common text processing terminal tools and why they should be part of your day-to-day toolbox.
Summary: One of the things that makes the shell an invaluable tool is the amount of available text processing commands, and the ability to easily pipe them into each other to build complex text processing workflows. These commands can make it trivial to perform text and data analysis, convert data between different formats, filter lines, etc. This chapter will go over some of the most common and useful text processing commands the shell has to offer, and will demonstrate real-life workflows piping them together.
Image: https://live.staticflickr.com/2909/14074154115_efa9541b12_b.jpg
Tags: terminal
Keywords: bash, awk, grep, sed, zsh, linux
chapter: 2

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

- [`cat`](#cat)
- [`head`](#head)
- [`tail`](#tail)
- [`wc`](#wc)
- [`grep`](#grep)
- [`cut`](#cut)
- [`paste`](#paste)
- [`sort`](#sort)
- [`uniq`](#uniq)
- [`awk`](#awk)
- [`tr`](#tr)
- [`fold`](#fold)
- [`sed`](#sed)
- [Real-life examples](#real-life-examples)
- [Going further: `for` loops and `xargs`](#going-further-for-loops-and-xargs)
- [Summary](#summary)
- [Going further](#going-further)

<!-- /MarkdownTOC -->



# Text processing in the shell

One of the things that makes the shell an invaluable tool is the amount
of available text processing commands, and the ability to easily pipe
them into each other to build complex text processing workflows. These
commands can make it trivial to perform text and data analysis, convert
data between different formats, filter lines, etc.

When working with text data, the philosophy is to break any complex
problem you have into a set of smaller ones, and to solve each of them
with a specialized tool.

> Make each program do one thing well.[^1]

The examples in that chapter might seem a little contrived at first, but
this is also by design. Each one of these tools was designed to solve one
small problem. They however become extremely powerful when combined.

We will go over some of the most common and useful text processing
commands the shell has to offer, and will demonstrate real-life
workflows piping them together. I suggest you take a look at the `man`
of these commands to see the full breadth of options at your disposal.

<div class="Note" markdown="1">

The example CSV (comma-separated values) file is available online.[^2]
Feel free to download it yourself to test these commands.

</div>

<a id="cat"></a>
## `cat`

As seen in the previous chapter, `cat` is used to concatenate a list of
one or more files and displays their content on screen.

``` extbash
$ cat Documents/readme
Thanks again for reading this book!
I hope you're following so far!

$ cat Documents/computers
Computers are not intelligent
They're just fast at making dumb things.
$ cat Documents/readme Documents/computers
Thanks again for reading this book!
I hope you are following so far!

Computers are not intelligent
They're just fast at making dumb things.
```

<a id="head"></a>
## `head`

`head` prints the first n lines in a file. It can be very useful to peek
into a file of unknown structure and format without burying your shell
under a wall of text.

``` extbash
$ head -n 2 metadata.csv
metric_name,metric_type,interval,unit_name,per_unit_name,description,orientation,integration,short_name
mysql.galera.wsrep_cluster_size,gauge,,node,,The current number of nodes in the Galera cluster.,0,mysql,galera cluster size
```

If `-n` is unspecified, `head` will print the first 10 lines in its
argument file or input stream.

<a id="tail"></a>
## `tail`

`tail` is `head`’s counterpart. It prints the last n lines in a file.

``` extbash
$ tail -n 1 metadata.csv
mysql.performance.queries,gauge,,query,second,The rate of queries.,0,mysql,queries
```

If you want to print all lines in a file located after the nth line
(included), you can use the `-n +n` argument.

``` extbash
$ tail -n +42 metadata.csv
mysql.replication.slaves_connected,gauge,,,,Number of slaves connected to a replication master.,0,mysql,slaves connected
mysql.performance.queries,gauge,,query,second,The rate of queries.,0,mysql,queries
```

Our file has 43 lines, so `tail -n +42` only prints the 42nd and 43rd
line in our file.

If `-n` is unspecified, `tail` will print the last 10 lines in its
argument file or input stream.

`tail -f` or `tail --follow` displays the last lines in a file and
displays each new line as the file is being written to. It is very
useful to see real time activity that is written to a log file, for
example a web server log file, etc.

<a id="wc"></a>
## `wc`

`wc` (for *word count*) prints either the number of characters (when
using `-c`), words (when using `-w`) or lines (when using `-l`) in its
argument files or input stream.

``` extbash
$ wc -l metadata.csv
43  metadata.csv
$ wc -w metadata.csv
405 metadata.csv
$ wc -c metadata.csv
5094 metadata.csv
```

By default, `wc` prints all of the above.

``` extbash
$ wc metadata.csv
43     405    5094 metadata.csv
```

Only the count will be printed out if the text data is piped in or
redirected into `stdin`.

``` extbash
$ cat metadata.csv | wc
43     405    5094
$ cat metadata.csv | wc -l
43
$ wc -w < metadata.csv
405
```

<a id="grep"></a>
## `grep`

`grep` is the Swiss Army knife of line filtering. It allows you to
filter lines matching a given pattern.

For example, we can use `grep` to find all occurrences of the word
*mutex* in our `metadata.csv` file.

``` extbash
$ grep mutex metadata.csv
mysql.innodb.mutex_os_waits,gauge,,event,second,The rate of mutex OS waits.,0,mysql,mutex os waits
mysql.innodb.mutex_spin_rounds,gauge,,event,second,The rate of mutex spin rounds.,0,mysql,mutex spin rounds
mysql.innodb.mutex_spin_waits,gauge,,event,second,The rate of mutex spin waits.,0,mysql,mutex spin waits
```

`grep` can either filter files passed as arguments, or a stream of text passed
to its `stdin`. We can thus chain multiple `grep` commands to further
filter our text. In the next example, we filter lines in our
`metadata.csv` file that contain both the *mutex* and *OS* words.

``` extbash
$ grep mutex metadata.csv | grep OS
mysql.innodb.mutex_os_waits,gauge,,event,second,The rate of mutex OS waits.,0,mysql,mutex os waits
```

Let’s go over some of the options you can pass to grep and their
associated behavior.

`grep -v` performs an invert matching: it filters the lines that do
*not* match the argument pattern.

``` extbash
$ grep -v gauge metadata.csv
metric_name,metric_type,interval,unit_name,per_unit_name,description,orientation,integration,short_name
```

`grep -i` performs a case-insensitive matching. In the next example
`grep -i os` matches both *OS* and *os*.

``` extbash
$ grep -i os metadata.csv
mysql.innodb.mutex_os_waits,gauge,,event,second,The rate of mutex OS waits.,0,mysql,mutex os waits
mysql.innodb.os_log_fsyncs,gauge,,write,second,The rate of fsync writes to the log file.,0,mysql,log fsyncs
```

`grep -l` only lists files containing a match.

``` extbash
$ grep -l mysql metadata.csv
metadata.csv
```

`grep -c` counts the number of times a pattern was found.

``` extbash
$ grep -c select metadata.csv
3
```

`grep -r` recursively searches files in the current working directory
and all subdirectories below it.

``` extbash
$ grep -r are ~/Documents
/home/br/Documents/computers:Computers are not intelligent
/home/br/Documents/readme:I hope you are following so far!
```

`grep -w` only matches whole words.

``` extbash
$ grep follow ~/Documents/readme
I hope you are following so far!
$ grep -w follow ~/Documents/readme
$
```

<a id="cut"></a>
## `cut`

`cut` cuts out a portion of a file (or, as always, its input stream).
`cut` works by defining a field delimited (what separates two columns)
with the `-d` option, and what column(s) should be extracted, with the
`-f` option.

For example, the following command extracts the first column of the last
5 lines our CSV file.

``` extbash
$ tail -n 5 metadata.csv | cut -d , -f 1
mysql.performance.user_time
mysql.replication.seconds_behind_master
mysql.replication.slave_running
mysql.replication.slaves_connected
mysql.performance.queries
```

As we are dealing with a CSV file, we can extract each column by cutting
over the `,` character, and extract the first column with `-f 1`.

We could also select both the first and second columns by using the
`-f 1,2` option.

``` extbash
$ tail -n 5 metadata.csv | cut -d , -f 1,2
mysql.performance.user_time,gauge
mysql.replication.seconds_behind_master,gauge
mysql.replication.slave_running,gauge
mysql.replication.slaves_connected,gauge
mysql.performance.queries,gauge
```

<a id="paste"></a>
## `paste`

`paste` can merge together two different files into one multi-column
file.

``` extbash
$ cat ingredients
eggs
milk
butter
tomatoes
$ cat prices
1$
1.99$
1.50$
2$/kg
$ paste ingredients prices
eggs    1$
milk    1.99$
butter  1.50$
tomatoes    2$/kg
```

By default, `paste` uses a tab delimiter, but you can change that using
the `-d` option.

``` extbash
$ paste ingredients prices -d:
eggs:1$
milk:1.99$
butter:1.50$
tomatoes:2$/kg
```

Another common use of `paste` it to join all lines within a stream or a
file using a given delimiter, using a combination of the `-s` and `-d`
argument.

``` extbash
$ paste -s -d, ingredients
eggs,milk,butter,tomatoes
```

If `-` is specified as an input file, `stdin` will be read instead.

``` extbash
$ cat ingredients | paste -s -d, -
eggs,milk,butter,tomatoes
```

<a id="sort"></a>
## `sort`

`sort`, well, sorts argument files or input.

``` extbash
$ cat ingredients
eggs
milk
butter
tomatoes
salt
$ sort ingredients
butter
eggs
milk
salt
tomatoes
```

`sort -r` performs a reverse sort.

``` extbash
$ sort -r ingredients
tomatoes
salt
milk
eggs
butter
```

`sort -n` performs a numerical sort, by sorting fields by their
arithmetic value.

``` extbash
$ cat numbers
0
2
1
10
3
$ sort numbers
0
1
10
2
3
$ sort -n numbers
0
1
2
3
10
```

<a id="uniq"></a>
## `uniq`

`uniq` detects or filters out adjacent identical lines in its argument
file or input stream.

``` extbash
$ cat duplicates
and one
and one
and two
and one
and two
and one, two, three
$ uniq duplicates
and one
and two
and one
and two
and one, two, three
```

As `uniq` only filters out *adjacent* identical lines, we can still see
more than one unique lines in its output. To filter out all identical
lines from our `duplicates` file, we need to sort its content first.

``` extbash
$ sort duplicates | uniq
and one
and one, two, three
and two
```

`uniq -c` prepends all lines with its number of occurrences.

``` extbash
$ sort duplicates | uniq -c
   3 and one
   1 and one, two, three
   2 and two
```

`uniq -u` only displays the unique lines within its input.

``` extbash
$ sort duplicates | uniq -u
and one, two, three
```

<div class="Note" markdown="1">

`uniq` is particularly useful used in conjunction with `sort`, as
`| sort | uniq` allows you to remove any duplicate line in a file or a
stream.

</div>

<a id="awk"></a>
## `awk`

`awk` is a little more than a text processing tool: it’s actually a
whole programming language of its own[^3]. One thing `awk` is *really*
good at is splitting files into columns, and it especially shines when
these files contain a mix and match of spaces and tabs.

``` extbash
$ cat -t multi-columns
John Smith    Doctor^ITardis
Sarah-James Smith^I    Companion^ILondon
Rose Tyler   Companion^ILondon
```

<div class="Note" markdown="1">

`cat -t` displays tabs as `^I`.

</div>

We can see that these columns are either separated by spaces or tabs,
and that they are not always separated by the same number of spaces.
`cut` would be of no use there, because it only works on a single
character delimiter. `awk` however, can easily make sense of that file.

`awk '{ print $n }'` prints the nth column in the text.

``` extbash
$ cat multi-columns | awk '{ print $1 }'
John
Sarah-James
Rose
$ cat multi-columns | awk '{ print $3 }'
Doctor
Companion
Companion
$ cat multi-columns | awk '{ print $1,$2 }'
John Smith
Sarah-James Smith
Rose Tyler
```

There is so much more we can do with `awk`, however, printing columns
probably accounts for 99% of my personal usage.

<div class="Note" markdown="1">

`{ print $NF }` prints the last column in the line.

</div>

<a id="tr"></a>
## `tr`

`tr` stands for *translate*, and it replaces characters into others. It
either works on characters or character *classes*, such as lowercase,
printable, spaces, alphanumeric, etc.

`tr <char1> <char2>` translates all occurrences of `<char1>` from its
standard input into `<char2>`.

``` extbash
$ echo "Computers are fast" | tr a A
computers Are fAst
```

`tr` can also translate character classes by using the `[:class:]`
notation. The full list of available classes is described in the `tr`
man page, but we’ll demonstrate some of them here.

`[:space:]` represent all types of spaces, from a simple space, to a tab
or a newline.

``` extbash
$ echo "computers are fast" | tr '[:space:]' ','
computers,are,fast,%
```

All spaces-like characters were translated into a comma. Note that the
`%` character at the end of the output represents the lack of a trailing
newline. Indeed, that newline was translated to a comma as well.

`[:lower:]` represents all lowercase characters, and `[:upper:]`
represents all uppercase characters. Converting between cases is thus
made very easy.

``` extbash
$ echo "computers are fast" | tr '[:lower:]' '[:upper:]'
COMPUTERS ARE FAST
$ echo "COMPUTERS ARE FAST" | tr '[:upper:]' '[:lower:]'
computers are fast
```

`tr SET1 SET2` will transform any character in SET1 into the
characters in SET2. The following example replaces all vowels by
spaces.

``` extbash
$ echo "computers are fast" | tr '[aeiouy]' ' '
c mp t rs  r  f st
```

`tr -c SET1 SET2` does the opposite: it transforms any character *not* in SET1 into the
characters in SET2. The following example replaces all non vowels by
spaces.

``` extbash
$ echo "computers are fast" | tr -c '[aeiouy]' ' '
 o  u e   a e  a
```

`tr -d` deletes the matched characters, instead of replacing them. It’s
the equivalent of `tr <char> ''`.

``` extbash
$ echo "Computers Are Fast" | tr -d '[:lower:]'
C A F
```

`tr` can also replace character ranges, for example all letters between
*a* and *e*, or all numbers between 1 and 8, by using the notation
`s-e`, where `s` is the start character and `e` is the end one.

``` extbash
$ echo "computers are fast" | tr 'a-e' 'x'
xomputxrs xrx fxst
$ echo "5uch l337 5p34k" | tr '1-4' 'x'
5uch lxx7 5pxxk
```

`tr -s string1` compresses any multiple occurrences of the characters in `string1` into a single one. One of the most useful uses of `tr -s` is to replace multiple consecutive spaces by a single one.

``` extbash
$ echo "Computers         are       fast" | tr -s ' '
Computers are fast
```

<a id="fold"></a>
## `fold`

`fold` wraps each input line to fit in a specified width. It can be
useful to make sure an argument text fits in a small display size for
example. `fold -w n` folds the lines at `n` characters.

``` extbash
$ cat ~/Documents/readme | fold -w 16
Thanks again for
 reading this bo
ok!
I hope you're fo
llowing so far!
```

`fold -s` will only break lines on a space character, and can be
combined with `-w` to fold up to a given number of characters.

```
Thanks again
for reading
this book!
I hope you're
following so
far!
```

<a id="sed"></a>
## `sed`

`sed` is a non-interactive stream editor, used to perform text
transformation on its input stream, on a line-per-line basis. It can
take its output from a file our its `stdin` and will output its result
either in a file or its `stdout`.

It works by taking one or many optional *addresses*, a *function* and
*parameters*. A `sed` command thus looks like this:

    [address[,address]]function[arguments]

While `sed` can perform many functions, we will cover only substitution,
as it is probably `sed`’s most common use.

### Substituting text

A `sed` substitution command looks like this:

    s/PATTERN/REPLACEMENT/[options]


**Example**: replacing the first instance of a word for each line in a
file

``` extbash
$ cat hello
hello hello
hello world!
hi
$ cat hello | sed 's/hello/Hey I just met you/'
Hey I just met you hello
Hey I just met you world
hi
```

We can see that only the first occurrence of `hello` was replaced in the
first line. To replace *all* occurrences of `hello` in each line, we can
use the `g` (for *global*) option.

``` extbash
$ cat hello | sed 's/hello/Hey I just met you/g'
Hey I just met you Hey I just met you
Hey I just met you world
hi
```

`sed` allows you to specify any other separator than `/`, which is
especially useful to keep the command readable if the search of
replacement pattern contains forward slashes.

``` extbash
$ cat hello | sed 's@hello@Hey I just met you@g'
Hey I just met you Hey I just met you
Hey I just met you world
hi
```

By specifying an address, we can tell sed on which line or line-range to
actually perform the substitution.

``` extbash
$ cat hello | sed '1s/hello/Hey I just met you/g'
Hey I just met you hello
hello world
hi
$ cat hello | sed '2s/hello/Hey I just met you/g'
hello hello
Hey I just met you  world
hi
```

The address `1` tells `sed` to only replace `hello` by
`Hey I just met you` on line 1. We can specify an address range with the
notation `<start>,<end>` where `<end>` can either be a line number or
`$`, meaning the last line in the file.

``` extbash
$ cat hello | sed '1,2s/hello/Hey I just met you/g'
Hey I just met you Hey I just met you
Hey I just met you world
hi
$ cat hello | sed '2,3s/hello/Hey I just met you/g'
hello hello
Hey I just met you world
hi
$ cat hello | sed '2,$s/hello/Hey I just met you/g'
hello hello
Hey I just met you world
hi
```

By default, `sed` displays its result in its `stdout`, but it can also
edit the initial file in-place, with the use of the `-i` option.

``` extbash
$ sed -i '' 's/hello/Bonjour/' sed-data
$ cat sed-data
Bonjour hello
Bonjour world
hi
```

<div class="Note" markdown="1">

On Linux, only `-i` needs to be specified. However, due to the fact that
`sed`’s behavior on macOS is slightly different, the `''` needs to be
added right after `-i`.

</div>

<a id="real-life-examples"></a>
## Real-life examples

### Filtering a CSV using `grep` and `awk`

``` extbash
$ grep -w gauge metadata.csv | awk -F, '{ if ($4 == "query") { print $1, "per", $5 } }'
mysql.performance.com_delete per second
mysql.performance.com_delete_multi per second
mysql.performance.com_insert per second
mysql.performance.com_insert_select per second
mysql.performance.com_replace_select per second
mysql.performance.com_select per second
mysql.performance.com_update per second
mysql.performance.com_update_multi per second
mysql.performance.questions per second
mysql.performance.slow_queries per second
mysql.performance.queries per second
```

This example filters the lines containing the word `gauge` in our
`metadata.csv` file using `grep`, then the filters the lines with the
string `query` as their 4th column, and displays the metric name (1st
column) with its associated `per_unit_name` value (5th column).

### Printing the IPv4 address associated with a network interface

``` extbash
$ ifconfig en0 | grep inet | grep -v inet6 | awk '{ print $2 }'
192.168.0.38
```

`ifconfig <interface name>` prints details associated with the argument
network interface name. For example:

``` extbash
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
    ether 19:64:92:de:20:ba
    inet6 fe80::8a3:a1cb:56ae:7c7c%en0 prefixlen 64 secured scopeid 0x7
    inet 192.168.0.38 netmask 0xffffff00 broadcast 192.168.0.255
    nd6 options=201<PERFORMNUD,DAD>
    media: autoselect
    status: active
```

We then `grep` for `inet`, which will match 2 lines.

``` extbash
$ ifconfig en0 | grep inet
    inet6 fe80::8a3:a1cb:56ae:7c7c%en0 prefixlen 64 secured scopeid 0x7
    inet 192.168.0.38 netmask 0xffffff00 broadcast 192.168.0.255
```

We then exclude the line with `ipv6` by using a `grep -v`.

``` extbash
$ ifconfig en0 | grep inet | grep -v inet6
inet 192.168.0.38 netmask 0xffffff00 broadcast 192.168.0.255
```

We finally use `awk` to get the 2nd column in that line: the IPv4
address associated with our `en0` network interface.

``` extbash
$ ifconfig en0 | grep inet | grep -v inet6 | awk '{ print $2 }'
192.168.0.38
```

<div class="Note" markdown="1">

It has been [suggested](https://www.reddit.com/r/bash/comments/finbd2/beginner_friendly_introduction_to_the_shell_text/fki8523/?context=3) to me that `grep inet | grep -v inet6` could be replaced by the following future-proof `awk` command:


``` extbash
$ ifconfig en0 | awk ' $1 == "inet" { print $2 }'
192.168.0.38
```

It is shorter and specifically targets IPv4 using the `$1 == "inet"` condition.

</div>


### Extracting a value from a config file

``` extbash
$ grep 'editor =' ~/.gitconfig  | cut -d = -f2 | sed 's/ //g'
/usr/bin/vim
```

We look for the `editor =` value in the current user’s git configuration
file, then cut over the `=` sign, get the second column and remove any
space around that column.

``` extbash
$ grep 'editor =' ~/.gitconfig
     editor = /usr/bin/vim
$ grep 'editor =' ~/.gitconfig  | cut -d'=' -f2
 /usr/bin/vim
$ grep 'editor =' ~/.gitconfig  | cut -d'=' -f2 | sed 's/ //'
/usr/bin/vim
```

### Extracting IP addresses from a log file

The following real life example looks for the message
`Too many connections from` in a database log file (which is followed by
an IP address) and displays the 10 biggest offenders.

``` extbash
$ grep 'Too many connections from' db.log | \
  awk '{ print $12 }' | \
  sed 's@/@@' | \
  sort | \
  uniq -c | \
  sort -rn | \
  head -n 10 | \
  awk '{ print $2 }'
   10.11.112.108
   10.11.111.70
   10.11.97.57
   10.11.109.72
   10.11.116.156
   10.11.100.221
   10.11.96.242
   10.11.81.68
   10.11.99.112
   10.11.107.120
```

Let’s break down what this pipeline of command does. First, let’s look
at what a log line looks like.

``` extbash
$ grep "Too many connections from" db.log | head -n 1
2020-01-01 08:02:37,617 [myid:1] - WARN  [NIOServerCxn.Factory:1.2.3.4/1.2.3.4:2181:NIOServerCnxnFactory@193] - Too many connections from /10.11.112.108 - max is 60
```

`awk '{ print $12 }'` then extracts the IP from the line.


``` extbash
$ grep "Too many connections from" db.log | awk '{ print $12 }'
/10.11.112.108
...
```

`sed 's@/@@'` removes the trailing slash from the IPs.

``` extbash
$ grep "Too many connections from" db.log | awk '{ print $12 }' | sed 's@/@@'
10.11.112.108
...
```

<div class="Note" markdown="1">

As we have previously seen, we can use whatever separator we want for
`sed`. While `/` is commonly used as a separator, we are currently
replacing that very character, which would make the substitution
expression sightly less readable.

``` extbash
sed 's/\///'
```

</div>

`sort | uniq -c` sorts the IPs lexicographically, and then removed
duplicates while prefixing IPs by their associated number of
occurrences.

``` extbash
$ grep 'Too many connections from' db.log | \
  awk '{ print $12 }' | \
  sed 's@/@@' | \
  sort | \
  uniq -c
   1379 10.11.100.221
   1213 10.11.103.168
   1138 10.11.105.177
    946 10.11.106.213
   1211 10.11.106.4
   1326 10.11.107.120
   ...
```

`sort -rn | head -n 10` sorts the lines by the number of occurrences,
numerically and in the reversed order, which displays the biggest
offenders first, 10 of which are displayed. The final `awk { print $2 }`
extracts the IPs themselves.

``` extbash
$ grep 'Too many connections from' db.log | \
  awk '{ print $12 }' | \
  sed 's@/@@' | \
  sort | \
  uniq -c | \
  sort -rn | \
  head -n 10 | \
  awk '{ print $2 }'
  10.11.112.108
  10.11.111.70
  10.11.97.57
  10.11.109.72
  10.11.116.156
  10.11.100.221
  10.11.96.242
  10.11.81.68
  10.11.99.112
  10.11.107.120
```

### Renaming a function in a source file

Let’s imagine that we are working a code project, and we would like to
rename rename a poorly named function (or class, variable, etc) in a
code file. We can do this by using `sed -i`, which performs an in-place
replacement in a file.

``` extbash
$ cat izk/utils.py
def bool_from_str(s):
    if s.isdigit():
        return int(s) == 1
    return s.lower() in ['yes', 'true', 'y']
```

``` extbash
$ sed -i 's/def bool_from_str/def is_affirmative/' izk/utils.py
$ cat izk/utils.py
def is_affirmative(s):
    if s.isdigit():
        return int(s) == 1
    return s.lower() in ['yes', 'true', 'y']
```

<div class="Note" markdown="1">

Use `sed -i ''` instead of `sed -i` on macOs, as the `sed` version
behaves slightly differently.

</div>

We’ve however only renamed this function in the file it was defined in.
Any other file we import `bool_from_str` will now be broken, as this
function is not defined anymore. We’d need a way to rename
`bool_from_str` everywhere it is found in our project. We can achieve
just that by using `grep`, `sed`, and either `for` loops or `xargs`.

<a id="going-further-for-loops-and-xargs"></a>
## Going further: `for` loops and `xargs`

To replace all occurrences of `bool_from_str` in our project, we first
need to recursively find them using `grep -r`.

``` extbash
$ grep -r bool_from_str .
./tests/test_utils.py:from izk.utils import bool_from_str
./tests/test_utils.py:def test_bool_from_str(s, expected):
./tests/test_utils.py:    assert bool_from_str(s) == expected
./izk/utils.py:def bool_from_str(s):
./izk/prompt.py:from .utils import bool_from_str
./izk/prompt.py:                    default = bool_from_str(os.environ[envvar])
```

As we are only interested in the matching files, we also need to use the
`-l/--files-with-matches` option:

    -l, --files-with-matches
            Only the names of files containing selected lines are written to standard out-
            put.  grep will only search a file until a match has been found, making
            searches potentially less expensive.  Pathnames are listed once per file
            searched.  If the standard input is searched, the string ``(standard input)''
            is written.

``` extbash
$ grep -r --files-with-matches bool_from_str .
./tests/test_utils.py
./izk/utils.py
./izk/prompt.py
```

We can then use the `xargs` command to perform an action on each line in
the output (each file containing the `bool_from_str` string).

``` extbash
$ grep -r --files-with-matches bool_from_str . | \
  xargs -n 1 sed -i 's/bool_from_str/is_affirmative/'
```

`-n 1` tells `xargs` that each line in the output should cause a
separate `sed` command to be executed.

The following commands are then executed:

``` extbash
$ sed -i 's/bool_from_str/is_affirmative/' ./tests/test_utils.py
$ sed -i 's/bool_from_str/is_affirmative/' ./izk/utils.py
$ sed -i 's/bool_from_str/is_affirmative/' ./izk/prompt.py
```

If the command you call with `xargs` (`sed`, in our case) support
multiple arguments, you can (and shoud, as a single command will execute faster) drop the `-n 1` argument and run

``` extbash
$ grep -r --files-with-matches bool_from_str . | xargs sed -i 's/bool_from_str/is_affirmative/'
```

which will then execute

``` extbash
$ sed -i 's/bool_from_str/is_affirmative/' ./tests/test_utils.py ./izk/utils.py ./izk/prompt.py
```

<div class="Note" markdown="1">

We can see that `sed` can take multiple arguments by looking at its
synopsis, in its `man` page.

    SYNOPSIS
         sed [-Ealn] command [file ...]
         sed [-Ealn] [-e command] [-f command_file] [-i extension] [file ...]

Indeed, as we’ve seen in the previous chapter, `file ...` means that
multiple arguments representing file names are accepted.

</div>

We can see that all `bool_from_str` occurrences have been replaced.

``` extbash
$ grep -r is_affirmative .
./tests/test_utils.py:from izk.utils import is_affirmative
./tests/test_utils.py:def test_is_affirmative(s, expected):
./tests/test_utils.py:    assert is_affirmative(s) == expected
./izk/utils.py:def is_affirmative(s):
./izk/prompt.py:from .utils import is_affirmative
./izk/prompt.py:                    default = is_affirmative(os.environ[envvar])
```

As it is often the case, there are multiple ways of achieving the same
result. Instead of using `xargs`, we could have used `for` lops, which
allow you to iterate over a list of lines and perform an action on each
element. These `for` loops have the following syntax:

``` extbash
for item in list; do
    command $item
done
```

By wrapping our `grep` command by `$()`, it will cause the shell to
execute the it in a *subshell*, which result will then be iterated on by
the `for` loop.

``` extbash
$ for file in $(grep -r --files-with-matches bool_from_str .); do
  sed -i 's/bool_from_str/is_affirmative/' $file
done
```

which will execute

``` extbash
$ sed -i 's/bool_from_str/is_affirmative/' ./tests/test_utils.py
$ sed -i 's/bool_from_str/is_affirmative/' ./izk/utils.py
$ sed -i 's/bool_from_str/is_affirmative/' ./izk/prompt.py
```

I tend to find the for loop syntax clearer than `xargs`’s. `xargs` can
however execute the commands in parallel using its `-P n` options, where
`n` is the maximum number of parallel commands to be executed at a time,
which can be a performance win if your command takes time to run.

<a id="summary"></a>
## Summary

All these tools open up a world of possibilities, as they allow you to
extract data and transform its format, to make it possible to build
entire workflows of commands that were possibly never intended to work
together. Each of these commands accomplishes has a relatively small
function (`sort` sorts, `cat` concatenates, `grep` filters, `sed` edits,
`cut` cuts, etc).

Any given task involving text, can then be reduced to a pipeline of
smaller tasks, each of them performing a simple action and piping its
output into the next task.

For example, if we wanted to know how many unique IPs could be found in
a log file, and that these IPs always appeared at the same column, we
could:

-   `grep` lines on a pattern specific to lines containing an IP address
-   locate the column the IPs appear, and extract them with `awk`
-   sort the list of IPs with `sort`
-   compute the list of *unique* IPs with `uniq`
-   count the number of lines (aka, of unique IPs) with `wc -l`

As there is a plethora of text processing tools, either available by
default or installable, there is bound to be many ways to solve any
given task.

The examples in this article were contrived, but I suggest you read the
amazing article “Command-line Tools can be 235x Faster than your Hadoop
Cluster”[^4] to get a sense of how useful and powerful these text
processing commands really are, and what real-life problems they can
solve.

<a id="going-further"></a>
## Going further

**2.1**: Count the number of files and directories located in your home
directory.

**2.2**: Display the content of a file in all caps.

**2.3**: Count how many times each word was found in a file.

**2.4**: Count the number of vowels present in a file. Display the
result from the most common to the least.

[^1]: <https://homepage.cs.uri.edu/~thenry/resources/unix_art/ch01s06.html>

[^2]: <https://raw.githubusercontent.com/DataDog/integrations-core/master/mysql/metadata.csv>

[^3]: <https://www.gnu.org/software/gawk/manual/gawk.html>

[^4]: <https://adamdrake.com/command-line-tools-can-be-235x-faster-than-your-hadoop-cluster.html>


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
