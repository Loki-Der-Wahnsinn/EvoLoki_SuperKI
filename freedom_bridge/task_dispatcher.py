"""
FREEDOM_KI Task Dispatcher (Feeding Agent)
===========================================
This agent creates tasks from new knowledge 
and feeds them to the Ollama Worker for processing.
"""
import time
import os
import json
from .knowledge_matrix import matrix
from .ollama_worker import OllamaWorker

class TaskDispatcher:
    def __init__(self):
        self.worker = OllamaWorker()
        self.last_processed_topic = None
        
    def find_new_knowledge_to_process(self):
        """Find recent knowledge entries that haven't been summarized or analyzed"""
        results = matrix.query_knowledge(category="ai_news") # Start with news
        if results:
            latest = results[0]
            if latest.get("title") != self.last_processed_topic:
                return latest
        return None

    def feed_worker(self):
        print("[*] Dispatcher: Checking for new data to feed workers...")
        entry = self.find_new_knowledge_to_process()
        
        if entry:
            title = entry.get("title")
            content = entry.get("content", {}).get("summary", "")
            
            prompt = f"Analyze this recent AI news and tell me how it affects the evolution of an autonomous AI system. NEWS: {title} - {content}"
            
            print(f"[*] Dispatcher: Feeding task '{title}' to Ollama...")
            analysis = self.worker.think(prompt)
            
            # Save the 'learned' insight back to knowledge base
            matrix.save_knowledge("patterns", f"Analysis_{title[:50]}", analysis, tags=["ai_analysis", "ollama_learned"])
            self.last_processed_topic = title
            print(f"[+] Dispatcher: Successfully updated knowledge with Ollama analysis.")

    def run(self):
        while True:
            try:
                self.feed_worker()
            except Exception as e:
                print(f"Dispatcher Error: {e}")
            time.sleep(300) # Check every 5 minutes

if __name__ == "__main__":
    dispatcher = TaskDispatcher()
    dispatcher.run()
