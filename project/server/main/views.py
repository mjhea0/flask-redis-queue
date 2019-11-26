# project/server/main/views.py


from flask import render_template, Blueprint, jsonify, request

main_blueprint = Blueprint("main", __name__,)


@main_blueprint.route("/", methods=["GET"])
def home():
    return render_template("main/home.html")


@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    task_type = request.form["type"]
    return jsonify(task_type), 202


@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    return jsonify(task_id)
