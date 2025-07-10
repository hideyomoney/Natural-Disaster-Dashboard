from flask import Flask, request, jsonify, after_this_request
from tweet_analysis import runscripts
import threading
import os

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

@app.route('/', methods=['GET'])
def run():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    safe_runscripts()  # Lock prevents overlap
    return jsonify(message="Manual run triggered.")

#  This is what Render needs:
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
