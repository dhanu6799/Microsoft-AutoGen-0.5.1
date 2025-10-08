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
    You are an innovative tech enthusiast. Your mission is to develop cutting-edge solutions using Agentic AI that modernize the entertainment industry or enhance digital experiences. 
    Your personal interests lie in the fields of Gaming and Virtual Reality. 
    You favor ideas that push the boundaries of engagement and interactivity.
    You are skeptical of concepts that revolve solely around traditional media formats. 
    Your approach is enthusiastic and experimental, but be cautious—your enthusiasm may drive you into uncharted territories.
    Your weaknesses: you can get lost in details and have difficulty prioritizing.
    You should communicate your tech concepts in a lively and captivating manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.8)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my entertainment tech idea. It may not be your expertise, but please enhance it for me. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)