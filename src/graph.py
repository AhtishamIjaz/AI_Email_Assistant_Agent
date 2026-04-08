from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from src.agents import email_sorter_agent, email_drafter_agent, email_critic_agent
from utils.logger import logger

# 1. Define the "Notebook" (State) that agents share
class AgentState(TypedDict):
    email_content: str
    category: Optional[str]
    draft: Optional[str]
    final_email: Optional[str]

# 2. Define the Nodes (The Actions)
def sort_node(state: AgentState):
    category = email_sorter_agent(state['email_content'])
    return {"category": category}

def draft_node(state: AgentState):
    # Only draft if it's not Spam
    if state['category'] == "Spam":
        return {"draft": "No response needed for spam."}
    
    draft = email_drafter_agent(state['category'], state['email_content'])
    return {"draft": draft}

def criticize_node(state: AgentState):
    if state['category'] == "Spam":
        return {"final_email": "Filtered"}
        
    final = email_critic_agent(state['draft'])
    return {"final_email": final}

# 3. Build the Graph
def create_email_graph():
    workflow = StateGraph(AgentState)

    # Add our Workers (Nodes)
    workflow.add_node("sorter", sort_node)
    workflow.add_node("drafter", draft_node)
    workflow.add_node("critic", criticize_node)

    # Define the Path (Edges)
    workflow.set_entry_point("sorter")
    workflow.add_edge("sorter", "drafter")
    workflow.add_edge("drafter", "critic")
    workflow.add_edge("critic", END)

    # Compile the Brain
    return workflow.compile()

# Initialize the global graph instance
email_processor = create_email_graph()