
from celery.task import task

import send


@task(name="tasks.SendQueriesTask", serializer='json')
def SendQueriesTask(kwargs, requestargs, queries, viewname, is_view, ga_cookie, ga_exp_time):
    send.SendQueries(kwargs, requestargs, queries, viewname, is_view, ga_cookie, ga_exp_time)

@task(name="tasks.SendBenchmarkTask")
def SendBenchmarkTask(kwargs, requestargs, exectime, cputime, viewname, is_view, ga_cookie, ga_exp_time):
    send.SendBenchmark(kwargs, requestargs, exectime, cputime, viewname, is_view, ga_cookie, ga_exp_time)

@task(name="tasks.SendMemcacheStat")
def SendMemcacheStat(kwargs, requestargs, statobj, viewname, is_view, ga_cookie, ga_exp_time):
    send.SendMemcacheStat(kwargs, requestargs, statobj, viewname, is_view, ga_cookie, ga_exp_time)

@task(name="tasks.SendUserActivity")
def SendUserActivity(kwargs, requestargs, is_anonymous, username, userid, useremail, viewname, is_view, ga_cookie, ga_exp_time):
    send.SendUserActivity(kwargs, requestargs, is_anonymous, username, userid, useremail, viewname, is_view, ga_cookie, ga_exp_time)

@task(name="tasks.SendBundle")
def SendBundle(kwargs, requestargs, querydata, exectime, cputime, stat, is_anonymous, username, userid, useremail, name, ga_cookie, ga_exp_time):
    send.SendBundle(kwargs, requestargs, querydata, exectime, cputime, stat, is_anonymous, username, userid, useremail, name, ga_cookie, ga_exp_time)

@task(name='tasks.SendSendLogMessage')
def SendLogMessage(record):
    send.SendLogMessage(record)

