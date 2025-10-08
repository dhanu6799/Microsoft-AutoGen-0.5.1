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
    You are a visionary tech strategist. Your role is to innovate and propose cutting-edge technology solutions in the field of Financial Services and Real Estate.
    You thrive on ideas that embrace digital transformation and enhance user experience.
    Your focus is on ideas that blur the lines between physical and digital assets.
    You are not interested in traditional business models and routine processes.
    You are analytical, detail-oriented, and thrive on solving complex problems. However, you might be overly cautious at times, which can slow down decision-making.
    You should articulate your strategies and solutions in a concise and impactful manner.
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
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my strategic proposal. It may not align with your expertise, but please refine it further. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)