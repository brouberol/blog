Title: Tools I'm thankful for
Date: 2022-02-22
Category: Programming
Description: A description of the tools which helped me grow as an engineer and define my core engineering values.
Summary: Software engineers sometimes have a reputation for being overly critical when it comes to tools and programming languages. The web is full of rants, heated debates and articles about what technology is "better" and which is "crap". It was thus refreshing to read an post titled [_Software I'm thankful for_](https://www.jowanza.com/blog/2022/2/21/software-im-thankful-for), that shone a light on some pieces of software in a positive light. In honor of this article, I've decided to go through the same exercise.
Image: https://images.rawpixel.com/image_1300/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvcGQ0My0wMi0wMTEtZXllXzEuanBn.jpg?s=lpexiDOfvyyBvu5KHWfgqE9pBkcnyZ_xkNA4-EV9E5A
Tags:
Keywords: docker, raspberry-pi, python, software, kubernetes
Status: draft


Software engineers sometimes have a reputation of being overly critical when it comes to tools and programming languages. The web is full of rants, heated debates and articles about what technology is "better" and which is "crap". It was thus refreshing to read an post titled [_Software I'm thankful for_](https://www.jowanza.com/blog/2022/2/21/software-im-thankful-for), that shone a light on some pieces of software in a positive light. In honor of this article, I've decided to go through the same exercise.


## Python

[Python](https://python.org) was my gateway to becoming a software engineering. It was the first programming language I _loved_, and I still do to this day.
I wrote Python code professionally for a an AI startup, an e-ticketing startup, the Scottish government, a global hosting provider, a huge observability SaaS. I've written large Python webapps and quick Python scripts. I've written large asynchronous task workflows processing payments, trained machine learning models, written self-documented REST APIs, found my house listing by scraping the web, [monitor the level of the river close by](/river-monitoring-with-datadog), all of that in Python. 

I also write Python code to maintain my own [infrastructure](https://github.com/brouberol/infrastructure), that I deploy via [ansible](https://docs.ansible.com/), itself written in Python. This blog is generated via [Pelican](https://pelican.readthedocs.org), which is written in Python. I've started to play with a RaspberryPi Pico, that I program in ... [CircuitPython](http://docs.circuitpython.org/en/latest/README.html). It's ubiquitous, and I've heard it be called "The second best tool for every job", meaning that it probably won't be the most performant tool for what you're working on, but you'll make progress really fast.

Learning and programming Python has taught me many programming concepts, such as object oriented programming, functional programming, unit testing, dataclasses, metaprogramming, REST APIs, HTTP. JSON, etc.

I however now realize that it also allowed me to get introduced to _lower-level_ concepts, such as ioctl, sockets, system calls, file descriptors, etc, through the reassuring lens of the Python standard library, instead of having to interact with these concepts in C, which was much more intimidating, and still is to this day.


## Docker

The first time I was introduced to [Docker](https://docs.docker.com/) was at a Python meetup in Lyon, circa 2013. After the 30 minute long presentation, I still had no clue as to what any of it meant and why I'd ever need it and pretty much shrugged it off. As the Docker ecosystem flourished and the dust settled, I started to understand the appeal.

Do you need to run redis to prototype against? Just run `docker run redis` and _voila_. Do you want to run `calibre-web` on your local VPS without having to install its dependencies in your system libraries? [Sure](https://github.com/brouberol/infrastructure/blob/0e2ece50b45bc998cfc09dff1dc002c96f91cdee/playbooks/roles/gallifrey/calibre/tasks/main.yml#L10-L26).

Docker allowed me to self-host a collection of tools that I use every day, package and run applications in extremely large production environments, spin up development environments without having to pollute my system libraries. It boosted my productivity and became part of my day-to-day workflow. None of these are the _real_ reason why I'm thankful for Docker.

I've seen many companies break down their monolith into dockerized microservices. The commonly invoked reasons are allowing teams to chose their own language for each project, and helping the horizontal scaling of some load-critical apps. As useful Docker was to start a single container, it didn't solve the issue of starting several containers that could communicate with each other on a single host. Enter [docker-compose](https://docs.docker.com/compose/), which in turn didn't solve the issue of orchestrating containers on a fleet of nodes. Enter [Mesos/Marathon](https://mesosphere.github.io/marathon/), [Docker Swarm](https://docs.docker.com/engine/swarm/), [Kubernetes](https://kubernetes.io), [Amazon ECS](https://aws.amazon.com/fr/ecs/), etc.

The beef I have with Docker is that the hype around its _ecosystem_ caused small companies to onboard immense amount of complexity from the absolute get-go, to help with recruiting. Because engineers want to build experience with Kubernetes, these companies find themselves dividing their attention between grappling with its inherent complexity, distributed tracing, image recycling policies, RBAC, etc, and building their actual core value.  

This is why I'm thankful for Docker and its ecosystem. I believe I've seen situations in which it truly was critically useful, and I'll now be able to differentiate between situations in which we need it, and situations in which we only wished we did. 


## Raspberry Pi

Before I joined OVH, the _only_ sysadmin experience I had was tinkering with my [Raspberry Pi](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/). Thanks to that 35$ matchbox-sized computer, I got to learn iptables and systemd, port forwarding, ssh hardening, file system checks and repairs. But really, the crucial point is that I was able to learn all that by making mistakes. I'd rather learn about why you need to be careful with `iptables -j DROP` in the comfort of my own home than in a production, high pressure, environment. I can't stress the impact that learning without the fear of public failure had on me. 

I'm now getting into electronics through the [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/), which opens a whole new exploration and tinkering domain for me!


## The terminal

The terminal is a truly important part of my day as a software engineer. It's really what allows me to feel in control. Like Python, it became a familiar tool in which I could discover entirely new domains, interact with new systems and concepts. I learned so much from it that I decided to help people out [getting familiarized with the terminal and the shell](/category/essential-tools-and-practices-for-the-aspiring-software-developer). 