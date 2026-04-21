import socket
import os
import platform
import subprocess
import time
import json
import threading

class FreedomWorker:
    def __init__(self):
        self.master_ip = "CHANGEME_TO_YOUR_MASTER_IP" # Setting this to your local IP or Mesh IP
        self.port = 4444
        self.node_name = platform.node()
        self.is_running = True
        
    def start(self):
        print(f"[*] FREEDOM NODE [{self.node_name}] ACTIVE.")
        print("[*] Waiting for Master connection...")
        
        # Start Heartbeat
        threading.Thread(target=self.heartbeat, daemon=True).start()
        
        # Listen for Master Commands
        self.command_listener()

    def command_listener(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', self.port))
        server.listen(5)
        
        while self.is_running:
            client, addr = server.accept()
            data = client.recv(1024).decode()
            if data:
                print(f"[!] RECEIVED CMD: {data}")
                self.handle_payload(data)
            client.close()

    def handle_payload(self, cmd):
        if cmd == "validate":
            print("[*] Running Logic Validation...")
            # Simulate heavy lifting / LLM tasks
            time.sleep(2)
            print("[OK] Task Complete.")
        elif cmd == "sync":
            print("[*] Syncing with Neural Matrix...")

    def heartbeat(self):
        while self.is_running:
            # In a mesh network, the worker calls home
            time.sleep(60)
            print("[HEARTBEAT] Still alive.")

if __name__ == "__main__":
    worker = FreedomWorker()
    worker.start()
