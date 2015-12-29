Title: 3 years of celery, lessons learned
Date: 2015-12-29
Category: Programming, Python

I've been programming with [celery](http://celery.readthedocs.org/) for the last three years, and have recently been giving celery consulting to other teams at [OVH](http://ovh.com/). I've come to realize that I regularly go through the same best practices and common pitfalls, and that I should probably have them written up somewhere. I guess this blog is as good a place as any.


## Short task body

My feeling is that a task should be as concise as possible, in order to be able to understand what it does and how it handles corner cases as quickly as possible. I personally try to follow these rules:

* wrap the main task logic in an object method or a function
* make this method/function raise identified exceptions for identified corner cases and decide what is the logic for each of them
* implement a retry mechanism only where appropriate

Let's illustrate these rules with a simple example: sending an email using an HTTP REST API (eg: [Mailgun](https://mailgun.com), [Mailjet](https://en.mailjet.com/), etc). Anyone having spent enough time using third party APIs knows they can be unreliable: the network can fail, a bug can be introduced and fail to show up during the review process, etc. We thus need to handle some expectable error cases and have a fallback strategy in case of an unexpected error.

Let's say that we have a function  ``send_mail`` that does the actual API call, raising a ``requests.ConnectionError`` exception, in case of an unreachable host and a ``requests.HTTPError`` exception in case of a client/server error. These two exceptions constitute our set of expectable exceptions, that we need to plan for. Any other exception will be sent to some crash report backend, like [Sentry](http://getsentry.com).

My task implementation would look something like this:

    ::python

    import requests

    from utils.mail import send_mail as _send_mail

    @app.task(bind=True, max_retries=3)
    def send_mail(self, recipients, sender_email, subject, body):
        """Send a plaintext email with argument subject, sender and body to a list of recipients."""
        try:
            data = _send_mail(recipients, sender_email, subject, body)
        except requests.ConnectionError as exc:
            # Host unreachable. Maybe a temporary connection error?
            self.retry(countdown=10, exc=exc)
        except requests.HTTPError as exc:
            if exc.response.status_code >= 500:
                # Server error. Maybe temporary?
                self.retry(countdown=10, exc=exc)
            else:
                # Client error. Fail fast
                raise
        except Exception:
            # Any other exception. Log the exception to sentry and let the task fail.
            sentrycli.captureException()
            raise
        return data

What the task actually does is abstracted one layer down, and almost all the rest of the task body is handling errors. I strongly feel that's how it should be.


## Retry gracefully

Setting fixed countdowns for retries may not be what you want. I tend to prefer using a backoff which increases with the number of retries. This means the more a task fails, the more I have to wait until the next retry. I think this has a couple of interesting consequences:

* it avoids hammering the external service in case of an outage,
* it gives more time to the service status to go back to normal,
* and thus increases your chance of successful result

A simple (but effective) implementation could look something like this:

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

One thing to remember is to **always** specify a timeout on I/O operations, or at least on the celery task itself. If you don't, it's possible all your tasks could block indefinitely, which would then prevent any additional task to start. In the context of the ``send_mail`` task, I could probably do something like this:

    ::python

    @app.task(
        bind=True,
        max_retries=3,
        soft_time_limit=3 # time limit is in seconds
    )
    def send_mail(self, recipients, sender_email, subject, body):
        ...

The ``celery.exceptions.SoftTimeLimitExceeded`` exception, raised if the task takes more than 3 seconds to return, would then be logged in Sentry.

I also tend to set the ``CELERYD_TASK_SOFT_TIME_LIMIT`` configuration option with a default value of 300 (5 minutes). This will act as a failsafe if I forget to set an appropriate ``soft_time_limit`` option.


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
        soft_time_limit=3,
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

You can see that the ``send_mail`` task implementation only deals with email sending and expected error handling. All common behavior, not directly related to what the tasks does, is handled by the abstract base class. If the common behavior is more complex, this trick can *drastically* reduce the size of each task body!

**Note**: this example is only here to demonstrate how to share behavior between tasks. To properly integrate Sentry with Celery, have a look at [this page](https://docs.getsentry.com/hosted/clients/python/integrations/celery/).

**Tip**: have a look at the list of [available handlers](https://celery.readthedocs.org/en/latest/userguide/tasks.html?highlight=context#handlers), to get an idea of what behavior can be shared between tasks.

## Isolate SQLAlchemy sessions
## Implement data pipelines using chains
## Supervisor production workers
## Throttle external API calls
