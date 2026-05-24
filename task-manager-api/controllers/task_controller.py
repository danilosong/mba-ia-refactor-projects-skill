from flask import jsonify, request

from services.task_service import TaskService


task_service = TaskService()


def get_tasks():
    return jsonify(task_service.list_tasks()), 200


def get_task(task_id):
    return jsonify(task_service.get_task(task_id)), 200


def create_task():
    return jsonify(task_service.create_task(request.get_json())), 201


def update_task(task_id):
    return jsonify(task_service.update_task(task_id, request.get_json())), 200


def delete_task(task_id):
    task_service.delete_task(task_id)
    return jsonify({"message": "Task deletada com sucesso"}), 200


def search_tasks():
    return jsonify(task_service.search_tasks(request.args)), 200


def task_stats():
    return jsonify(task_service.stats()), 200
