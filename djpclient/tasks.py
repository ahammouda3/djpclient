
from celery.task import task
#from celery.decorators import task

import send


@task(name="tasks.SendQueriesTask", serializer='json')
def SendQueriesTask(queries, viewname, is_view):
    send.SendQueries(queries, viewname, is_view)


@task(name="tasks.SendBenchmarkTask")
def SendBenchmarkTask(exectime, cputime, viewname, is_view):
    send.SendBenchmark(exectime, cputime, viewname, is_view)


@task(name="tasks.SendMemcacheStat")
def SendMemcacheStat(statobj, viewname, is_view):
    send.SendMemcacheStat(statobj, viewname, is_view)

@task(name="tasks.SendUserActivity")
def SendUserActivity(is_anonymous, username, userid, useremail, viewname, is_view):
    send.SendUserActivity(is_anonymous, username, userid, useremail, viewname, is_view)

