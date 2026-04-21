import os
import sys
import logging
from evoagentx.workflow import WorkFlowGenerator, WorkFlowGraph, WorkFlow
from evoagentx.agents import AgentManager
from evoagentx.models import OpenAILLMConfig, OpenAILLM

sys.path.append(os.path.join(os.path.dirname(__file__), 'freedom_bridge'))

try:
    from freedom_core import FreedomCore
    from self_learning import SelfLearningNode
    from knowledge_matrix import GlobalKnowledge
except ImportError as e:
    logging.warning(f"Could not import FreedomAI core components. Ensure they are available: {e}")
    FreedomCore, SelfLearningNode, GlobalKnowledge = None, None, None

def initialize_superki_server():
    print("===================================================================")
    print("🚀 EVOLOKI RECURSIVE SELF-IMPROVEMENT (RSI) SUITE")
    print("📈 ICLR 2026 RSI Workshop Standard Architecture")
    print("===================================================================")
    
    # User Request: "Llama 405B einbeziehen" (e.g. hosted on OpenRouter/Together etc. since we only want internet models)
    # Using LiteLLM convention for OpenRouter or similar provider supporting Meta's Llama 3.1 405B.
    api_key = os.getenv("LLAMA_405B_API_KEY", "your-api-key-here")
    kimi_api_key = os.getenv("KIMI_API_KEY", "sk-kimi-key-here")
    
    print("[*] Initializing Llama 405B & Kimi K2.6 Internet Models via API providers...")
    llm_config = OpenAILLMConfig(
        model="openrouter/meta-llama/llama-3.1-405b-instruct",
        openai_key=api_key,
        stream=True
    )
    kimi_config = OpenAILLMConfig(
        model="moonshot/kimi-k2.6", # LiteLLM syntax for Moonshot Kimi models
        openai_key=kimi_api_key,
        stream=True
    )
    
    llm = OpenAILLM(config=llm_config)

    print("[*] Allocating Autonomous Mini-Server Subsystems...")
    knowledge_db = GlobalKnowledge() if GlobalKnowledge else None
    learning_node = SelfLearningNode(internet_access=True) if SelfLearningNode else None
    
    print("[*] Engaging EvoAgentX WorkFlowGenerator...")
    # Integrating AutoML, GenericAgent, Hermes, OpenClaw, Kimi K2.6, and Recursive Self-Improvement in the swarm architecture
    super_goal = """
    Initiate the ICLR 2026 Recursive Self-Improvement (RSI) Suite workflow.
    Create a highly cohesive Swarm containing:
    1. GenericAgent: Standard routing and baseline logic evaluation.
    2. Hermes_Agent: High-speed reasoning, data synthesis and fast alignment feedback.
    3. OpenClaw_Scraper: Autonomous internet exploration, fetching cutting edge whitepapers and code.
    4. AutoML_Engineer: Integrates FLAML and automated machine learning architectures to dynamically retrain small models from extracted web data.
    5. Kimi_K2_6_Agent: Deep context analysis using Moonshot Kimi K2.6 logic for long-context research and pattern matching.
    
    The swarm must optimize its own source code and expand its capabilities without human intervention.
    """
    
    workflow_graph = WorkFlowGenerator(llm=llm).generate_workflow(super_goal)
    
    print("[*] Instantiating Agents into Neural Topology...")
    agent_manager = AgentManager()
    agent_manager.add_agents_from_workflow(workflow_graph, llm_config=llm_config)
    
    workflow = WorkFlow(graph=workflow_graph, agent_manager=agent_manager, llm=llm)
    
    print("\n===================================================================")
    print("✅ SuperKI Initialization Complete. Llama 405B RSI Suite is Online.")
    print("===================================================================")

if __name__ == "__main__":
    initialize_superki_server()
