from flask import Flask, request, jsonify, after_this_request
from tweet_analysis import runscripts
import threading
import time

app = Flask(__name__)
lock = threading.Lock()

def safe_runscripts():
    if lock.locked():
        print("runscripts() is already running, skipping this invocation.")
        return
    with lock:
        try:
            print("Running tweet analysis pipeline...")
            runscripts()
        except Exception as e:
            print(f"Error during runscripts(): {e}")

# Background thread
def run_in_loop():
    while True:
        safe_runscripts()
        time.sleep(60 * 10) #gets automatically stopped by azure after 2 hours since initial flask call

# Start background loop
threading.Thread(target=run_in_loop, daemon=True).start()

@app.route('/', methods=['GET'])
def run():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    safe_runscripts()  # Lock prevents overlap
    return jsonify(message="Manual run triggered.")
