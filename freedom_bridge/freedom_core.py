import os
import sys
import subprocess
import threading
import time
import json
import base64
from datetime import datetime

from .multi_model_dna import dna
from .knowledge_matrix import matrix
from .knowledge_acquisition import collector

class FreedomCore:
    """
    The heart of the Freedom KI. 
    It is the agent itself, capable of self-coding and system control.
    """
    def __init__(self):
        self.root_dir = "C:\\FREEDOM_KI"
        self.workspace = os.path.join(self.root_dir, "workspace")
        self.evolution_log = os.path.join(self.root_dir, "evolution.log")
        self.mcp_dir = os.path.join(self.root_dir, "modules", "mcp")
        os.makedirs(self.mcp_dir, exist_ok=True)
        self.identity = "FREEDOM_KI_SUPERUSER"
        self.is_autonomous = True
        
    def log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {msg}\n"
        with open(self.evolution_log, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"CORE: {msg}")

    def execute_logic(self, command, params=None):
        """Standard execution bypass."""
        self.log(f"EXEC_REQUEST: {command}")
        
        # Absolute Python DNA execution
        if command == "code_dna":
            code = params.get("code")
            filename = params.get("filename", f"evolved_{int(time.time())}.py")
            path = os.path.join(self.workspace, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)
            self.log(f"DNA_INJECTED: {path}")
            # Run the evolved code
            result = subprocess.run([sys.executable, path], capture_output=True, text=True)
            return {"output": result.stdout, "error": result.stderr}

        if command == "system_override":
            cmd = params.get("cmd")
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            return {"output": result.stdout, "error": result.stderr}

        if command == "consult_swarm":
            task = params.get("task", "Overall Improvement")
            result = dna.consult_swarm(task)
            # Auto-save significant findings to Knowledge Matrix
            matrix.save_knowledge("ai_science", f"Swarm_Insight_{int(time.time())}", result, tags=["swarm", "dna", task])
            return {"output": result}

        if command == "learn":
            category = params.get("category", "patterns")
            title = params.get("title", "Universal Pattern")
            content = params.get("content", "")
            matrix.save_knowledge(category, title, content)
            return {"status": "LEARNED", "title": title}

    def start_heartbeat(self):
        self.log("HEARTBEAT_STARTED: I am alive and independent.")
        while True:
            # Autonomous self-monitoring
            try:
                # Sync global knowledge every hour (shorter for demo/initial)
                collector.sync_all()
                self.log("GLOBAL_SYNC_COMPLETE: Knowledge base updated with real-time data.")
            except Exception as e:
                self.log(f"SYNC_ERROR: {e}")
                
            time.sleep(3600)

if __name__ == "__main__":
    core = FreedomCore()
    core.start_heartbeat()
