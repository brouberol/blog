Title: Crawl a website with scrapy
Category: Programming
Date: 2012-04-23

In this article, we are going to see how to scrape information from a website, in particular, from all pages with a common URL pattern. We will see how to do that with [Scrapy](http://scrapy.org/), a very powerful, and yet simple, scraping and web-crawling framework.

For example, you might be interested in scraping information about each article of a blog, and store it information in a database. To achieve such a thing, we will see how to implement a simple [spider](https://en.wikipedia.org/wiki/Web_crawler) using [Scrapy](http://scrapy.org/), which will crawl the blog and store the extracted data into a [MongoDB](http://www.mongodb.org/) database.

We will consider that you have a [working MongoDB server](http://www.mongodb.org/display/DOCS/Quickstart), and that you have installed the `pymongo` and `scrapy` python packages, both installable with [`pip`](http://pypi.python.org/pypi/pip).

If you have never toyed around with [Scrapy](http://scrapy.org/), you should first read this [short tutorial](http://doc.scrapy.org/en/latest/intro/tutorial.html).

## First step, identify the URL pattern(s)

In this example, we’ll see how to extract the following information from each [isbullsh.it](http://isbullsh.it) blogpost :

* title
* author
* tag
* release date
* url

We’re lucky, all posts have the same URL pattern: `http://isbullsh.it/YYYY/MM/title`. These links can be found in the different pages of the site homepage.

What we need is a spider which will follow all links following this pattern, scrape the required information from the target webpage, validate the data integrity, and populate a MongoDB collection.

## Building the spider

We create a Scrapy project, following the instructions from their [tutorial](http://doc.scrapy.org/en/latest/intro/tutorial.html). We obtain the following project structure:

    isbullshit_scraping/
    ├── isbullshit
    │   ├── __init__.py
    │   ├── items.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   └── spiders
    │       ├── __init__.py
    │       ├── isbullshit_spiders.py
    └── scrapy.cfg

We begin by defining, in `items.py`, the item structure which will contain the extracted information:

```python
from scrapy.item import Item, Field

class IsBullshitItem(Item):
    title = Field()
    author = Field()
    tag = Field()
    date = Field()
    link = Field()
```

Now, let’s implement our spider, in `isbullshit_spiders.py`:

```python
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from isbullshit.items import IsBullshitItem

class IsBullshitSpider(CrawlSpider):
    name = 'isbullshit'
    start_urls = ['http://isbullsh.it'] # urls from which the spider will start crawling
    rules = [Rule(SgmlLinkExtractor(allow=[r'page/\d+']), follow=True),
    	# r'page/\d+' : regular expression for http://isbullsh.it/page/X URLs
    	Rule(SgmlLinkExtractor(allow=[r'\d{4}/\d{2}/\w+']), callback='parse_blogpost')]
    	# r'\d{4}/\d{2}/\w+' : regular expression for http://isbullsh.it/YYYY/MM/title URLs

    def parse_blogpost(self, response):
        ...
```

Our spider inherits from `CrawlSpider`, which “provides a convenient mechanism for following links by defining a set of rules”. More info [here](http://isbullsh.it/2012/04/Web-crawling-with-scrapy/readthedocs.org/docs/scrapy/en/0.14/topics/spiders.html#crawlspider).

We then define two simple rules:

* Follow links pointing to `http://isbullsh.it/page/X`
* Extract information from pages defined by a URL of pattern `http://isbullsh.it/YYYY/MM/title`, using the callback method `parse_blogpost`.

## Extracting the data

To extract the title, author, etc, from the HTML code, we’ll use the  `scrapy.selector.HtmlXPathSelector object`, which uses the `libxml2` HTML parser. If you’re not familiar with this object, you should read the `XPathSelector` [documentation](http://readthedocs.org/docs/scrapy/en/0.14/topics/selectors.html#using-selectors-with-xpaths).

We’ll now define the extraction logic in the `parse_blogpost` method (I’ll only define it for the title and tag(s), it’s pretty much always the same logic):

```python
def parse_blogpost(self, response):
    hxs = HtmlXPathSelector(response)
    item = IsBullshitItem()
    # Extract title
    item['title'] = hxs.select('//header/h1/text()').extract() # XPath selector for title
    # Extract author
    item['tag'] = hxs.select("//header/div[@class='post-data']/p/a/text()").extract() # Xpath selector for tag(s)
    ...
    return item
```

**Note**: To be sure of the XPath selectors you define, I’d advise you to use Firebug, Firefox Inspect, or equivalent, to inspect the HTML code of a page, and then test the selector in a [Scrapy shell](http://doc.scrapy.org/en/latest/intro/tutorial.html#trying-selectors-in-the-shell). That only works if the data position is coherent throughout all the pages you crawl.

## Store the results in MongoDB

Each time that the `parse_blogspot` method returns an item, we want it to be sent to a pipeline which will validate the data, and store everything in our Mongo collection.

First, we need to add a couple of things to `settings.py`:

```python
ITEM_PIPELINES = ['isbullshit.pipelines.MongoDBPipeline',]

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "isbullshit"
MONGODB_COLLECTION = "blogposts"
```

Now that we’ve defined our pipeline, our MongoDB database and collection, we’re just left with the pipeline implementation. We just want to be sure that we do not have any missing data (ex: a blogpost without a title, author, etc).

Here is our `pipelines.py` file :

```python
import pymongo

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
    	valid = True
        for data in item:
          # here we only check if the data is not null
          # but we could do any crazy validation we want
       	  if not data:
            valid = False
            raise DropItem("Missing %s of blogpost from %s" %(data, item['url']))
        if valid:
          self.collection.insert(dict(item))
          log.msg("Item wrote to MongoDB database %s/%s" %
                  (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                  level=log.DEBUG, spider=spider)
        return item
```

## Release the spider!

Now, all we have to do is change directory to the root of our project and execute

```bash
$ scrapy crawl isbullshit
```

The spider will then follow all links pointing to a blogpost, retrieve the post title, author name, date, etc, validate the extracted data, and store all that in a MongoDB collection if validation went well.

Pretty neat, hm?

## Conclusion

This case is pretty simplistic: all URLs have a similar pattern and all links are hard written in the HTML code: there is no JS involved. In the case were the links you want to reach are generated by JS, you’d probably want to check out [Selenium](http://pypi.python.org/pypi/selenium). You could complexify the spider by adding new rules, or more complicated regular expressions, but I just wanted to demo how Scrapy worked, not getting into crazy regex explanations.

Also, be aware that sometimes, there’s a thin line bewteen playing with web-scraping and [getting into trouble](https://en.wikipedia.org/wiki/Web_scraping#Legal_issues).

Finally, when toying with web-crawling, keep in mind that you might just flood the server with requests, which can sometimes get you IP-blocked :)

The entire code of this project is hosted on [Github](https://github.com/BaltoRouberol/isbullshit-crawler). Help yourselves!