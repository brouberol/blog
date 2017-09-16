Title: Preparing the SRE interview
Date: 2017-04-20
Category: Programming

I recently interviewed for an <abbr title="Site Reliability Engineer">SRE</abbr> position. I spent a full week learning (or refreshing my memory) on the subjects and topics that could be covered in such an interview. I'll try and lay down the list of topics I covered and resources I used.

## What is an SRE?

Having spent the last 2 years employed as a DevOps, I've often felt that DevOps and SRE were two slightly differing implementations of the same ideas. The first one felt like a set of general principles, when the second one is a clear and detailed model (pre-dating DevOps), with a set of rules and guidelines. Google developed the SRE model and explained it in the [SRE book][srebook]. The underlying ideas are simple, but powerful:

* Develop tools and systems reducing toil and repetitive work from engineers
* Automate everything, or as much as possible (deployments, maintenances, tests, scaling, mitigation)
* Monitor everything
* Think scalable from the start
* Build **resilient-enough** architectures
* Handle change and risk through <abbr title="Service Level Agreement">SLA</abbr>s, <abbr title="Service Level Objective">SLO</abbr>s and <abbr title="Service Level Indicator">SLI</abbr>s
* Learn from outages

If you haven't yet read the [SRE book][srebook], I strongly urge you to do so. There's even a [free online version](https://landing.google.com/sre/book/index.html) available. If you do not have the time, then maybe have a look at this Ben Treynor (Google VP Engineering) [What is 'Site Reliability Engineering'?](https://landing.google.com/sre/interview/ben-treynor.html) interview, for a general introduction.

According to the SRE book, an SRE should spend half of its time on "ops" work, and the other half doing development.

>  Google places a 50% cap on the aggregate "ops" work for all SREs—tickets, on-call, manual tasks, etc. [...] An SRE team must spend the remaining 50% of its time actually doing development.
[Source](https://landing.google.com/sre/book/chapters/introduction.html)

Some skills are thus paramount to an SRE:

* coding / software development
* system administration and automation
* scalable system design
* system troubleshooting

Consequently, each of these areas of expertise can be (and often are) the subject of an interview.

## Coding / Software development interview

I've found that the reference resource to prepare a coding interview, especially when targeting companies like Amazon, Google, Microsoft, Yahoo, etc, is [Cracking the Coding Interview][ctci], by [Gayle Laakmann McDowell][ctci_by]. This book is a real trove of advice (technical or not) and example exercises (with the associated solutions).

Even though it is targeted to *software developer* interviews, I still covered the following topics listed in the *Must Know* section of the book:

**Data structures**:

* Linked list
* Stack
* Queue
* Heap
* Hash table
* Binary tree
* associated Big-O [time and memory complexity](http://bigocheatsheet.com/) for common operations (Search, insert, delete, etc).

I found [Data structures and Algorithms using Python and C++][dataalgo] to be useful (albeit a bit lengthy) when dealing with these data structures for the first time. This [presentation](http://www.columbia.edu/~jxz2101/#) gives a short but to-the-point, no-nonsense introduction of these data structures.

**Algorithms**

* Mergesort
* Quicksort
* Binary search

I also had a look at [https://github.com/adicu/interview_help](https://github.com/adicu/interview_help/) to practice on some real-life interview questions, and at [https://github.com/nryoung/algorithms](https://github.com/nryoung/algorithms) to read Python implementations of common data structures and algorithms.

## Scalable system design interview

This was my favorite subject to work on, as an apparently simple question such as "Design the bit.ly service" hides unexpected depths of complexity. Being able to design a scalable system implies knowing about:

* DNS
* load balancing
* micro-service architecture
* CAP theorem
* consistency patterns
* availability patterns
* databases
* caching
* asynchronism patterns
* etc

The main idea is to be able to identify the architecture bottlenecks, and to dimension the architecture with an appropriate number of machines, with some "back-of-the-envelope" calculations, whilst being robust and failure tolerant.

The most useful resources I found to prepare were:

* [Scalability lecture](https://www.youtube.com/watch?v=-W9F__D3oY4) given at Harvard
* [Latency Numbers Every Programmer Should Know](http://norvig.com/21-days.html#answers)
* [The System Design Primer](https://github.com/donnemartin/system-design-primer) (I suggest you follow the links after each section for an in-depth follow-up)
* this great [step-by-step walkthrough](https://www.hiredintech.com/classrooms/system-design/lesson/52) on design questions, by HiredInTech
* [Scaling up to your first 10 million users](https://www.youtube.com/watch?v=vg5onp8TU6Q), talk given by Joel Williams of AWS
* [Crack the design interview](http://www.puncsky.com/blog/2016/02/14/crack-the-system-design-interview/)
* [When to use NoSQL vs SQL](https://docs.microsoft.com/en-us/azure/documentdb/documentdb-nosql-vs-sql)


## System troubleshooting interview

To be able to automate the administration of a system, one should first know the said system in depth, which, in a lot of cases, will be GNU/Linux. If you have time, I strongly suggest reading [The Linux Programming Interface][tlpi]. Note that this is a **large** book (my version has 1556 pages) focusing on an old version of the Linux kernel (2.6.x). Fear not! You'll still gain a vast knowledge about how a GNU/Linux system operates. For a quicker tour, you could have a look at the [Linux Kernel Internals][linuxtour] blog. You'll also find interesting SRE interview questions/answers in this [SRE interview questions](https://syedali.net/engineer-interview-questions/) blogpost.

[Julia Evans](https://jvns.ca/), also known as [b0rk](https://twitter.com/b0rk) has written some absolutely **fantastic** beginner-friendly resources about troubleshooting and networking.
I strongly recommend having a look at:

* [the debugging zine](http://jvns.ca/debugging-zine.pdf)
* [networking! ACK!](https://jvns.ca/networking-zine.pdf)
* [How to spy on your programs with `strace`](http://jvns.ca/strace-zine-v2.pdf)

Mastering the mentioned tools (`strace`, `tcpdump`, `netstat`, `lsof`, `ngrep`, etc) gave me some good debugging chops I have applied in production many times.

Netflix has also written a very nice and thorough blogpost on performance troubleshooting: [Linux Performance Analysis in 60,000 Milliseconds](http://techblog.netflix.com/2015/11/linux-performance-analysis-in-60s.html), detailing what to check in case of a performance issue.

## Wait, there's more

Technical knowledge is one thing, but SRE being a relatively new activity, I also wanted to get real-life feedbacks from real-life SREs. To that end, I watched the following (great) talks:

* [Case Study: Adopting SRE Principles at StackOverflow](https://www.usenix.org/conference/srecon15/program/presentation/limoncelli), by Tom Limoncelli of Stack Exchange
* [Love DevOps? Wait until you meet SRE](https://www.youtube.com/watch?v=fsTpRx8Pt-k), by Nick Wright, from Atlassian
* [Panel: training new SREs](https://www.usenix.org/conference/srecon17americas/program/presentation/training-new-sres), with Katie Ballinger (CircleCI), Saravanan Loganathan (Yahoo), Rita Lu (Google), Craig Sebenik (Matterport), Andrew Widdowson (Google)

## Oh and one last thing...

<blockquote class="twitter-tweet" data-lang="fr"><p lang="en" dir="ltr">I&#39;m super excited to announce I&#39;m joining <a href="https://twitter.com/datadoghq">@datadoghq</a> as an SRE ! <a href="https://t.co/Ji1JJQLJ4x">pic.twitter.com/Ji1JJQLJ4x</a></p>&mdash; Balthazar Rouberol (@brouberol) <a href="https://twitter.com/brouberol/status/854620051307196417">19 avril 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

[srebook]: https://landing.google.com/sre/book.html
[ctci]: https://www.amazon.com/Cracking-Coding-Interview-Programming-Questions/dp/0984782850/ref=sr_1_1?ie=UTF8&qid=1492689425&sr=8-1&keywords=cracking+the+coding+interview
[ctci_by]: https://www.amazon.com/Gayle-Laakmann-McDowell/e/B004BI1ZUQ/ref=dp_byline_cont_book_1
[dataalgo]: https://www.amazon.com/Data-Structures-Algorithms-Using-Python/dp/1590282337
[tlpi]: https://www.amazon.com/Linux-Programming-Interface-System-Handbook/dp/1593272200/ref=sr_1_1?ie=UTF8&qid=1492692882&sr=8-1&keywords=linux+programming+interface
[linuxtour]: http://learnlinuxconcepts.blogspot.fr/2014/10/this-blog-is-to-help-those-students-and.html