# creator.py
# ------------------------------------------------------------
# Purpose:
#   Dynamically registers all specialized agents for the
#   AI Startup Studio using Autogen's gRPC runtime.
#
# Key Fix:
#   Ensures factories return a proper RoutedAgent instance,
#   avoiding "Factory registered using wrong type" errors.
# ------------------------------------------------------------

from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import AgentId
from dotenv import load_dotenv
import messages
import importlib
import logging

# Load environment variables if needed
load_dotenv(override=True)

# Configure logging to show info in console
logging.basicConfig(level=logging.INFO, format="%(message)s")

class Creator(RoutedAgent):
    """
    CreatorAgent — orchestrates the spawning and registration of
    all specialized agents (Research, Designer, Engineer, Reviewer, PM).
    """

    system_message = """
    You are the CreatorAgent.
    Your goal is to create and register all specialized agents for
    the AI Startup Studio workflow:
      - ResearchAgent
      - DesignerAgent
      - EngineerAgent
      - ReviewerAgent
      - PMAgent
    """

    def __init__(self, name: str):
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.5)
        self._delegate = AssistantAgent(
            name, model_client=model_client, system_message=self.system_message
        )

    # ------------------------------------------------------------
    # Message handler — called when Creator receives a message.
    # It dynamically loads and registers all agent modules.
    # ------------------------------------------------------------
    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        """Registers all specialized agents with proper factory instances."""
        agents = [
            "agent_research",
            "agent_designer",
            "agent_engineer",
            "agent_reviewer",
            "agent_pm"
        ]

        registered = []
        for agent_name in agents:
            try:
                # Dynamically import each agent module
                module = importlib.import_module(agent_name)

                # Create an instance of the agent class
                instance = module.Agent(agent_name)

                # Define a valid factory (must return the instance directly)
                factory = lambda inst=instance: inst

                # Register with runtime (critical: factory must return RoutedAgent)
                await module.Agent.register(self.runtime, agent_name, factory)

                logging.info(f"✅ Registered {agent_name} ({type(instance).__name__})")
                registered.append(agent_name)
            except Exception as e:
                logging.error(f"❌ Failed to register {agent_name}: {e}")

        # Return message for logging in world.py
        return messages.Message(content=f"Registered agents: {', '.join(registered)}")
