Title: On meritocracy, identity and context
Date: 2018-09-21
Category: Programming


**Before reading**

This is a deeply personal article, that hasn't been easy to write, especially with all the tension currently occurring in the tech industry, around inclusiveness, gender, code of conducts, etc. I've done my best to explain my thoughts on the matter, while being as respectful as possible. If you feel that you disagree with me, I'd be happy to debate with you, as long as the discussion stays civil and respectful.

---

### The lay of the land

I have been working as a professional engineer in the tech industry for the last 7 years or so. My first contact with the subject of under-representation of minorities in the industry came during EuroPython 2012, when a tasteless tweet was posted the very night after which [Lynn Root](http://www.roguelynn.com/) talked about ["Increasing women engagement in the Python community"](https://www.youtube.com/watch?v=l2PnVKQJg0I) (these events are best summarized by [Lynn herself](http://www.roguelynn.com/words/a-memorable-europython-for-the-better/)). And these events kept [happening](https://en.wiktionary.org/wiki/Donglegate), and [happening](https://www.dailydot.com/debug/sexist-tech-conference-slide/), and [happening](https://en.wikipedia.org/wiki/Sexism_in_the_technology_industry#Incidents). My personal view has since then been that each of these highly publicized events were caused by an appalling lack of tact, thoughtfulness, empathy and respect, and that conference attendees should make sure to behave appropriately or should suffer the consequences.

[Code of Conducts](http://confcodeofconduct.com/) started to be [defined](https://ep2018.europython.eu/en/coc/) for [conferences](https://www.dotconferences.com/codeofconduct) and [online projects](https://www.djangoproject.com/conduct/), thanks to the initiative of groups and individuals pushing for more respectful and inclusive communities. I have always thought that these were essential and useful, because they seemed to be making some conference attendees or project members feel safer (and not making myself feel less so), and would probably help keeping jerk-like behavior at bay.

[Safe spaces](https://djangogirls.org/pyconuk/) were organized in conferences (I even helped on a few myself, as a tutor), and I thought it was a wonderful idea. I did not take anything away from the most represented types of conference attendees, and allowed less represented people to be able to take their marks in a safe environment.

However, I feel something changed for me when I read the proposal to replace the `master/slave` terminology by `leader/follower` in the [Django framework](https://github.com/django/django/pull/2692). The PR starts with the following stance:
> The docs and some tests contain references to a master/slave db configuration.
  While this terminology has been used for a long time, those terms may carry racially charged meanings to users.

My view at the time was _"I mean, it does not really change anything for me, and if it can help people feel better..."_. Looking back, I'm pretty sure I felt a bit of unease reading the PR, but I (subconsciously or not) shrugged it off.

That debate recently resurfaced when the same thing happened in both the [redis](https://github.com/antirez/redis/issues/5335) and the [CPython](https://bugs.python.org/issue34605) codebases.
Reading what antirez (the redis creator) [had to say on the subject](http://antirez.com/news/122) was a real moment of clarity for me.

> Today it happened again. A developer, that we’ll call Mark to avoid exposing his real name, read the Redis 5.0 RC5 change log, and was disappointed to see that Redis still uses the “master” and “slave” terminology in order to identify different roles in Redis replication.

> I said that I was sorry he was disappointed about that, but at the same time, I don’t believe that terminology out of context is offensive, so if I use master-slave in the context of databases, and I’m not referring in any way to slavery. I originally copied the terms from MySQL, and now they are the way we call things in Redis, and since I do not believe in this battle (I’ll tell you later why), to change the documentation, deprecate the API and add a new one, change the INFO fields, just to make a subset of people that care about those things more happy, do not make sense to me.

> After it was clear that I was not interested in his argument, Mark accused me of being fascist.

At this point, I realized the landscape had dramatically changed, and that the inclusiveness debate had morphed into a more politicized and (according to me) confused and sterile version of itself.

Case in point, someone suggested the [Zen of Python](https://www.python.org/dev/peps/pep-0020/) should be [modified](https://mail.python.org/pipermail/python-ideas/2018-September/053365.html) because the sentence _Beautiful is better than ugly_ could be interpreted as a support for body-shaming behaviors. Words cannot express how wrong this feels to me. That suggestion shows both a profound lack of contextual thinking, and a will to advance a pro political correctness agenda.

People have been talking about [Beautiful Code](https://www.amazon.com/Beautiful-Code-Leading-Programmers-Practice/dp/0596510047) and [Ugly Code](http://uglycode.com/) for a **long time**. Long enough to write books about it. Long enough so that I could have late night discussions about it with my father (who's also a computer scientist). To me, suggesting that _Beautiful is better than ugly_ encourages body shaming feels alien, because it's completely **out of context**. Words have certain meanings in certain contexts. That's how we get away with synonyms. In the context of the [Zen of Python](https://www.python.org/dev/peps/pep-0020/), the word _Beautiful_ clearly characterizes code, not people. The [Dwarf Star](https://en.wikipedia.org/wiki/Dwarf_star) term defines a certain type of star, with given astrophysical properties. Should the entire astrophysics community rename it just because some people feel it's an offensive way of calling [Peter Dinklage](https://fr.wikipedia.org/wiki/Peter_Dinklage)? Similar humorous (or not?) [counter-arguments](https://bugs.python.org/msg324816) were offered during the CPython master/slave debate.

It seems all we read about now (especially after Linus Torvalds' [temporary stepdown](https://lkml.org/lkml/2018/9/16/167)) is either written by [strong meritocracy](https://medium.com/culture-null/how-sjws-infiltrated-the-open-source-community-21001e7059ef) [partisans](https://lkml.org/lkml/2018/9/16/198), [conspiracy theorists](https://www.reddit.com/r/linux/comments/9ghrrj/linuxs_new_coc_is_a_piece_of_shit/e64h04h/) or by [strong inclusiveness defenders](https://twitter.com/CoralineAda/status/1041441155874009093?ref_src=twsrc%5Etfw) (I've decided not to use the term SJW, as I understand it's a [mocking and pejorative](https://en.wikipedia.org/wiki/Social_justice_warrior) term).

It was even [suggested](https://mail.python.org/pipermail/python-ideas/2018-September/053369.html) and [debated](https://mail.python.org/pipermail/python-ideas/2018-September/053375.html) whether that this suggestion was made by a troll. The fact that, troll or not, that discussion lingered for several days is a very serious issue to me. It shows how polarized the debate now is, and how easily a strong community can be derailed.


### About inclusivity, diversity and context

The core of the debate is focused on inclusivity and diversity (see [this example](https://bugs.python.org/issue34605)), which got me thinking. It's clear to me *why* we want to push for diversity:

- a body of similar minds will likely producer similar solutions to a problem, causing the final adopted solution to be [more narrowed](https://www.dailymail.co.uk/sciencetech/article-4800234/Is-soap-dispenser-RACIST.html)
- a person could (subconsciously or not) avoid a given career path / community because she/he might not feel represented enough, and thus feel excluded or as though he/she does not belong

I want to focus on the second point, because I'm of the opinion that this is where the heated debates stem from.

If you read the [Code of Conduct Covenant](https://www.contributor-covenant.org/version/1/4/code-of-conduct), which is a code of conduct most of the current conferences and community use or are based on, the text starts with:

> In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

I naturally tend to agree with this. We should all strive for inclusiveness and diversity, and should make sure everyone is treated gently and is given a friendly, open hand, whomever they are.
However, if I were fostering malicious intent, I could point out that this list does not cover diets. I myself am a flexitarian (I've cut out all fish and meat from my daily diet, but will eat some without issue if there's no other option). I could somehow feel unrepresented or even excluded from a given community if its CoC does not state that my personal diet should be respected.

Although that example could seem frivolous or ridiculous, it points out something I feel is interesting. That whole paragraph attempts at listing all the way people could differ, to make sure everyone is explicitly included. I would personally have phrased it a more open-ended way:

> In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of who they are and how they identify.

as I think some issues stem from the fact we have attempted to list what constitutes "diversity". If a tech conference decides to impose quotas on speakers, these quotas will focus on certain attributes (eg sex and skin color) while missing others (eg age, education), which might some people to better identify to the speakers, but might not help others. This _inventaire à la Prévert_ certainly looks like inclusiveness, but I think it misses the point.

How we identify is both subjective and subject to context. I might identify as an SRE, an engineer or a Python developer in the context of work or a tech-related event, a social extrovert in the context of a party, an leftist heterosexual male in the context of my personal and private life, etc.

How we identify depends on context, and yet, we seem intent on mixing personal identities and non-personal contexts, the same way accusing _Beautiful is better than ugly_ to promote body shaming mixes human and technological contexts. I recognize that some situations are trickier than others (eg conferences, workplaces), because they can mix personal and professional contexts, thus blurring the lines.

If diversity is defined as having multiple identities present, then diversity must be subjective and subject to context too. To follow in that tech conference example, I feel diversity in the technological content should reside in education background, level of experience and field of interest of the speaker, while diversity in the social events tied to the conference could have a totally different definition.

These criterion are my pick, but I suggest you clearly and openly define which ones matter to you if you're ever in the position of selecting speakers or employees.


### Closing words

In my view, the tech industry as a whole has been guilty of resistance to change by kicking around the old meritocracy horse for too long. We need to talk about the lack of women, the rampant misogynist attitudes, the male/women pay gap. We need to fix these issues by acknowledging them first, and debating them transparently. Not just as an industry, but as a society.

However, as I don't buy in "show me the code or GTFO" attitude, I don't believe in politically correctness before everything else. If some people lack the ability to recognize that _Beautiful is better than ugly_ in the [Zen of Python](https://www.python.org/dev/peps/pep-0020/) not body shame people, then maybe we shouldn't let them define what our core values are.
