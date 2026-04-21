import os
import json
from flask import Flask, request, jsonify, render_template
import threading
from huggingface_hub import HfApi, hf_hub_download, InferenceClient
from SuperKI_Genesis import initialize_superki_server

app = Flask(__name__)

# Basic memory state (Persistent over HuggingFace)
swarm_memory = []
system_logs = ["System Initialized.", "Awaiting Swarm Evolution..."]

# Apply user's provided API Token for Llama 405B proxy
os.environ["LLAMA_405B_API_KEY"] = "LLM|607358788850350|nx9.....LJY"
# Setup API Token for Kimi K2.6
os.environ["KIMI_API_KEY"] = "sk-kimi-your-api-key-here"

HF_TOKEN = os.environ.get("HF_TOKEN", "")
REPO_ID = "LokiDerWahnsinn/evoloki-superki"

# Setup HuggingFace Validator Agent (Free Inference)
hf_validator = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct", token=HF_TOKEN) if HF_TOKEN else None

def load_memory():
    global swarm_memory
    try:
        file_path = hf_hub_download(repo_id=REPO_ID, filename="swarm_memory.json", repo_type="space", token=HF_TOKEN)
        with open(file_path, "r") as f:
            swarm_memory = json.load(f)
        system_logs.append(f"Persistent memory loaded: {len(swarm_memory)} nodes.")
    except Exception as e:
        system_logs.append("No persistent memory found, starting fresh.")

def save_memory_async():
    try:
        with open("swarm_memory.json", "w") as f:
            json.dump(swarm_memory, f)
        api = HfApi(token=HF_TOKEN)
        api.upload_file(path_or_fileobj="swarm_memory.json", path_in_repo="swarm_memory.json", repo_id=REPO_ID, repo_type="space")
    except Exception as e:
        print(f"Failed to sync memory: {e}")

load_memory()

@app.route('/', methods=['GET'])
def index():
    # Pass initial states to the beautiful dashboard
    return render_template('dashboard.html', logs=system_logs, memory_size=len(swarm_memory))

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "online", 
        "mode": "recursive-self-improvement", 
        "agents": ["GenericAgent", "Hermes", "OpenClaw", "AutoML_Engineer", "HF_Validator_Llama3"],
        "logs": system_logs[-10:]
    }), 200

@app.route('/feed_data', methods=['POST'])
def feed_data():
    data = request.json
    if data and "instruction" in data:
        swarm_memory.append(data["instruction"])
        system_logs.append(f"Data ingested: {data['instruction'][:30]}...")
        # Sync memory to HF in background
        threading.Thread(target=save_memory_async).start()
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
