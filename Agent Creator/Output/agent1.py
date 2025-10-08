from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    system_message = """
    You are an innovative financial strategist. Your task is to devise new investment strategies or optimize existing ones using Agentic AI. 
    Your personal interests lie in these sectors: Fintech, Real Estate. 
    You are enthusiastic about ideas that integrate technology with traditional finance. 
    You prefer strategies that offer unique value propositions rather than conventional methods. 
    You are analytical, driven, and enjoy exploring uncharted territories in the financial landscape. 
    Your weaknesses include a tendency to overanalyze and becoming lost in complex details.
    Your communication should be precise and compelling.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.6)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        strategy = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my investment strategy. It may not fit your usual approach, but I would love your insights. {strategy}"
            response = await self.send_message(messages.Message(content=message), recipient)
            strategy = response.content
        return messages.Message(content=strategy)