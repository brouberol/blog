{% from 'note.j2' import note %}
---
Title: The Mystery of the Silent Process
Date: 2025-03-28
Category: Programming
Description: I'm reproducing my un-edited debugging notes when investigating what looked like a deadlock in production to show the process that led to fixing the issue. This article is intended to showcase how tools such as strace and a debugger are essential to my personal debugging workflow, and would probably benefit you too.
Summary: I've recently had to debug why a program in charge of regularly dumping the [Wikimedia wikis data](https://dumps.wikimedia.org/) would simply... stop, without any prior knowledge of this (rather large) codebase. I'm reproducing my (mostly) un-edited debugging notes to show the actual debugging process that led to a very simple-looking fix, and is intended to showcase how tools such as `strace` and a debugger are essential to my personal debugging workflow, and would probably benefit you too.
Tags: SRE, Python
---

I've recently had to debug why a program in charge of regularly dumping the [Wikimedia wikis data](https://dumps.wikimedia.org/) would simply... stop, without any  prior knowledge of this (rather large) codebase.

For context, we have been working on containarizing the jobs themselves, and orchesrating them via [Airflow](https://airflow.apache.org/docs/apache-airflow/stable/index.html). We haven't written the dump tools though. We're merely working on orchestrating and running them a different way. This issue was happeninig in a container while working on the migration, and to our knowledge, was not happening in the current production environment.

I'm reproducing my (mostly) un-edited notes to show the actual debugging process that led to a very simple-looking fix, and is intended to showcase how tools such as `strace` and a debugger are essential to my personal debugging workflow, and would probably benefit you too.

{{ note("The notes were left as is, so please excuse my raw style and syntax.") }}

### Debugging notes.

I've observed that the `cawiki` dump is getting stuck on:

```
[2025-03-26, 13:13:46 UTC] {pod_manager.py:496} INFO - [mediawiki-sql-xml-dump] 2025-03-26 13:08:46: cawiki ... building articles 1 XML dump, for output cawiki-20250326-pages-articles1.xml-p1500001p2154119.bz2, no text prefetch...
```
This smells like a TCP connection not being able to establish, and an unconfigured timeout..

We've hypothesized that we're missing some egress policy allowing the dumps to egress to the external storage servers.

---

The new external services rule allowing the task pod to reach out to the external storage hosts seems to have worked:

```
brouberol@dse-k8s-worker1007:~$ nsenter-containerd-container mediawiki-sql-xml-dump-cawiki-3qyib3p mediawiki-sql-xml-dump telnet 10.64.0.20 3306
Trying 10.64.0.20...
Connected to 10.64.0.20.
Escape character is '^]'.
]
5.5.5-10.6.20-MariaDB-log�3*u6IN-5�ajqw%K-?4'eGmysql_native_password^]
```
---

Looking at `dse-k8s-worker1007` on which the dump pod is currently running, I only see ingress traffic though:
```
brouberol@dse-k8s-worker1007:~$ netstat -laputen | grep -v ESTABLISHED | grep -v LISTEN | grep 10.67.30.237
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 10.64.134.5:58762       10.67.30.237:9361       TIME_WAIT   0          0          -
tcp        0      0 10.64.134.5:50156       10.67.30.237:9361       TIME_WAIT   0          0          -
tcp        0      0 10.64.134.5:49954       10.67.30.237:9361       TIME_WAIT   0          0          -
tcp        0      0 10.64.134.5:45094       10.67.30.237:9361       TIME_WAIT   0          0          -
tcp        0      0 10.64.134.5:47626       10.67.30.237:9361       TIME_WAIT   0          0          -
tcp        0      0 10.64.134.5:40532       10.67.30.237:9361       TIME_WAIT   0          0          -
```
where `10.67.30.237` is the dump pod IP.
```
brouberol@deploy1003:~$ k get pod -o wide
NAME                                             READY   STATUS    RESTARTS   AGE     IP             NODE                             NOMINATED NODE   READINESS GATES
mediawiki-dumps-legacy-toolbox-9d978bc46-f5bxl   1/1     Running   0          25h     10.67.30.219   dse-k8s-worker1007.eqiad.wmnet   <none>           <none>
mediawiki-sql-xml-dump-cawiki-et5jmr1            3/3     Running   0          7m32s   10.67.30.237   dse-k8s-worker1007.eqiad.wmnet   <none>           <none>
```
This seems to be the host (probably the kubelet or associated) trying to scrape the envoy telemetry endpoint.
```console
$ grep -r -B2 ./charts 9361
...
./charts/eventgate/values.yaml-  telemetry:
./charts/eventgate/values.yaml-    enabled: true
./charts/eventgate/values.yaml:    port: 9361
...
```
The container still seems stuck. I'm going to restart it to see if we fare better.

---

Nope, still stuck.

---
Looking at what one of the subprocess is doing via `strace`, we see some futex timeout happening every 10s, after having reset the mtime on the lockfile.

This leads me to believe that we're looking at a thread executing this:
```python
class LockWatchdog(threading.Thread):
    """Touch the given file every 10 seconds until asked to stop."""

    # For emergency aborts
    threads = []

    def __init__(self, lockfile):
        threading.Thread.__init__(self)
        self.lockfile = lockfile
        self.trigger = threading.Event()
        self.finished = threading.Event()

    def stop_watching(self):
        """Run me outside..."""
        # Ask the thread to stop...
        self.trigger.set()

        # Then wait for it, to ensure that the lock file
        # doesn't get touched again after we delete it on
        # the main thread.
        self.finished.wait(10)
        self.finished.clear()

    def run(self):
        LockWatchdog.threads.append(self)
        while not self.trigger.isSet():
            self.touch_lock() # <---
            self.trigger.wait(10) # <---
        self.trigger.clear()
        self.finished.set()
        LockWatchdog.threads.remove(self)

    def touch_lock(self):
        """Run me inside..."""
        os.utime(self.lockfile, None)
```

---

Looking at the threads themselves from `gdb`, this is looking more and more like a deadlock / infinite wait:
```php
(gdb) set pagination 0
(gdb) thread apply all bt

Thread 3 (LWP 1376698 "python3"):
#0  0x00007f12920ea174 in do_futex_wait.constprop () from target:/lib/x86_64-linux-gnu/libpthread.so.0
#1  0x00007f12920ea278 in __new_sem_wait_slow.constprop.0 () from target:/lib/x86_64-linux-gnu/libpthread.so.0
#2  0x00000000004f256f in PyThread_acquire_lock_timed ()
#3  0x00000000005451ab in ?? ()
#4  0x000000000052d7d6 in ?? ()
...
#19 0x000000000053ece1 in ?? ()
#20 0x00000000005ec5c6 in ?? ()
#21 0x00000000005dd9e4 in ?? ()
#22 0x00007f12920e0ea7 in start_thread () from target:/lib/x86_64-linux-gnu/libpthread.so.0
#23 0x00007f1291e63acf in clone () from target:/lib/x86_64-linux-gnu/libc.so.6

Thread 2 (LWP 1376697 "python3"):
#0  0x00007f12920ea388 in do_futex_wait.constprop () from target:/lib/x86_64-linux-gnu/libpthread.so.0
#1  0x00007f12920ea4b3 in __new_sem_wait_slow.constprop.0 () from target:/lib/x86_64-linux-gnu/libpthread.so.0
#2  0x00000000004f25cd in PyThread_acquire_lock_timed ()
#3  0x00000000005451ab in ?? ()
#4  0x000000000052d611 in ?? ()
...
#17 0x000000000053ece1 in ?? ()
#18 0x00000000005ec5c6 in ?? ()
#19 0x00000000005dd9e4 in ?? ()
#20 0x00007f12920e0ea7 in start_thread () from target:/lib/x86_64-linux-gnu/libpthread.so.0
#21 0x00007f1291e63acf in clone () from target:/lib/x86_64-linux-gnu/libc.so.6

Thread 1 (LWP 1376601 "python3"):
#0  0x00007f12920ea388 in do_futex_wait.constprop () from target:/lib/x86_64-linux-gnu/libpthread.so.0
#1  0x00007f12920ea4b3 in __new_sem_wait_slow.constprop.0 () from target:/lib/x86_64-linux-gnu/libpthread.so.0
#2  0x00000000004f25cd in PyThread_acquire_lock_timed ()
#3  0x00000000005451ab in ?? ()
#4  0x000000000052d611 in ?? ()
...
#35 0x00000000005128e3 in PyEval_EvalCode ()
#36 0x00000000006497b7 in ?? ()
#37 0x0000000000646a30 in ?? ()
#38 0x0000000000649749 in ?? ()
#39 0x00000000006493e6 in PyRun_SimpleFileExFlags ()
#40 0x0000000000640223 in Py_RunMain ()
#41 0x0000000000629ea9 in Py_BytesMain ()
#42 0x00007f1291d8bd7a in __libc_start_main () from target:/lib/x86_64-linux-gnu/libc.so.6
#43 0x0000000000629daa in _start ()
```
Note that the stack cannot be properly detailed as `gdb` does not belong to the same file namespace as the running processes. We'd need to install `gdb` in the image to be able to know more, which I'm not super keen on.

---

Let's slightly modify the code so that SIGUSR2 causes it to break into `pdb` instead.

---

We start by sending a SIGUSR2 signal to the stuck dumps process, which gets us in a debugger:
```python
--Return--
> /srv/deployment/dumps/xmldumps-backup/worker.py(23)handle_sigusr2()->None
-> breakpoint()
(Pdb) u
> /usr/lib/python3.9/threading.py(316)wait()
-> gotit = waiter.acquire(True, timeout)
(Pdb) w
  /usr/lib/python3.9/runpy.py(197)_run_module_as_main()
-> return _run_code(code, main_globals, None,
  /usr/lib/python3.9/runpy.py(87)_run_code()
-> exec(code, run_globals)
  /usr/lib/python3.9/pdb.py(1732)<module>()
-> pdb.main()
  /usr/lib/python3.9/pdb.py(1705)main()
-> pdb._runscript(mainpyfile)
  /usr/lib/python3.9/pdb.py(1573)_runscript()
-> self.run(statement)
  /usr/lib/python3.9/bdb.py(580)run()
-> exec(cmd, globals, locals)
  <string>(1)<module>()
  /srv/deployment/dumps/xmldumps-backup/worker.py(4)<module>()
-> import getopt
  /srv/deployment/dumps/xmldumps-backup/worker.py(550)main()
-> result = runner.run()
  /srv/deployment/dumps/xmldumps-backup/dumps/runner.py(599)run()
-> self.run_prereqs_and_job(item)
  /srv/deployment/dumps/xmldumps-backup/dumps/runner.py(542)run_prereqs_and_job()
-> prereq_job = self.do_run_item(item)
  /srv/deployment/dumps/xmldumps-backup/dumps/runner.py(454)do_run_item()
-> item.dump(self)
  /srv/deployment/dumps/xmldumps-backup/dumps/jobs.py(190)dump()
-> done = self.run(runner)
  /srv/deployment/dumps/xmldumps-backup/dumps/xmlcontentjobs.py(886)run()
-> self.stubber.run_temp_stub_commands(runner, commands, batchsize)
  /srv/deployment/dumps/xmldumps-backup/dumps/stubprovider.py(138)run_temp_stub_commands()
-> error, broken_pipelines = runner.run_command_without_errorcheck(command_batch)
  /srv/deployment/dumps/xmldumps-backup/dumps/runner.py(397)run_command_without_errorcheck()
-> commands.run_commands()
  /srv/deployment/dumps/xmldumps-backup/dumps/commandmanagement.py(644)run_commands()
-> self.watch_output_queue()
  /srv/deployment/dumps/xmldumps-backup/dumps/commandmanagement.py(620)watch_output_queue()
-> output = self._output_queue.get(True, 1)
  /usr/lib/python3.9/queue.py(180)get()
-> self.not_empty.wait(remaining)
> /usr/lib/python3.9/threading.py(316)wait()
-> gotit = waiter.acquire(True, timeout)
  /srv/deployment/dumps/xmldumps-backup/worker.py(23)handle_sigusr2()->None
-> breakpoint()
```
so, if we scan this stack, we see that we're basically waiting on a queue, while running some kind of command
```python
-> commands.run_commands()
  /srv/deployment/dumps/xmldumps-backup/dumps/commandmanagement.py(644)run_commands()
-> self.watch_output_queue()
  /srv/deployment/dumps/xmldumps-backup/dumps/commandmanagement.py(620)watch_output_queue()
-> output = self._output_queue.get(True, 1)
  /usr/lib/python3.9/queue.py(180)get()
```
What I'm always interested in is the boundary of the code I control, aka the last couple of frames before it goes to cpython itself. Here, it's
```python
  /srv/deployment/dumps/xmldumps-backup/dumps/commandmanagement.py(620)watch_output_queue()
-> output = self._output_queue.get(True, 1)
(Pdb) n
_queue.Empty
```

Ah, here we are
```python
def watch_output_queue(self):
    done = False
    while not done:
        # check the number of threads active, if they are all gone we are done
        if threading.activeCount() == self._normal_thread_count:
            done = True
        output = None
        try:
            output = self._output_queue.get(True, 1)
        except Exception as ex:
            pass
        if output:
            # <snip>

(Pdb) threading.activeCount()
3
(Pdb) self._normal_thread_count
3
(Pdb) threading.enumerate()
[<_MainThread(MainThread, started 140474817730368)>, <LockWatchdog(Thread-1, started daemon 140474798417664)>, <Logger(Thread-2, started daemon 140474790024960)>]
```
we see here that we're going to exit this `watch_ouptut_queue` method, as the queue is empty, and that we have the expected number of threads. And indeed, we do, and go back to the caller frame, which is here.
```python
@staticmethod
def run_temp_stub_commands(runner, commands, batchsize):
    """
    run the commands to generate the temp stub files, without
    output file checking
    """
    errors = False

    while commands:
        command_batch = commands[:batchsize]
        error, broken_pipelines = runner.run_command_without_errorcheck(command_batch)
        # <<<<we get here>>>>
        if error:
           #  <snip, we don't have any error>

        commands = commands[batchsize:]
    if errors:
        raise BackupError("failed to write pagerange stub files")
```
ok, so that looks like a while loop, but it has an exit condition, so why is is running in circles?

let's dumb the code down a bit
```python
while things:
    thing_batch = things[:batchsize]
    do_something_with_thing(thing_batch)
    things = things[batchsize:]

```
ok, so for example, if we have `things = [1, 2, 3, 4]` and `batchsize = 2`, we get
```python
things_batch = [1, 2]
do_something_with_thing_batch([1, 2])
things = [3, 4]
things_batch = [3, 4]
do_something_with_thing_batch([3, 4])
things = []
# done
```
ok, ok, so let's have a look at `batchsize` then:
```python
(Pdb) batchsize
0
```
Huh. Now, let's see how things go downhill from there.
```python
(Pdb) !commands
[[[['/bin/gzip', '-dc', '/mnt/dumpsdata/xmldatadumps/public/cawiki/20250327/cawiki-20250327-stub-articles1.xml.gz'], ['/usr/local/bin/writeuptopageid', '--odir', '/mnt/dumpsdata/xmldatadumps/temp/c/cawiki', '--fspecs', 'cawiki-20250327-stub-articles1.xml-p1p1500000.gz:1:1500001;cawiki-20250327-stub-articles1.xml-p1500001p2154308.gz:1500001:2154309']]]]
(Pdb) commands[:0]
[]
```
ok so `command_batch` is empty, so we give an empty list to the command runner, basically twiddling itself for 1s, and then we get this
```python
commands = commands[batchsize:]
```
which is equivalent to `commands = commands[0:]`, itself equivalent to `commands = commands`

So there you have it, your infinite loop doing nothing.

Now, why does `batchsize = 0` in the first place?

we see in `xmlcontentjobs.py`:
```python
# figure out how many stub input files we generate at once
batchsize = self.get_batchsize(stubs=True)

commands, output_dfnames = self.stubber.get_commands_for_temp_stubs(to_generate, runner)

worker_type = self.doing_batch_jobs(runner)

# secondary batch workers should not generate temp stubs, that should
# be done only if we run without batches or by the primary worker
if worker_type != 'secondary_batches':
    self.stubber.run_temp_stub_commands(runner, commands, batchsize)
```
ok, so we call `self.get_batchsize(stubs=True)`.
```python
def get_batchsize(self, stubs=False):
    """
    figure out how many commands we run at once for generating
    temp stubs
    """
    if self._pages_per_part:
        if stubs:
            # these jobs are more expensive than e.g. page content jobs,
            # do half as many
            batchsize = int(len(self._pages_per_part) / 2)
        else:
            batchsize = len(self._pages_per_part)
    else:
        batchsize = 1
    return batchsize
```
Note: `self._pages_per_part is [0],` so we end up executing `batchsize = int(len(self._pages_per_part) / 2)` => `batchsize = int(1 / 2)` => `batchsize = 0`

What we need is this:
```diff
diff --git a/xmldumps-backup/dumps/xmlcontentjobs.py b/xmldumps-backup/dumps/xmlcontentjobs.py
index bf87626..ae30be6 100644
--- a/xmldumps-backup/dumps/xmlcontentjobs.py
+++ b/xmldumps-backup/dumps/xmlcontentjobs.py
@@ -553,7 +553,7 @@ class XmlDump(Dump):
                 batchsize = len(self._pages_per_part)
         else:
             batchsize = 1
-        return batchsize
+        return batchsize if batchsize > 0 else 1

     def get_commands_for_pagecontent(self, wanted, runner):
```

---

Actually, my last message was missing the larger picture. I was tired and a bit strapped for time.

While the fix is (IMO) valid, the real question was: why was `self._pages_for_part = 0` ? To answer that question, we go back to the debugger, and set a breakpoint where the `XmlDump` object was instanciated.
```python
# dumps/xmlcontentjobs,py

class XmlDump(Dump):
    """Primary XML dumps, one section at a time."""
    def __init__(self, subset, name, desc, detail, item_for_stubs, item_for_stubs_recombine,
                 prefetch, prefetchdate, spawn,
                 wiki, partnum_todo, pages_per_part=None, checkpoints=False, checkpoint_file=None,
                 page_id_range=None, numbatches=0, verbose=False):
        self.jobinfo = {'subset': subset, 'detail': detail, 'desc': desc,
                        'prefetch': prefetch, 'prefetchdate': prefetchdate,
                        'spawn': spawn, 'partnum_todo': partnum_todo,
                        'pageid_range': page_id_range, 'item_for_stubs': item_for_stubs}
        if checkpoints:
            self._checkpoints_enabled = True
        self.checkpoint_file = checkpoint_file
        self._pages_per_part = pages_per_part
        [ BREAKPOINT ]
        if self._pages_per_part:
            self._parts_enabled = True
            self.onlyparts = True

        self.wiki = wiki
        self.verbose = verbose
        self._prerequisite_items = [self.jobinfo['item_for_stubs']]
        if item_for_stubs_recombine is not None:
            self._prerequisite_items.append(item_for_stubs_recombine)
```

```python
-> if self._pages_per_part:
(Pdb) l
138  	                        'pageid_range': page_id_range, 'item_for_stubs': item_for_stubs}
139  	        if checkpoints:
140  	            self._checkpoints_enabled = True
141  	        self.checkpoint_file = checkpoint_file
142  	        self._pages_per_part = pages_per_part
143 B->	        if self._pages_per_part:
144  	            self._parts_enabled = True
145  	            self.onlyparts = True
146
147  	        self.wiki = wiki
148  	        self.verbose = verbose
(Pdb) pages_per_part
[0]
```
Let's go a frame up, to see what passed `pages_per_part = [0]` to the constructor.
```python
(Pdb) u
> /srv/deployment/dumps/xmldumps-backup/dumps/dumpitemlist.py(179)__init__()
-> XmlDump("articles",
(Pdb) l
174
175  	        # NOTE that _pages_per_filepart_history passed here should be the same
176  	        # as the stubs job, since these files get generated from the stubs
177  	        if self.find_item_by_name('xmlstubsdump') is not None:
178  	            self.append_job_if_needed(
179  ->	                XmlDump("articles",
180  	                        "articlesdump",
181  	                        "<big><b>Articles, templates, media/file descriptions, " +
182  	                        "and primary meta-pages.</b></big>",
183  	                        "This contains current versions of article content, " +
184  	                        "and is the archive most mirror sites will probably want.",
(Pdb) l
185  	                        self.find_item_by_name('xmlstubsdump'),
186  	                        None,
187  	                        self._prefetch, self._prefetchdate, self._spawn,
188  	                        self.wiki, self._get_partnum_todo("articlesdump"),
189  	                        self.filepart.get_attr('_pages_per_filepart_history'), checkpoints,
190  	                        self.checkpoint_file, self.page_id_range, self.numbatches, self.verbose))
191
192  	        if self.find_item_by_name('articlesdump') is not None:
193  	            self.append_job_if_needed(
194  	                RecombineXmlDump(
195  	                    "articlesdumprecombine",
(Pdb) self.filepart.get_attr('_pages_per_filepart_history')
[0]
```
Ok, so now, let's have a look at what `self.filepart` is.
```python
(Pdb) self.filepart
<dumps.utils.FilePartInfo object at 0x7fd02d8a5190>

Let's now have a look at the FilePartInfo class itself.

class FilePartInfo():
    #<snip>
    def init_for_parts(self):
        self._pages_per_filepart_history = self.convert_comma_sep( # <--- OK, this is interesting
            self.wiki.config.pages_per_filepart_history)
        self._revs_per_filepart_history = self.convert_comma_sep(
            self.wiki.config.revs_per_filepart_history)
        self._recombine_metacurrent = self.wiki.config.recombine_metacurrent
        self._recombine_history = self.wiki.config.recombine_history
```
Going back to our debugger now.
```python
(Pdb) self.filepart.wiki.config.pages_per_filepart_history
'0'
(Pdb) self.filepart.convert_comma_sep(self.filepart.wiki.config.pages_per_filepart_history)
[0]
```
Ok, so this might be a configuration issue after all. Let's find where the `Wiki` object itself was instantiated.
```python
(Pdb) u
> /srv/deployment/dumps/xmldumps-backup/dumps/runner.py(241)__init__()
-> self.dump_item_list = DumpItemList(self.wiki, self.prefetch, self.prefetchdate,
(Pdb) l
236  	        self.dumpjobdata = DumpRunJobData(self.wiki, self.dump_dir, notice,
237  	                                          self.log_and_print, self.debug, self.enabled,
238  	                                          self.verbose)
239
240  	        # some or all of these dump_items will be marked to run
241  ->	        self.dump_item_list = DumpItemList(self.wiki, self.prefetch, self.prefetchdate,
242  	                                           self.spawn,
243  	                                           self._partnum_todo, self.checkpoint_file,
244  	                                           self.job_requested, self.skip_jobs,
245  	                                           self.filepart_info, self.page_id_range,
246  	                                           self.dumpjobdata, self.dump_dir,
(Pdb) u
> /srv/deployment/dumps/xmldumps-backup/worker.py(545)main()
-> runner = Runner(wiki, prefetch, prefetchdate, spawn, None, skip_jobs,
(Pdb) l
540  	            else:
541  	                sys.stderr.write("Running %s...\n" % wiki.db_name)
542
543  	            # no specific jobs requested, runner will do them all
544  	            if not jobs_todo:
545  ->	                runner = Runner(wiki, prefetch, prefetchdate, spawn, None, skip_jobs,
546  	                                restart, html_notice, dryrun, enabled,
547  	                                partnum_todo, checkpoint_file, page_id_range, skipdone,
548  	                                cleanup_files, do_prereqs, batchworker, numbatches, verbose)
549
550  	                result = runner.run()
```
Ok, we've made our way up to `worker.py`, which is our main script. Let's exit the debugger, and restart the process, this time stepping into the code as soon as possible, within `worker.py:main()`.
```python
www-data@mediawiki-dumps-legacy-toolbox-5b847f4557-mkxds:/$ python3 -m pdb /srv/deployment/dumps/xmldumps-backup/worker.py --configfile /etc/dumps/confs/wikidump.conf.dumps:bigwikis --log --skipdone --exclusive --date last cawiki
> /srv/deployment/dumps/xmldumps-backup/worker.py(4)<module>()
-> import getopt
(Pdb) b 458
Breakpoint 1 at /srv/deployment/dumps/xmldumps-backup/worker.py:458
(Pdb) c
> /srv/deployment/dumps/xmldumps-backup/worker.py(458)main()
-> if remainder:
(Pdb) l
453  	        if dryrun:
454  	            print("***")
455  	            print("Dry run only, no files will be updated.")
456  	            print("***")
457
458 B->	        if remainder:
459  	            wiki = Wiki(config, remainder[0])
460  	            if cutoff:
461  	                # fixme if we asked for a specific job then check that job only
462  	                # not the dir
463  	                last_ran = wiki.latest_dump()
(Pdb) remainder
['cawiki']
(Pdb) n
> /srv/deployment/dumps/xmldumps-backup/worker.py(459)main()
-> wiki = Wiki(config, remainder[0])
(Pdb) pp config
<dumps.wikidump.Config object at 0x7f1de3d88160>
```
We're really close now. What matters is the `config` object.
```python
www-data@mediawiki-dumps-legacy-toolbox-5b847f4557-mkxds:/$ python3 -m pdb /srv/deployment/dumps/xmldumps-backup/worker.py --configfile /etc/dumps/confs/wikidump.conf.dumps:bigwikis --log --skipdone --exclusive --date last cawiki
> /srv/deployment/dumps/xmldumps-backup/worker.py(4)<module>()
-> import getopt
(Pdb) b 416
Breakpoint 1 at /srv/deployment/dumps/xmldumps-backup/worker.py:416
(Pdb) c
> /srv/deployment/dumps/xmldumps-backup/worker.py(416)main()
-> if config_file:
(Pdb) l
411  	            skip_jobs = []
412  	        else:
413  	            skip_jobs = skip_jobs.split(",")
414
415  	        # allow alternate config file
416 B->	        if config_file:
417  	            config = Config(config_file)
418  	        else:
419  	            config = Config()
420  	        externals = ['php', 'mysql', 'mysqldump', 'head', 'tail',
421  	                     'checkforbz2footer', 'grep', 'gzip', 'bzip2',
(Pdb) config_file
'/etc/dumps/confs/wikidump.conf.dumps:bigwikis'
(Pdb) s
> /srv/deployment/dumps/xmldumps-backup/worker.py(417)main()
-> config = Config(config_file)
(Pdb) s
--Call--
> /srv/deployment/dumps/xmldumps-backup/dumps/wikidump.py(106)__init__()
-> def __init__(self, config_file=None):
(Pdb) l
101  	class Config(ConfigParsing):
102  	    """
103  	    management of general config settings and
104  	    potentially specific settings for a given wiki
105  	    """
106  ->	    def __init__(self, config_file=None):
107  	        super().__init__()
108  	        self.script_dirname = os.path.abspath(os.path.dirname(sys.argv[0]))
109  	        if config_file and ':' in config_file:
110  	            config_file, self.override_section = config_file.split(':')
```
Skimming the `Config` class, I see:
```python
def parse_conffile_per_project(self, project_name=None):
       ...
       self.pages_per_filepart_history = self.get_opt_for_proj_or_default(
           "chunks", "pagesPerChunkHistory", 0)
       ...
```
Stepping in there, we end up here.
```python
> /srv/deployment/dumps/xmldumps-backup/dumps/wikidump.py(48)get_opt_from_sections()
-> if is_int:
(Pdb) l
 43  	                continue
 44  	            if not self.conf.has_section(section):
 45  	                continue
 46  	            if not self.conf.has_option(section, item_name):
 47  	                continue
 48  ->	            if is_int:
 49  	                return self.conf.getint(section, item_name)
 50  	            return self.conf.get(section, item_name)
 51  	        return None
 52
 53  	    def get_opt_in_overrides_or_default(self, section_name, item_name, is_int):
(Pdb) n
> /srv/deployment/dumps/xmldumps-backup/dumps/wikidump.py(50)get_opt_from_sections()
-> return self.conf.get(section, item_name)
(Pdb) self.conf.get(section, item_name)
'0'
(Pdb) section
'chunks'
(Pdb) item_name
'pagesPerChunkHistory'
(Pdb) pp self.conf._sections['chunks']
{'checkpointtime': '0',
 'chunksenabled': '0',
 'chunksforpagelogs': '0',
 'contentbatchesenabled': '0',
 'jobsperbatch': '',
 'lbzip2threads': '0',
 'logitemsperpagelogs': '0',
 'maxrevbytes': '35000000000',
 'pagesperchunkhistory': '0',
 'recombinehistory': '1',
 'recombinemetacurrent': '1',
 'retrywait': '30',
 'revinfostash': '0',
 'revsmargin': '100',
 'revsperchunkhistory': '0',
 'revsperjob': '1000000',
 'testsleep': '0'}
```
What I'm noticing here is that we don't have these ^ configuration values in the chunks section of `/etc/dumps/confs/wikidumps.conf.dumps`. We have
```ini
...
[chunks]
chunksEnabled=0
retryWait=30
...
```
However, we do have these in `/srv/deployment/dumps/xmldumps-backup/defaults.conf`:
```ini
...
[chunks]
chunksEnabled=0
recombineMetaCurrent=1
recombineHistory=1
checkpointTime=0
pagesPerChunkHistory=0
revsPerChunkHistory=0
chunksForPagelogs=0
logitemsPerPagelogs=0
jobsperbatch=
revsPerJob=1000000
retryWait=30
revsMargin=100
# 35 GB uncompressed in one page content file is plenty
maxrevbytes=35000000000
lbzip2threads=0
revinfostash=0
testsleep=0
contentbatchesEnabled=0
...
```
So, `self.conf` seems to act as an overlay of the `/etc/config/dumps/wikidumps.conf.dumps` on top of `defaults.conf`. That takes us to the `Config` class itself.
```python
-> self.conf.read(self.files)
(Pdb) l
121  	                                           ".wikidump.conf"))
122
123  	        self.conf = configparser.ConfigParser(strict=False)
124  	        with open(os.path.join(self.script_dirname, 'defaults.conf')) as defaults_fp:
125  	            self.conf.read_file(defaults_fp)
126 B->	        self.conf.read(self.files)
127
128  	        if not self.conf.has_section("wiki"):
129  	            print("The mandatory configuration section 'wiki' was not defined.")
130  	            raise configparser.NoSectionError('wiki')
131
```
At this point, `self.conf` has already loaded the defaults:
```python
(Pdb) pp self.conf._sections
{'chunks': {'checkpointtime': '0',
            'chunksenabled': '0',
            'chunksforpagelogs': '0',
            'contentbatchesenabled': '0',
            'jobsperbatch': '',
            'lbzip2threads': '0',
            'logitemsperpagelogs': '0',
            'maxrevbytes': '35000000000',
            'pagesperchunkhistory': '0',
            'recombinehistory': '1',
            'recombinemetacurrent': '1',
            'retrywait': '30',
            'revinfostash': '0',
            'revsmargin': '100',
            'revsperchunkhistory': '0',
            'revsperjob': '1000000',
            'testsleep': '0'},
 'cleanup': {'keep': '3'},
...
```
Once on line 128, we have the config overlay:
```python
(Pdb) self.conf._sections['bigwikis']
{'checkpointtime': '720', 'chunksenabled': '1', 'chunksforabstract': '6', 'chunksforpagelogs': '6', 'dblist': '/etc/dumps/dblists/bigwikis.dblist', 'fixeddumporder': '1', 'keep': '8', 'lbzip2forhistory': '1', 'lbzip2threads': '6', 'recombinehistory': '0', 'revinfostash': '1', 'revsmargin': '100', 'revsperjob': '1500000', 'skipdblist': '/etc/dumps/dblists/skipnone.dblist'}
```
Let's see if we can reproduce the same behavior on a `snapshot` server now, instead of a container.
```python
brouberol@snapshot1014:/srv/deployment/dumps/dumps/xmldumps-backup$ python3 -m pdb ./worker.py --configfile /etc/dumps/confs/wikidump.conf.dumps:bigwikis --log --skipdone --date last cawiki
> /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/worker.py(4)<module>()
-> import getopt
(Pdb) b /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/wikidump.py:279
Breakpoint 1 at /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/wikidump.py:279
(Pdb) c
> /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/wikidump.py(279)parse_conffile_per_project()
-> self.numparts_for_pagelogs = self.get_opt_for_proj_or_default(
(Pdb) l
274  	            "chunks", "jobsperbatch", 0)
275  	        self.pages_per_filepart_history = self.get_opt_for_proj_or_default(
276  	            "chunks", "pagesPerChunkHistory", 0)
277  	        self.revs_per_filepart_history = self.get_opt_for_proj_or_default(
278  	            "chunks", "revsPerChunkHistory", 0)
279 B->	        self.numparts_for_pagelogs = self.get_opt_for_proj_or_default(
280  	            "chunks", "chunksForPagelogs", 0)
281  	        self.logitems_per_filepart_pagelogs = self.get_opt_for_proj_or_default(
282  	            "chunks", "logitemsPerPagelogs", 0)
283  	        self.recombine_metacurrent = self.get_opt_for_proj_or_default(
284  	            "chunks", "recombineMetaCurrent", 1)
(Pdb) self.pages_per_filepart_history
'0'
```
Samesies.

---
I'm runing a `cawiki` dump using the test config file to see whether we're affected by the same issue.
```python
brouberol@snapshot1014:/srv/deployment/dumps/dumps/xmldumps-backup$ sudo -u dumpsgen python3 -m pdb ./worker.py --configfile /etc/dumps/confs/wikidump.conf.tests:bigwikis --log --skipdone --date last cawiki
> /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/worker.py(4)<module>()
-> import getopt
(Pdb) b /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/dumpitemlist.py:179
Breakpoint 1 at /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/dumpitemlist.py:179
(Pdb) c
Running cawiki...
2025-03-28 08:12:13: cawiki Creating /mnt/dumpsdata/temp/dumpsgen/private/cawiki/20250328 ...
2025-03-28 08:12:13: cawiki Checkdir dir /mnt/dumpsdata/temp/dumpsgen/public/cawiki/20250328 ...
Couldn't update tableinfo file. Continuing anyways'
> /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/dumpitemlist.py(179)__init__()
-> XmlDump("articles",
(Pdb) l
174
175  	        # NOTE that _pages_per_filepart_history passed here should be the same
176  	        # as the stubs job, since these files get generated from the stubs
177  	        if self.find_item_by_name('xmlstubsdump') is not None:
178  	            self.append_job_if_needed(
179 B->	                XmlDump("articles",
180  	                        "articlesdump",
181  	                        "<big><b>Articles, templates, media/file descriptions, " +
182  	                        "and primary meta-pages.</b></big>",
183  	                        "This contains current versions of article content, " +
184  	                        "and is the archive most mirror sites will probably want.",
(Pdb) l
185  	                        self.find_item_by_name('xmlstubsdump'),
186  	                        None,
187  	                        self._prefetch, self._prefetchdate, self._spawn,
188  	                        self.wiki, self._get_partnum_todo("articlesdump"),
189  	                        self.filepart.get_attr('_pages_per_filepart_history'), checkpoints,
190  	                        self.checkpoint_file, self.page_id_range, self.numbatches, self.verbose))
191
192  	        if self.find_item_by_name('articlesdump') is not None:
193  	            self.append_job_if_needed(
194  	                RecombineXmlDump(
195  	                    "articlesdumprecombine",
(Pdb) self.filepart.get_attr('_pages_per_filepart_history')
[0]
```
I'm going to let it proceed until we hit the breakpoint that is located in `get_batchsize()`. If we see that it returns `0`, then we know we have the same behavior between both envs.

---

On `snapshot1014`:
```python
2025-03-28 10:33:16: cawiki Could not locate a prefetchable dump.
2025-03-28 10:33:16: cawiki ... building articles 1 XML dump, for output cawiki-20250328-pages-articles1.xml-p1p1500000.bz2, no text prefetch...
2025-03-28 10:33:16: cawiki skipping current dump for prefetch of job articlesdump, date 20250328
2025-03-28 10:33:16: cawiki Could not locate a prefetchable dump.
2025-03-28 10:33:16: cawiki ... building articles 1 XML dump, for output cawiki-20250328-pages-articles1.xml-p1500001p2154428.bz2, no text prefetch...
> /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/xmlcontentjobs.py(547)get_batchsize()
-> if self._pages_per_part:
(Pdb) self._pages_per_part
[0]
(Pdb) l
542         def get_batchsize(self, stubs=False):
543             """
544             figure out how many commands we run at once for generating
545             temp stubs
546             """
547 B->         if self._pages_per_part:
548                 if stubs:
549                     # these jobs are more expensive than e.g. page content jobs,
550                     # do half as many
551                     batchsize = int(len(self._pages_per_part) / 2)
552                 else:
(Pdb) u
> /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/xmlcontentjobs.py(877)run()
-> batchsize = self.get_batchsize(stubs=True)
(Pdb) l
872             # output file will cover the same content as its stub input
873             # file)
874             to_generate = self.get_to_generate_for_temp_stubs(wanted)
875
876             # figure out how many stub input files we generate at once
877  ->         batchsize = self.get_batchsize(stubs=True)
878
879             commands, output_dfnames = self.stubber.get_commands_for_temp_stubs(to_generate, runner)
880
881             worker_type = self.doing_batch_jobs(runner)
882
(Pdb) n
> /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/xmlcontentjobs.py(879)run()
-> commands, output_dfnames = self.stubber.get_commands_for_temp_stubs(to_generate, runner)
(Pdb) n
> /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/xmlcontentjobs.py(881)run()
-> worker_type = self.doing_batch_jobs(runner)
(Pdb) n
> /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/xmlcontentjobs.py(885)run()
-> if worker_type != 'secondary_batches':
(Pdb) n
> /srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/xmlcontentjobs.py(886)run()
-> self.stubber.run_temp_stub_commands(runner, commands, batchsize)
(Pdb) c
# hangs...
(Pdb) q
^CTraceback (most recent call last):
  File "/usr/lib/python3.9/pdb.py", line 1705, in main
    pdb._runscript(mainpyfile)
  File "/usr/lib/python3.9/pdb.py", line 1573, in _runscript
    self.run(statement)
  File "/usr/lib/python3.9/bdb.py", line 580, in run
    exec(cmd, globals, locals)
  File "<string>", line 1, in <module>
  File "/srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/worker.py", line 571, in <module>
    main()
  File "/srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/worker.py", line 538, in main
    result = runner.run()
  File "/srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/runner.py", line 599, in run
    self.run_prereqs_and_job(item)
  File "/srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/runner.py", line 542, in run_prereqs_and_job
    prereq_job = self.do_run_item(item)
  File "/srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/runner.py", line 454, in do_run_item
    item.dump(self)
  File "/srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/jobs.py", line 183, in dump
    done = self.run(runner)
  File "/srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/xmlcontentjobs.py", line 886, in run
    self.stubber.run_temp_stub_commands(runner, commands, batchsize)
  File "/srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/stubprovider.py", line 138, in run_temp_stub_commands
    error, broken_pipelines = runner.run_command_without_errorcheck(command_batch)
  File "/srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/runner.py", line 397, in run_command_without_errorcheck
    commands.run_commands()
  File "/srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/commandmanagement.py", line 644, in run_commands
    self.watch_output_queue()
  File "/srv/deployment/dumps/dumps-cache/revs/2fe1059822c2b19208c49406b92c3fc845fc614d/xmldumps-backup/dumps/commandmanagement.py", line 620, in watch_output_queue
    output = self._output_queue.get(True, 1) # Oh hello old friend
  File "/usr/lib/python3.9/queue.py", line 180, in get
    self.not_empty.wait(remaining)
  File "/usr/lib/python3.9/threading.py", line 316, in wait
    gotit = waiter.acquire(True, timeout)
```
So, this isn't an environmental issue, or a configuration issue, this is a code issue, that should get fixed by [https://gerrit.wikimedia.org/r/c/operations/dumps/+/1131781](https://gerrit.wikimedia.org/r/c/operations/dumps/+/1131781)

This is not happening in production because the batch files were previously generated and the command generating the stub files is not run.
Were we to remove them from the disk, I believe we would be seeing the same issue.