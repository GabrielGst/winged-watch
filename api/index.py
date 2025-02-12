from flask import Flask, request, jsonify
# from celery import Celery # Cannot be used on windows os since redis cannot be installed
from multiprocessing import Process
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from modUtils import log
import modOptim as optim
import modRetrieve as retrieve

def dailyForecast():
  log("Processing to daily retrieve.")
  retrieve.main(force_export=False)

def computeCourse(start, end):
  log("Processing to compute course.")
  try:
    optim.main(start, end)
    log({'status': 'Completed'}) 
    
  except Exception as e:
    log({'status': 'Failed', 'error': str(e)})



app = Flask(__name__)
CORS(app) # Without CORS configured, any requests involving data mutation, such as POST, PUT, PATCH, and DELETE, would be blocked

scheduler = BackgroundScheduler()
scheduler.add_job(func=dailyForecast, trigger="interval", days=1)
scheduler.start()

@app.route("/api/healthchecker", methods=["GET"])
def healthchecker():
  return {"status": "success", "message": "Integrate Flask Framework with Next.js"}

@app.route('/api/receive-data', methods=['POST'])
def receive_data():
  data = request.get_json()  # Get JSON data from the request
  log(f"Received data: {data}")  # Print for debugging
  content = data.get("message")
  
  if len(content) > 2:
      content = content[:2] # for v2 of the API, we will provide a course with several destinations
    
  start, end = tuple(content[0]), tuple(content[1])
  log(f"Starting optimization. Start: {start}, End: {end}")
  process = Process(target=computeCourse, args=(start, end)) # Start the task
  process.start()
  
  return jsonify({'message': "Data received successfully!", 'status': 'Processing started'}), 200

# Ensure scheduler stops when the app exits
atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
  app.run(debug=True)