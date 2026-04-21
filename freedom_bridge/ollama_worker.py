"""
FREEDOM_KI Ollama Worker Agent
==============================
This agent communicates with the local Ollama instance 
and processes tasks provided by the Master Core.
"""
import requests
import json
import time
import subprocess
import os
from datetime import datetime

class OllamaWorker:
    def __init__(self, model="llama3:8b"):
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"
        self.log_file = "P:/FREEDOM_KI/evolution.log"
        
    def log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [OLLAMA_WORKER] {msg}\n"
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"OLLAMA_WORKER: {msg}")

    def ensure_ollama_running(self):
        """Try to start Ollama if it's not responding"""
        try:
            requests.get("http://localhost:11434")
            return True
        except:
            self.log("Ollama not responding. Attempting to start service...")
            subprocess.Popen(["ollama", "serve"], creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(5)
            return True

    def think(self, prompt, context=""):
        """Process a prompt through local Ollama"""
        if not self.ensure_ollama_running():
            return "Error: Ollama not available"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=60)
            if response.status_code == 200:
                result = response.json().get("response", "")
                self.log(f"Processed task. Output length: {len(result)}")
                return result
            else:
                return f"Error: API returned {response.status_code}"
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

    def autonomous_loop(self):
        """Check for tasks in the workspace or from other agents"""
        self.log(f"Ollama Worker ({self.model}) is ONLINE.")
        while True:
            # Here we could poll a task queue file or directory
            # For now, it pulse-checks the system
            time.sleep(30)

if __name__ == "__main__":
    worker = OllamaWorker()
    worker.autonomous_loop()
