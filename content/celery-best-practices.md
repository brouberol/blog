Title: Celery best practices
Date: 2015-12-29
Category: Programming
Description: My set of best practices for writing Celery asynchronous tasks


I've been programming with [celery](http://celery.readthedocs.org/) for the last three years, and [Deni Bertović](https://denibertovic.com/pages/about-me/)'s article about [Celery best practices](https://denibertovic.com/posts/celery-best-practices/) has truly been invaluable to me. In time, I've also come up with my set of best practices, and I guess this blog is as good a place as any to write them down.

## Write short tasks

I think that a task should be as concise as possible, in order to be able to understand what it does and how it handles corner cases as quickly as possible. I personally try to follow these rules:

* wrap the main task logic in an object method or a function
* make this method/function raise identified exceptions for identified corner cases and decide what is the logic for each of them
* implement a retry mechanism only where appropriate

Let's illustrate these rules with a simple example: sending an email using a 3rd party API (eg: [Mailgun](https://mailgun.com), [Mailjet](https://en.mailjet.com/), etc). Anyone having spent enough time using third party infrastructure and systems knows they should never totally rely on them: the network can fail, they can be unavailable, etc. We thus need to handle some expectable error cases and have a fallback strategy in case of an unexpected error.

Let's say that we have a function  ``api_send_mail`` that does the actual API call, raising a ``myapp.exceptions.InvalidUserInput`` exception, in case of an HTTP client error. This exception constitutes our set of expectable exceptions, that we need to plan for. Any other exception (connection error, server HTTP error, etc) will be sent to some crash report backend, like [Sentry](http://getsentry.com) and trigger a retry.

My task implementation would look something like this:

    ::python

    import requests

    from myproject.tasks import app  # app is your celery application
    from myproject.exceptions import InvalidUserInput

    from utils.mail import api_send_mail

    @app.task(bind=True, max_retries=3)
    def send_mail(self, recipients, sender_email, subject, body):
        """Send a plaintext email with argument subject, sender and body to a list of recipients."""
        try:
            data = api_send_mail(recipients, sender_email, subject, body)
        except InvalidUserInput:
            # No need to retry as the user provided an invalid input
            raise
        except Exception as exc:
            # Any other exception. Log the exception to sentry and retry in 10s.
            sentrycli.captureException()
            self.retry(countdown=10, exc=exc)
        return data

What the task actually does is abstracted one layer down, and almost all the rest of the task body is handling errors. I feel that it's easier to grasp the bigger picture, and that the task is easier to maintain this way.

## Retry gracefully

Setting fixed countdowns for retries may not be what you want. I tend to prefer using a backoff increasing with the number of retries. This means the more a task fails, the more we have to wait until the next retry. I think this has a couple of interesting consequences:

* we don't hammer the external service in case of an outage,
* it gives more time to the service to go back to normal,
* and thus increases our overall chance of success

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
            data = api_send_mail(recipients, sender_email, subject, body)
        except InvalidUserInput:
            raise
        except Exception as exc:
            sentrycli.captureException()
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

If the task takes more than 5 seconds to complete, the ``celery.exceptions.SoftTimeLimitExceeded`` exception would get raised and logged to Sentry.

I also tend to set the [``CELERYD_TASK_SOFT_TIME_LIMIT``](https://celery.readthedocs.org/en/latest/configuration.html?highlight=eager#celeryd-task-soft-time-limit) configuration option with a default value of 300 (5 minutes). This will act as a failsafe if I forget to set an appropriate ``soft_time_limit`` option on a task.


## Share common behavior among tasks

All that is pretty dandy, but I don't want to re-implement the exception catching for every task. I should be able to specify a basic behavior shared between all my tasks. Turns out you can, using an [abstract task class](https://celery.readthedocs.org/en/latest/userguide/tasks.html?highlight=context#abstract-classes).

    ::python

    from myproject.tasks import app

    class BaseTask(app.Task):
        """Abstract base class for all tasks in my app."""

        abstract = True

        def on_retry(self, exc, task_id, args, kwargs, einfo):
            """Log the exceptions to sentry at retry."""
            sentrycli.captureException(exc)
            super(BaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

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
            data = api_send_mail(recipients, sender_email, subject, body)
        except InvalidUserInput:
            raise
        except Exception as exc:
            self.retry(countdown=backoff(self.request.retries), exc=exc)
        return data

You can see that the ``send_mail`` task implementation only deals with email sending and expected error handling. Everything else is handled by the abstract base class. If the common behavior is more complex, this trick can *drastically* reduce the size of each task body and the amount of duplicated code in your tasks.

**Note**: this example is only here to demonstrate how to share behavior between tasks. To properly integrate Sentry with Celery, have a look at [this page](https://docs.getsentry.com/hosted/clients/python/integrations/celery/).

**Tip**: have a look at the list of [available handlers](https://celery.readthedocs.org/en/latest/userguide/tasks.html?highlight=context#handlers), to get an idea of what behavior can be shared between tasks.

## Write large tasks as classes

So far, I've only implemented tasks as functions. However, it's also possible to define [class tasks](https://celery.readthedocs.org/en/latest/userguide/tasks.html#custom-task-classes).

I think one of the scenarii where class tasks really shine are when you'd like to split a large task function into several well-defined and testable methods. As you can see [here](https://celery.readthedocs.org/en/latest/userguide/tasks.html#custom-task-classes), the ``celery.task`` decorator will generate a task class and inject the decorated function as the class ``run`` method.
Defining a class task amounts to defining a class inheriting from ``app.Task`` with a ``run`` method.

    ::python

    class handle_event(BaseTask):   # BaseTask inherits from app.Task

        def validate_input(self, event):
            ...

        def get_or_create_model(self, event):
            ...

        def stream_event(self, event):
            ...

        def run(self, event):
            if not self.validate_intput(event):
                raise InvalidInput(event)
            try:
                model = self.get_or_create_model(event)
                self.call_hooks(event)
                self.persist_model(event)
            except Exception as exc:
                self.retry(countdown=backoff(self.request.retries), exc=exc)
            else:
                self.stream_event(event)


By doing this, the task logic is clear and easy to follow (the ``run`` method stays concise even if the methods body are large), and each of these method can then be unit-tested independently.

Another advantage of using class tasks is using multiple inheritance to specialize a task with multiple abstract base classes.
For example, I'd like to use the [celery_once](https://github.com/TrackMaven/celery-once/) ``QueueOnce`` abstract class to introduce some locking mechanism, while still using the ``BaseTask`` for sentry logging. This way, each abstract task class is used as a mixin, adding some behaviour to the task.

## Unit-test your tasks

Unit testing a project involving celery has always been a pickle for me. I tried to deploy a broker and a test celery worker in the CI environment, but it felt like killing a fly with a bazooka. The answer turns out to be quite simple, thanks to Nicolas Le Manchet for figuring this one out! When the [``CELERY_ALWAYS_EAGER``](https://celery.readthedocs.org/en/latest/configuration.html#celery-always-eager) option is activated, all tasks called using their ``apply_async`` or ``delay`` method are called *directly*, without requiring any broker or celery worker. Easy as pie.
