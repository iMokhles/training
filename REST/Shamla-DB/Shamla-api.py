#! todo-API using flask

from flask import Flask, jsonify, abort, make_response, request
from types import *

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]
@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_all_tasks():
   return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id=None):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    return jsonify({'tasks': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not Found'}), 404)


@app.route('/todo/api/v1.0/tasks', methods = ['POST'])
def create_task():
    print (request.json)
    print (request)
    if not request.json or not 'title' in request.json:
        abort(400)
    task ={
        'id' : tasks[-1]['id'] + 1,
        'title' : request.json['title'],
        'description' : request.json.get('description', ''),
        'done' : False
    }
    tasks.append(task)
    return jsonify({'task' : task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        print('not found')
        abort(404)
    if task_id is None:
        abort(400)
    if not request.json:
        print ('no json')
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        print('title is not string')
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        print ('description not str')
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        print ('done is not bool')
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify( { 'task': task[0] } )

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
def delete_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify( { 'result': True } )


if __name__ == '__main__':
    app.run(debug = True)



