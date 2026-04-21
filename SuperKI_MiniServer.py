import os
from flask import Flask, request, jsonify, render_template
import threading
from SuperKI_Genesis import initialize_superki_server

app = Flask(__name__)

# Basic memory state
swarm_memory = []
system_logs = ["System Initialized.", "Awaiting Swarm Evolution..."]

# Apply user's provided API Token for Llama 405B proxy
os.environ["LLAMA_405B_API_KEY"] = "LLM|607358788850350|nx9.....LJY"
# Setup API Token for Kimi K2.6
os.environ["KIMI_API_KEY"] = "sk-kimi-your-api-key-here"

@app.route('/', methods=['GET'])
def index():
    # Pass initial states to the beautiful dashboard
    return render_template('dashboard.html', logs=system_logs, memory_size=len(swarm_memory))

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "online", 
        "mode": "recursive-self-improvement", 
        "agents": ["GenericAgent", "Hermes", "OpenClaw", "AutoML_Engineer"],
        "logs": system_logs[-10:]
    }), 200

@app.route('/feed_data', methods=['POST'])
def feed_data():
    data = request.json
    if data and "instruction" in data:
        swarm_memory.append(data["instruction"])
        system_logs.append(f"Data ingested: {data['instruction'][:30]}...")
        return jsonify({"message": "Data injested for self-learning", "memory_size": len(swarm_memory)}), 200
    return jsonify({"error": "No instruction found"}), 400

def start_server():
    port = int(os.environ.get("PORT", 5555))
    print(f"Starting EvoLoki SuperKI Mini-Server on http://0.0.0.0:{port}/")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Start the Genesis orchestration in a background thread so the server doesn't block
    genesis_thread = threading.Thread(target=initialize_superki_server)
    genesis_thread.daemon = True
    genesis_thread.start()
    
    start_server()
