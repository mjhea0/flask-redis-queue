# project/server/config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))
REDIS_URL = os.environ.get("REDIS_URL")  # REDIS_URL = "redis://redis:6379/0"

from project.server.main.job_callbacks import report_failure, report_success


class BaseConfig(object):
    """Base configuration."""

    WTF_CSRF_ENABLED = True

    # Reference: https://python-rq.org/docs
    REDIS_URL = os.environ.get("REDIS_URL", REDIS_URL)
    QUEUES = ["default"]

    # job_timeout specifies the maximum runtime of the job before it’s \
    # interrupted and marked as failed. Its default unit is second and it can \
    # be an integer or a string representing an integer(e.g. 2, '2'). \
    # Furthermore, it can be a string with specify unit including hour, \
    # minute, second(e.g. '1h', '3m', '5s').
    JOB_TIMEOUT = "1h"

    # result_ttl specifies how long (in seconds) successful jobs and their \
    # results are kept. Expired jobs will be automatically deleted.
    # Defaults to 500 seconds.
    JOB_RESULT_TTL = 3600 * 12

    # ttl specifies the maximum queued time (in seconds) of the job before \
    # it’s discarded. This argument defaults to None (infinite TTL).
    JOB_TTL = None

    # failure_ttl specifies how long failed jobs are kept (defaults to 1 year)
    JOB_FAILURE_TTL = "300s"

    # depends_on specifies another job (or list of jobs) that must complete \
    # before this job will be queued.
    DEPENDS_ON = None

    # job_id allows you to manually specify this job’s job_id
    JOB_ID = None

    # at_front will place the job at the front of the queue, instead of the back
    JOB_AT_FRONT = False

    # description to add additional description to enqueued jobs.
    JOB_DESCRIPTION = "This job is handled independently by seperate web worker"

    # on_success allows you to run a function after a job completes successfully
    JOB_ON_SUCCESS = report_success

    # on_failure allows you to run a function after a job fails
    JOB_ON_FAILURE = report_failure

    # You can also enqueue multiple jobs in bulk with queue.enqueue_many()
    # and Queue.prepare_data() which will enqueue all the jobs in a single
    # redis pipeline which you can optionally pass in yourself
    JOB_PIPELINE = None

    # Refer https://python-rq.org/docs/ and
    # https://github.com/rq/rq/blob/master/rq/queue.py
    JOB_META = None
    JOB_RETRY = None

    # Webhook endpoint to send automatic response after job success or failure
    WEBHOOK_ENDPOINT = "http://webhook:8888"


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    WTF_CSRF_ENABLED = False
    REDIS_URL = os.environ.get("REDIS_URL", REDIS_URL)


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    REDIS_URL = os.environ.get("REDIS_URL", REDIS_URL)
