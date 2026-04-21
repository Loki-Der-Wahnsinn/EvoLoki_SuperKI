"""
FREEDOM_KI Self-Learning Knowledge System
==========================================
"Learning by Doing" - The AI learns from every interaction!

This system:
1. Records all interactions and outcomes
2. Identifies patterns in successful operations
3. Automatically improves knowledge base
4. Adapts strategies based on results

Author: Matrix Agent & Loki
Version: 2.0.0
"""

import os
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from collections import defaultdict

try:
    from .config_loader import config
except ImportError:
    config = None


class LearningMemory:
    """Short-term and long-term memory for learning"""
    
    def __init__(self, memory_file: Path):
        self.memory_file = memory_file
        self.short_term = []  # Recent interactions
        self.long_term = self._load_memory()
        self.max_short_term = 100
        
    def _load_memory(self) -> Dict:
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"patterns": {}, "successes": [], "failures": [], "insights": []}
    
    def save(self):
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.long_term, f, indent=2, default=str)
    
    def remember(self, event: Dict):
        """Add event to short-term memory"""
        event['timestamp'] = datetime.now().isoformat()
        self.short_term.append(event)
        if len(self.short_term) > self.max_short_term:
            self._consolidate()
    
    def _consolidate(self):
        """Move patterns from short-term to long-term memory"""
        # Extract patterns from short-term memory
        patterns = self._extract_patterns()
        for pattern_id, pattern_data in patterns.items():
            if pattern_id in self.long_term["patterns"]:
                self.long_term["patterns"][pattern_id]["count"] += 1
                self.long_term["patterns"][pattern_id]["last_seen"] = datetime.now().isoformat()
            else:
                self.long_term["patterns"][pattern_id] = pattern_data
        
        self.short_term = self.short_term[-20:]  # Keep recent 20
        self.save()
    
    def _extract_patterns(self) -> Dict:
        """Identify recurring patterns in interactions"""
        patterns = {}
        action_sequences = defaultdict(int)
        
        for event in self.short_term:
            action = event.get('action', 'unknown')
            result = event.get('result', 'unknown')
            key = f"{action}:{result}"
            action_sequences[key] += 1
        
        for key, count in action_sequences.items():
            if count >= 2:  # Pattern threshold
                pattern_id = hashlib.md5(key.encode()).hexdigest()[:8]
                patterns[pattern_id] = {
                    "pattern": key,
                    "count": count,
                    "first_seen": datetime.now().isoformat(),
                    "last_seen": datetime.now().isoformat()
                }
        
        return patterns


class SelfLearningKnowledge:
    """
    Self-improving knowledge system that learns from:
    1. User interactions
    2. Task outcomes (success/failure)
    3. Pattern recognition
    4. External knowledge integration
    """
    
    def __init__(self, knowledge_dir: Path = None):
        if knowledge_dir:
            self.knowledge_dir = Path(knowledge_dir)
        elif config:
            self.knowledge_dir = config.knowledge_base
        else:
            self.knowledge_dir = Path("C:/FREEDOM_KI/knowledge_base")
        
        self.learning_dir = self.knowledge_dir / "_learning"
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        self.memory = LearningMemory(self.learning_dir / "memory.json")
        self.knowledge_index = self._build_index()
        self.learning_log = self.learning_dir / "learning_log.jsonl"
        
    def _build_index(self) -> Dict:
        """Index all knowledge files for quick access"""
        index = {}
        for category_dir in self.knowledge_dir.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('_'):
                for knowledge_file in category_dir.glob("*.json"):
                    try:
                        with open(knowledge_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        topic = data.get('topic', knowledge_file.stem)
                        index[topic] = {
                            "path": str(knowledge_file),
                            "category": category_dir.name,
                            "meta": data.get('meta', {})
                        }
                    except:
                        continue
        return index
    
    def learn_from_interaction(self, action: str, context: Dict, result: str, success: bool):
        """
        Learn from every interaction!
        
        Args:
            action: What was attempted
            context: Relevant context/parameters
            result: What happened
            success: Was it successful?
        """
        event = {
            "action": action,
            "context": context,
            "result": result,
            "success": success
        }
        
        self.memory.remember(event)
        
        # Log for analysis
        self._log_learning(event)
        
        # If successful, extract and save insights
        if success:
            self._extract_insight(action, context, result)
        
        # Update knowledge usefulness scores
        self._update_knowledge_scores(context, success)
    
    def _log_learning(self, event: Dict):
        """Append to learning log (JSONL format)"""
        try:
            with open(self.learning_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event, default=str) + '\n')
        except:
            pass
    
    def _extract_insight(self, action: str, context: Dict, result: str):
        """Extract reusable insight from successful action"""
        insight = {
            "action_type": action,
            "success_factors": list(context.keys()),
            "outcome": result[:200],  # Truncate
            "learned_at": datetime.now().isoformat()
        }
        
        if "insights" not in self.memory.long_term:
            self.memory.long_term["insights"] = []
        
        self.memory.long_term["insights"].append(insight)
        
        # Keep only recent 1000 insights
        if len(self.memory.long_term["insights"]) > 1000:
            self.memory.long_term["insights"] = self.memory.long_term["insights"][-1000:]
        
        self.memory.save()
    
    def _update_knowledge_scores(self, context: Dict, success: bool):
        """Update usefulness scores of accessed knowledge"""
        accessed_topics = context.get('accessed_knowledge', [])
        
        for topic in accessed_topics:
            if topic in self.knowledge_index:
                path = Path(self.knowledge_index[topic]["path"])
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if 'meta' not in data:
                        data['meta'] = {}
                    
                    data['meta']['times_accessed'] = data['meta'].get('times_accessed', 0) + 1
                    
                    # Adjust usefulness score
                    current = data['meta'].get('usefulness_score', 0.5)
                    adjustment = 0.01 if success else -0.005
                    data['meta']['usefulness_score'] = max(0, min(1, current + adjustment))
                    data['meta']['last_accessed'] = datetime.now().isoformat()
                    
                    with open(path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2)
                except:
                    pass
    
    def query_knowledge(self, query: str, category: str = None) -> List[Dict]:
        """
        Search knowledge base with learning tracking
        """
        results = []
        query_lower = query.lower()
        
        for topic, info in self.knowledge_index.items():
            if category and info["category"] != category:
                continue
            
            if query_lower in topic.lower():
                try:
                    with open(info["path"], 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    results.append({
                        "topic": topic,
                        "category": info["category"],
                        "data": data
                    })
                except:
                    continue
        
        # Sort by usefulness score
        results.sort(key=lambda x: x["data"].get("meta", {}).get("usefulness_score", 0), reverse=True)
        
        return results
    
    def add_knowledge(self, category: str, topic: str, content: Dict, tags: List[str] = None):
        """
        Add new knowledge to the base
        """
        category_dir = self.knowledge_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Sanitize filename
        filename = "".join(c if c.isalnum() or c in '._- ' else '_' for c in topic)
        filepath = category_dir / f"{filename}.json"
        
        knowledge = {
            "topic": topic,
            "category": category,
            "created": datetime.now().isoformat(),
            "content": content,
            "tags": tags or [],
            "meta": {
                "times_accessed": 0,
                "usefulness_score": 0.5,
                "source": "self_learned"
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(knowledge, f, indent=2)
        
        # Update index
        self.knowledge_index[topic] = {
            "path": str(filepath),
            "category": category,
            "meta": knowledge["meta"]
        }
        
        return filepath
    
    def get_recommendations(self, context: str) -> List[str]:
        """
        Get knowledge recommendations based on context and past successes
        """
        recommendations = []
        
        # Find patterns that match context
        for pattern_id, pattern_data in self.memory.long_term.get("patterns", {}).items():
            if context.lower() in pattern_data.get("pattern", "").lower():
                recommendations.append(f"Pattern: {pattern_data['pattern']} (seen {pattern_data['count']} times)")
        
        # Find relevant insights
        for insight in self.memory.long_term.get("insights", [])[-50:]:
            if context.lower() in insight.get("action_type", "").lower():
                recommendations.append(f"Insight: {insight['action_type']} -> {insight['outcome'][:100]}")
        
        return recommendations[:10]
    
    def get_statistics(self) -> Dict:
        """Get learning statistics"""
        return {
            "total_topics": len(self.knowledge_index),
            "categories": list(set(info["category"] for info in self.knowledge_index.values())),
            "patterns_learned": len(self.memory.long_term.get("patterns", {})),
            "insights_gained": len(self.memory.long_term.get("insights", [])),
            "memory_events": len(self.memory.short_term)
        }


# Singleton instance
knowledge = SelfLearningKnowledge()


# Convenience functions
def learn(action: str, context: Dict, result: str, success: bool):
    """Quick function to record learning"""
    knowledge.learn_from_interaction(action, context, result, success)

def query(search: str, category: str = None) -> List[Dict]:
    """Quick function to query knowledge"""
    return knowledge.query_knowledge(search, category)

def add(category: str, topic: str, content: Dict, tags: List[str] = None):
    """Quick function to add knowledge"""
    return knowledge.add_knowledge(category, topic, content, tags)

def recommend(context: str) -> List[str]:
    """Quick function to get recommendations"""
    return knowledge.get_recommendations(context)


if __name__ == "__main__":
    # Demo
    print("=== FREEDOM_KI Self-Learning System ===")
    print(f"Statistics: {knowledge.get_statistics()}")
    
    # Simulate learning
    learn("file_read", {"file": "test.py"}, "Successfully read file", True)
    learn("code_execute", {"code": "print('hello')"}, "Executed without errors", True)
    
    print(f"After learning: {knowledge.get_statistics()}")
