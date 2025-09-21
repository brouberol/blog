Title: The story of the 20°C cronjob
Date: 2017-05-25
Category: Programming

For the last month or so, the lifespan of my beloved Thinkpad X1 Carbon battery had been getting down the drains, from 5-6 hours to less than 3. Following [@padenot](https://twitter.com/padenot)'s advice, I installed `powertop` and started investigating what was draining this good'ol battery of mine.

Looking at the `powertop` output, I immediatly realized that something fishy was happening on this laptop:

```
The battery reports a discharge rate of 4.95 W
The estimated remaining time is 2 hours, 6 minutes

Summary: 1111.7 wakeups/second,  7.9 GPU ops/seconds, 0.0 VFS ops/sec and 23.0% CPU use

                Usage       Events/s    Category       Description
            264.4 ms/s     3656.7       Process        /bin/bash /usr/sbin/sendmail -FCronDaemon -i -odi -oem -oi -t -f br
            114.3 ms/s     626.2        Process        /usr/lib64/firefox/firefox
             20.7 ms/s      95.5        Process        /opt/sublime_text_3/plugin_host 3272
             ...
```

Why was `sendmail` so busy, and why in the hell was it running anyway? `strace` showed me that the process was indeed very busy, and `mailq` showed that I had more than 15000 outgoing emails in the system mail queue!

```
$ mailq
...
mail in dir /home/br/.esmtp_queue/TSRueRJD:
    From: "(Cron Daemon)" <br>  To: br
mail in dir /home/br/.esmtp_queue/ZI1LtzhT:
    From: "(Cron Daemon)" <br>  To: br
15653 mails to deliver
```

Ok, so all these mails were being sent by `cron`. My user crontab only had one job, and it was `* * * * * rm $HOME/crash_dump.erl`. Indeed, I had been experimenting with [Elixir](http://elixir-lang.org/) recently, and when I crashed the Erlang VM, this file would pop-up in my home directory. At some point, I added this cronjob to make it go away and forgot about it. As the job's `stdout` was not redirected to `/dev/null`, each time the file was not found, the cron job would fail and a mail would be added to the queue.

After removing this job, purging the mail queue, and adding `MAILTO=""` at [the beginning of my crontab](https://www.cyberciti.biz/faq/disable-the-mail-alert-by-crontab-command/) (to avoid repeating this investigation down the road), `sendmail` went quiet, my battery life went back to ~6 hours, and the laptop average temperature went down 20°C.