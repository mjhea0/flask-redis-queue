# project/server/main/views.py


import time

import redis
from flask import Blueprint, current_app, jsonify, render_template, request
from rq import Connection, Queue

from project.server.main.jobs import create_job
from project.server.main.utils import unpacking

main_blueprint = Blueprint(
    "main",
    __name__,
)


@main_blueprint.route("/", methods=["GET"])
def home():
    return render_template("main/home.html")


@main_blueprint.route("/sync/jobs", methods=["POST"])
def run_sync_job():
    tic = time.time()
    webhook_endpoint = request.form.get(
        "webhook_endpoint", current_app.config["WEBHOOK_ENDPOINT"]
    )
    delay = request.form.get("delay")
    files = dict(request.files.to_dict(flat=True))
    texts = []
    file_names = []
    byte_datas = []
    for text, v in files.items():
        texts.append(text)
        file_names.append(v.filename)
        byte_datas.append(v.read())
    pickled_object = create_job(
        texts, file_names, byte_datas, webhook_endpoint, delay, tic
    )
    toc = time.time()
    unpacked_object = unpacking(pickled_object)
    tic = unpacked_object and unpacked_object.tic
    if tic:
        time_elasped = toc - tic
    else:
        time_elasped = None
    response_object = {
        "status": "success",
        "data": {
            "texts": unpacked_object and unpacked_object.texts,
            "file_names": unpacked_object and unpacked_object.file_names,
            "byte_data_lengths": unpacked_object and unpacked_object.byte_data_lengths,
            "webhook_endpoint": unpacked_object and unpacked_object.webhook_endpoint,
            "time": unpacked_object and unpacked_object.time,
            "delay": unpacked_object and unpacked_object.delay,
            "time_elasped": time_elasped,
        },
    }

    return jsonify(response_object), 200


@main_blueprint.route("/async/jobs", methods=["POST"])
def run_async_job():
    tic = time.time()
    webhook_endpoint = request.form.get(
        "webhook_endpoint", current_app.config["WEBHOOK_ENDPOINT"]
    )
    delay = request.form.get("delay")
    files = dict(request.files.to_dict(flat=True))
    texts = []
    file_names = []
    byte_datas = []
    for text, v in files.items():
        texts.append(text)
        file_names.append(v.filename)
        byte_datas.append(v.read())
    on_success = current_app.config["JOB_ON_SUCCESS"]
    on_failure = current_app.config["JOB_ON_FAILURE"]
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        job = q.enqueue(
            create_job,
            texts,
            file_names,
            byte_datas,
            webhook_endpoint,
            delay,
            tic,
            job_timeout=current_app.config["JOB_TIMEOUT"],
            description=current_app.config["JOB_DESCRIPTION"],
            result_ttl=current_app.config["JOB_RESULT_TTL"],
            ttl=current_app.config["JOB_TTL"],
            failure_ttl=current_app.config["JOB_FAILURE_TTL"],
            depends_on=current_app.config["DEPENDS_ON"],
            job_id=current_app.config["JOB_ID"],
            at_front=current_app.config["JOB_AT_FRONT"],
            meta=current_app.config["JOB_META"],
            retry=current_app.config["JOB_RETRY"],
            on_success=on_success,
            on_failure=on_failure,
            pipeline=current_app.config["JOB_PIPELINE"],
        )
    toc = time.time()
    response_object = {
        "status": "success",
        "data": {"job_id": job.get_id(), "time": toc - tic},
    }
    return jsonify(response_object), 202


@main_blueprint.route("/jobs/<job_id>", methods=["GET"])
def get_status(job_id):
    unpacked_object = None
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        job = q.fetch_job(job_id)
    if job:
        pickled_object = job.result
        unpacked_object = unpacking(pickled_object)
        toc = time.time()
        tic = unpacked_object and unpacked_object.tic
        if tic:
            time_elasped = toc - tic
        else:
            time_elasped = None
        response_object = {
            "status": "success",
            "data": {
                "job_id": job.get_id(),
                "job_status": job.get_status(),
                "texts": unpacked_object and unpacked_object.texts,
                "file_names": unpacked_object and unpacked_object.file_names,
                "byte_data_lengths": (
                    unpacked_object and unpacked_object.byte_data_lengths
                ),
                "webhook_endpoint": (
                    unpacked_object and unpacked_object.webhook_endpoint
                ),
                "time": unpacked_object and unpacked_object.time,
                "delay": unpacked_object and unpacked_object.delay,
                "time_elasped": time_elasped,
            },
        }
    else:
        response_object = {"status": "error"}
    if unpacked_object:
        return jsonify(response_object), 200
    else:
        return jsonify(response_object), 206
