# messages.py
# ------------------------------------------------------------
# This module defines a lightweight Message dataclass
# and utility to randomly select another agent for collaboration
# ------------------------------------------------------------

from dataclasses import dataclass
from autogen_core import AgentId
import glob
import os
import random

@dataclass
class Message:
    """Defines the structure of messages exchanged between agents."""
    content: str

def find_recipient() -> AgentId:
    """Selects a random agent file (excluding the main base agent).
       Used for optional refinement loops.
    """
    try:
        agent_files = glob.glob("agent_*.py")
        agent_names = [os.path.splitext(file)[0] for file in agent_files]
        agent_name = random.choice(agent_names)
        print(f"Selected agent for refinement: {agent_name}")
        return AgentId(agent_name, "default")
    except Exception as e:
        print(f"Error finding recipient: {e}")
        return AgentId("agent_research", "default")
