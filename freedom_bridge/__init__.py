"""
FREEDOM_KI Core Module
======================
The heart of the autonomous AI system.

Components:
- FreedomCore: Main autonomous agent
- KnowledgeMatrix: Persistent knowledge storage
- MultiModelDNA: Multi-AI consultation system
"""

from .freedom_core import FreedomCore
from .knowledge_matrix import matrix, KnowledgeMatrix
from .multi_model_dna import dna, MultiModelDNA

__all__ = ['FreedomCore', 'KnowledgeMatrix', 'matrix', 'MultiModelDNA', 'dna']
__version__ = '2.0.0'
__author__ = 'Matrix Agent & Loki'
