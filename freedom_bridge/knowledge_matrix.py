"""
FREEDOM_KI Knowledge Matrix v2.0
================================
Permanent memory with error handling and config support.
"""
import os, json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from .config_loader import config
    ROOT_DIR = config.knowledge_base
except:
    ROOT_DIR = Path("C:/FREEDOM_KI/knowledge_base")

class KnowledgeMatrix:
    DEFAULT_CATEGORIES = ["coding", "ai_science", "networks", "servers", "patterns"]
    
    def __init__(self, root_dir=None):
        self.root = Path(root_dir) if root_dir else ROOT_DIR
        self.categories = self.DEFAULT_CATEGORIES.copy()
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        try:
            self.root.mkdir(parents=True, exist_ok=True)
            for cat in self.categories:
                (self.root / cat).mkdir(exist_ok=True)
        except Exception as e:
            print(f"Warning: {e}")
    
    def save_knowledge(self, category, title, content, tags=None):
        if category not in self.categories:
            category = "patterns"
        entry = {
            "timestamp": datetime.now().isoformat(),
            "title": title, "category": category,
            "content": content, "tags": tags or [],
            "meta": {"times_accessed": 0, "usefulness_score": 0.5}
        }
        filename = "".join(c if c.isalnum() else "_" for c in title) + ".json"
        path = self.root / category / filename
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(entry, f, indent=2, default=str)
            print(f"KNOWLEDGE_LOCKED: {title} in {category}")
            return path
        except Exception as e:
            print(f"ERROR saving: {e}")
            return None

    def query_knowledge(self, category=None, search=None):
        results = []
        dirs = [self.root / category] if category in self.categories else [self.root / d for d in self.categories]
        for d in dirs:
            if not d.exists(): continue
            try:
                for f in d.glob("*.json"):
                    try:
                        data = json.loads(f.read_text(encoding="utf-8"))
                        if search and search.lower() not in str(data).lower():
                            continue
                        results.append(data)
                    except: pass
            except: pass
        return sorted(results, key=lambda x: x.get("meta",{}).get("usefulness_score",0), reverse=True)
    
    def get_statistics(self):
        stats = {"total": 0, "by_category": {}}
        for cat in self.categories:
            count = len(list((self.root / cat).glob("*.json"))) if (self.root / cat).exists() else 0
            stats["by_category"][cat] = count
            stats["total"] += count
        return stats

matrix = KnowledgeMatrix()
