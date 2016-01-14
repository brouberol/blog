Title: Celery best practices and common pitfalls
Date: 2015-12-29
Category: Programming, Python

I've been programming with [celery](http://celery.readthedocs.org/) for the last three years, and have recently been helping other teams at [OVH](http://ovh.com/) getting their celery project up and running. I've come to realize that I regularly go through the same best practices and common pitfalls, and that I should probably have them written up somewhere. I guess this blog is as good a place as any.


## Short task body

I think that a task should be as concise as possible, in order to be able to understand what it does and how it handles corner cases as quickly as possible. I personally try to follow these rules:

* wrap the main task logic in an object method or a function
* make this method/function raise identified exceptions for identified corner cases and decide what is the logic for each of them
* implement a retry mechanism only where appropriate

Let's illustrate these rules with a simple example: sending an email using a 3rd party API (eg: [Mailgun](https://mailgun.com), [Mailjet](https://en.mailjet.com/), etc). Anyone having spent enough time using third party infrastructure and systems knows they should never totally rely on them: the network can fail, they can be unavailable, etc. We thus need to handle some expectable error cases and have a fallback strategy in case of an unexpected error.

Let's say that we have a function  ``api_send_mail`` that does the actual API call, raising a ``requests.ConnectionError`` exception, in case of an unreachable host and a ``requests.HTTPError`` exception in case of a client/server error. These two exceptions constitute our set of expectable exceptions, that we need to plan for. Any other exception will be sent to some crash report backend, like [Sentry](http://getsentry.com).

My task implementation would look something like this:

    ::python

    import requests
    from myproject.tasks import app  # app is your celery application

    from utils.mail import api_send_mail

    @app.task(bind=True, max_retries=3)
    def send_mail(self, recipients, sender_email, subject, body):
        """Send a plaintext email with argument subject, sender and body to a list of recipients."""
        try:
            data = api_send_mail(recipients, sender_email, subject, body)
        except requests.ConnectionError as exc:
            # Host unreachable. Maybe a temporary connection error? Retry in 10s.
            self.retry(countdown=10, exc=exc)
        except requests.HTTPError as exc:
            if exc.response.status_code >= 500:
                # Server error. Maybe temporary? Retry in 10s.
                self.retry(countdown=10, exc=exc)
            else:
                # Client error. Fail fast
                raise
        except Exception:
            # Any other exception. Log the exception to sentry and let the task fail.
            sentrycli.captureException()
            raise
        return data

What the task actually does is abstracted one layer down, and almost all the rest of the task body is handling errors. I feel that it's easier to grasp the bigger picture, and that the task is easier to maintain this way.

## Retry gracefully

Setting fixed countdowns for retries may not be what you want. I tend to prefer using a backoff which increases with the number of retries. This means the more a task fails, the more I have to wait until the next retry. I think this has a couple of interesting consequences:

* it avoids hammering the external service in case of an outage,
* it gives more time to the service status to go back to normal,
* and thus increases your overall chance of success

A simple (but effective anyhow) implementation could look something like this:

    ::python

    def backoff(attempts):
        """Return a backoff delay, in seconds, given a number of attempts.

        The delay increases very rapidly with the number of attemps:
        1, 2, 4, 8, 16, 32, ...

        """
        return 2 ** attempts

    @app.task(bind=True, max_retries=3)
    def send_mail(self, recipients, sender_email, subject, body):
        """Send a plaintext email with argument subject, sender and body to a list of recipients."""
        try:
            data = _send_mail(recipients, sender_email, subject, body)
        except requests.ConnectionError as exc:
            self.retry(countdown=backoff(self.request.retries), exc=exc)
        except requests.HTTPError as exc:
            if exc.response.status_code >= 500:
                self.retry(countdown=backoff(self.request.retries), exc=exc)
            ...


## Fail fast and don't block forever

One thing to remember is to **always** specify a timeout on I/O operations, or at least on the celery task itself. If you don't, it's possible all your tasks could block indefinitely, which would then prevent any additional task to start. In the context of the ``send_mail`` task, I could probably do something like this, as an API call should probably not take more than 5 seconds:

    ::python

    @app.task(
        bind=True,
        max_retries=3,
        soft_time_limit=5 # time limit is in seconds.
    )
    def send_mail(self, recipients, sender_email, subject, body):
        ...

Uf the task takes more than 5 seconds to complete, the ``celery.exceptions.SoftTimeLimitExceeded`` exception would get raised and logged to Sentry.

I also tend to set the [``CELERYD_TASK_SOFT_TIME_LIMIT``](https://celery.readthedocs.org/en/latest/configuration.html?highlight=eager#celeryd-task-soft-time-limit) configuration option with a default value of 300 (5 minutes). This will act as a failsafe if I forget to set an appropriate ``soft_time_limit`` option on a task.


## Share common behavior among tasks

All that is pretty dandy, but I don't want to re-implement the exception catching for every task. I should be able to specify a basic behavior shared between all my tasks. Turns out you can, using an [abstract task class](https://celery.readthedocs.org/en/latest/userguide/tasks.html?highlight=context#abstract-classes).

    ::python

    from celery import Task


    class BaseTask(Task):
        """Abstract base class for all tasks in my app."""

        abstract = True

        def on_failure(self, exc, task_id, args, kwargs, einfo):
            """Log the exceptions to sentry."""
            sentrycli.captureException(exc)
            super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)


    @app.task(
        bind=True,
        max_retries=3,
        soft_time_limit=5,
        base=BaseTask)
    def send_mail(self, recipients, sender_email, subject, body):
        """Send a plaintext email with argument subject, sender and body to a list of recipients."""
        try:
            data = _send_mail(recipients, sender_email, subject, body)
        except requests.ConnectionError as exc:
            self.retry(countdown=backoff(self.request.retries), exc=exc)
        except requests.HTTPError as exc:
            if exc.response.status_code >= 500:
                self.retry(countdown=backoff(self.request.retries), exc=exc)
            else:
                raise
        # Any other exceptions will be logged by the base class on_failure method
        return data

You can see that the ``send_mail`` task implementation only deals with email sending and expected error handling. All common behavior, not directly related to what the tasks does, is handled by the abstract base class. If the common behavior is more complex, this trick can *drastically* reduce the size of each task body and the amount of duplicated code in your tasks.

**Note**: this example is only here to demonstrate how to share behavior between tasks. To properly integrate Sentry with Celery, have a look at [this page](https://docs.getsentry.com/hosted/clients/python/integrations/celery/).

**Tip**: have a look at the list of [available handlers](https://celery.readthedocs.org/en/latest/userguide/tasks.html?highlight=context#handlers), to get an idea of what behavior can be shared between tasks.

## Write complex tasks as classes

So far, I've only implemented tasks as functions. However, if your task logic is complex, the task body can grow quite large. A nice trick is to then define a [class task](https://celery.readthedocs.org/en/latest/userguide/tasks.html#custom-task-classes) instead, define methods for each part of the logic, and assemble everything in the task ``run`` method.

The ``send_mail`` task is a tad too simple to clearly see the benefit of class tasks, so I'll use the fine example from [Jeremy Satterfield](http://jsatt.com/blog/author/jsatt/)'s article [Class-based Celery Tasks](http://jsatt.com/blog/class-based-celery-tasks/):

    ::python

    from myproject.tasks import app

    class generate_file(app.Task):

        base = BaseTask

        def run(self, source, *args, **kwargs):
            # Note that proper error handling is missing here
            self.source = source
            data = self.collect_data()
            self.generate_file(data)

        def generate_file(self, data):
            # do your file generation here
            ...

        def collect_data(self):
            # do your data collection here
            ...
            return data

By doing this, the task logic is clear and easy to follow (the ``run`` method stays concise even if the methods body are large), and each of these method can then be unit-tested independently.


## Unit-testing tasks

I've always found that unit-testing turned out to be quite complex when celery was involved in a project. I've tried several strategies and methods:

* starting a test celery worker using the [CELERY_ALWAYS_EAGER](https://celery.readthedocs.org/en/latest/configuration.html?highlight=eager#std:setting-CELERY_ALWAYS_EAGER). I found it to be cumbersome and complex, especially in a CI environment.
* unit-testing functions or classes wrapped in celery tasks, but never directly testing the tasks themselves. Works well, but fails when your code directly *dispatches* a celery task.
* wrap all task dispatch and result collection calls in a function that will decide if the task should be called directly or through a celery worker. I like this approach, as it's both simple and works well in a test environment.

To illustrate the third approach, let's imagine that we have a API handler in charge of generating a PDF, and that the actual PDF generation is performed in a celery task. We'd like to write an integration test for this API call, without having any actual celery worker running.

We can thus write the following ``start_task`` function, which logic will depend of the project configuration:

    ::python

    # myproject/utils/tasks.py

    from celery import Task

    from myproject.config import Config

    def start_task(task, args=None, kwargs=None, **options):
        """

        """
        args = args or ()
        kwargs = kwargs or {}
        # handle the case of class tasks, which needs to be instantiated first
        if not isinstance(task, Task):
            task = task()
        # Either send the task to a celery worker...
        if Config()['tasks']['async']:
            res = task.apply_async(args=args, kwargs=kwargs, **options)
        # .. or call it directly
        else:
            res = task(*args, **kwargs)
        return res

We can then call celery tasks using this function in our API handler:

    ::python

    # myproject/api/pdf.py

    from myproject.tasks.pdf import generate_pdf
    from myproject.api import api
    from pyproject.utils.tasks import start_task


    @api.get('/account/<account>/pdf/')
    def generate_pdf(account):
        """Generate a PDF record for the argument account."""
        # some logic here that we'd like to test
        async_res = start_task(generate_pdf, kwargs={'account': account})
        # some logic here also

When launching our integration/unit tests, we'll just have to have the ``Config()['tasks']['async']`` set to ``False``, and all the pdf generation will be done synchronoulsy, in a regular python function/method call. Easy as pie.
