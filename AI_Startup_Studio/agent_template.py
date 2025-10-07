# agent_template.py
# ------------------------------------------------------------
# Base agent class for all specialized AI roles
# Fixes: 'AgentId not defined' and '_id missing' errors
# ------------------------------------------------------------

from autogen_core import MessageContext, RoutedAgent, AgentId, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages

class Agent(RoutedAgent):
    """Generic AI Agent that can process messages and respond intelligently."""

    system_message = """
    You are a general-purpose creative AI agent.
    Your task is to receive a prompt, analyze it, and respond thoughtfully.
    """

    def __init__(self, name: str):
        # ✅ Properly initialize the base RoutedAgent class
        super().__init__(name)

        # ✅ Assign AgentId — required for routing in gRPC runtime
        self._id = AgentId(name, "default")

        # ✅ Configure model client and delegate
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        self._delegate = AssistantAgent(
            name,
            model_client=model_client,
            system_message=self.system_message,
        )

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        """Handles incoming messages using the AssistantAgent delegate."""
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        return messages.Message(content=response.chat_message.content)
