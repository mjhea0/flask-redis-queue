# Job callbacks

import pathlib
import sys
import time

import requests
from redis import Redis
from rq import Queue

try:
    basedir = pathlib.os.path.abspath(pathlib.os.path.dirname(__file__))
except NameError:
    basedir = pathlib.os.path.abspath(pathlib.os.path.dirname("."))
server_parentdir = pathlib.os.path.dirname(basedir)

try:
    from project.server.main.utils import unpacking
except ModuleNotFoundError:
    project_parentdir = pathlib.os.path.dirname(server_parentdir)
    root_parentdir = pathlib.os.path.dirname(project_parentdir)
    # Import root for project
    pathlib.sys.path.insert(0, root_parentdir)
    from project.server.main.utils import unpacking


def report_success(
    job: Queue.enqueue, connection: Redis, result: object, *args, **kwargs
):
    """
    Success callbacks must be a function that accepts job, connection and
    result arguments. Your function should also accept *args and **kwargs
    so your application doesn’t break when additional parameters are added.

    Success callbacks are executed after job execution is complete, before
    dependents are enqueued. If an exception happens when your callback is
    executed, job status will be set to FAILED and dependents won’t be enqueued.

    Callbacks are limited to 60 seconds of execution time. If you want to
    execute a long running job, consider using RQ’s job dependency feature instead.

    Parameters
    ----------
    job : Queue.enqueue
        Enqued job object in rq.
    connection : Redis
        Redis connection object.
    result : object
        returned value of enqued job object in rq.
    *args
        Additional tuple parameter(s).
    **kwargs
        additional mapped dictionary parameter(s).

    Returns
    -------
    None.

    """
    # Run a function after a job completes successfully
    unpacked_object = unpacking(job.result)
    tic = unpacked_object and unpacked_object.tic
    webhook_endpoint = unpacked_object.webhook_endpoint
    toc = time.time()
    payload = {
        "status": "success",
        "data": {
            "time": toc - tic,
            "job_id": job.get_id(),
            "job_status": job.get_status(),
            "texts": unpacked_object.texts,
            "file_names": unpacked_object.file_names,
            "byte_data_lengths": unpacked_object.byte_data_lengths,
            "webhook_endpoint": unpacked_object.webhook_endpoint,
            "delay": unpacked_object.delay,
        },
    }
    url = webhook_endpoint
    headers = {"Content-Type": "text/plain"}
    response = requests.request(
        "POST", url, headers=headers, data=str(payload).encode("utf-8")
    )
    return response


def report_failure(
    job: Queue.enqueue,
    connection: Redis,
    type: sys.exc_info()[0],
    value: sys.exc_info()[1],
    traceback: sys.exc_info()[2],
) -> sys.exc_info():
    """
    Failure callbacks are functions that accept job, connection, type, value
    and traceback arguments. type, value and traceback values returned by
    sys.exc_info(), which is the exception raised when executing your job.

    Failure callbacks are limited to 60 seconds of execution time.

    Parameters
    ----------
    job : Queue.enqueue
        Enqued job object in rq.
    connection : Redis
        Redis connection object.
    type : sys.exc_info()[0]
        type gets the type of the exception being handled (a subclass of
                                                           BaseException).
    value : sys.exc_info()[1].
        value gets the exception instance (an instance of the exception type).
    traceback : sys.exc_info()[2]
        traceback gets a traceback object which encapsulates the call stack
        at the point where the exception originally occurred

    Returns
    -------
    sys.exc_info().
        This function returns a tuple of three values that give information
        about the exception that is currently being handled.

    """
    # Run a function after a job fails
    webhook_endpoint = value.webhook_endpoint
    tic = value.tic
    if job:
        pickled_object = job.result
        unpacked_object = unpacking(pickled_object)
    toc = time.time()
    payload = {
        "status": "error",
        "data": {
            "time": toc - tic,
            "job_id": job.get_id(),
            "job_status": job.get_status(),
            "texts": unpacked_object.texts,
            "file_names": unpacked_object.file_names,
            "byte_data_lengths": unpacked_object.byte_data_lengths,
            "webhook_endpoint": unpacked_object.webhook_endpoint,
            "delay": unpacked_object.delay,
        },
    }
    url = webhook_endpoint
    headers = {"Content-Type": "text/plain"}
    response = requests.request(
        "POST", url, headers=headers, data=str(payload).encode("utf-8")
    )
    return response
