from flask import Flask, request, jsonify
# from celery import Celery # Cannot be used on windows os since redis cannot be installed
from multiprocessing import Process
from flask_cors import CORS
from collections import defaultdict

from utils import log
from boatCourse import main

app = Flask(__name__)
CORS(app) # Without CORS configured, any requests involving data mutation, such as POST, PUT, PATCH, and DELETE, would be blocked

@app.route("/api/healthchecker", methods=["GET"])
def healthchecker():
  return {"status": "success", "message": "Integrate Flask Framework with Next.js"}


def computeCourse(start, end):
  try:
    main(start, end)
    log({'status': 'Completed'}) 
    
  except Exception as e:
    log({'status': 'Failed', 'error': str(e)})
  

@app.route('/api/receive-data', methods=['POST'])
def receive_data():
  data = request.get_json()  # Get JSON data from the request
  log(f"Received data: {data}")  # Print for debugging
  content = data.get("message")
  log(content)
  if len(content) > 2:
      content = content[:2]
    
  start = tuple(content[0])
  end = tuple(content[1])
  log(f"Start: {start}, End: {end}")
  process = Process(target=computeCourse, args=(start, end)) # Start the task
  process.start()
  return jsonify({'message': "Data received successfully!", 'status': 'Processing started'}), 200
  


# @app.route("/api/todos/<int:todo_id>", methods=["GET"])
# def get_todo_item(todo_id):
#     todo = next((todo for todo in todos if todo["id"] == todo_id), None)
#     if todo:
#         return todo
#     return {"error": "Todo item not found"}, 404


# @app.route("/api/todos", methods=["POST"])
# def create_todo_item():
#     data = request.get_json()
#     title = data.get("title")
#     if not title:
#         return {"error": "Title is required"}, 400

#     global todo_id_counter
#     todo = {
#         "id": todo_id_counter,
#         "title": title,
#         "completed": False
#     }
#     todos.append(todo)
#     todo_id_counter += 1
#     return todo, 201


# @app.route("/api/todos/<int:todo_id>", methods=["PATCH"])
# def update_todo_item(todo_id):
#     data = request.get_json()
#     title = data.get("title")
#     completed = data.get("completed")

#     todo = next((todo for todo in todos if todo["id"] == todo_id), None)
#     if todo:
#         if title is not None:
#             todo["title"] = title
#         if completed is not None:
#             todo["completed"] = completed
#         return todo
#     return {"error": "Todo item not found"}, 404


# @app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
# def delete_todo_item(todo_id):
#     global todos
#     todos = [todo for todo in todos if todo["id"] != todo_id]
#     return {"message": "Todo item deleted"}


# @app.route("/api/healthchecker", methods=["GET"])
# def healthchecker():
#     return {"status": "success", "message": "Integrate Flask Framework with Next.js"}


if __name__ == "__main__":
    app.run()
