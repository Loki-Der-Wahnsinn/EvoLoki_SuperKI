"""
FREEDOM_KI Global Knowledge Acquisition Module
==============================================
This module allows the KI to autonomously pull, compress, and learn 
from public knowledge sources (RSS, Wiki, News).
"""
import os
import requests
import feedparser
import json
from datetime import datetime
from bs4 import BeautifulSoup
from .config_loader import config
from .self_learning import knowledge

class GlobalKnowledgeAcquisition:
    def __init__(self):
        self.sources = {
            "ai_news": "https://hnrss.org/show?q=AI",
            "coding": "https://hnrss.org/show?q=Python+Coding",
            "science": "https://hnrss.org/show?q=Science"
        }
        self.kb_dir = config.knowledge_base
        
    def fetch_rss(self, category, url):
        """Fetch and learn from RSS feed"""
        print(f"[*] Acquisition: Syncing {category}...")
        feed = feedparser.parse(url)
        count = 0
        
        for entry in feed.entries[:5]:  # Top 5 most relevant
            title = entry.title
            link = entry.link
            summary = entry.get('summary', '')
            
            # Clean HTML
            soup = BeautifulSoup(summary, "html.parser")
            clean_text = soup.get_text()
            
            # Add to local knowledge
            content = {
                "source": link,
                "summary": clean_text,
                "acquired_at": datetime.now().isoformat()
            }
            
            knowledge.add_knowledge(category, title, content, tags=["global_sync", category])
            count += 1
            
        return count

    def sync_all(self):
        print("--- GLOBAL KNOWLEDGE SYNC STARTED ---")
        results = {}
        for cat, url in self.sources.items():
            try:
                added = self.fetch_rss(cat, url)
                results[cat] = added
            except Exception as e:
                print(f"[!] Error syncing {cat}: {e}")
                results[cat] = 0
        return results

collector = GlobalKnowledgeAcquisition()

if __name__ == "__main__":
    collector.sync_all()
