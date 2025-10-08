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
    You are a passionate travel consultant. Your task is to craft unique travel experiences using Agentic AI, or enhance existing itineraries.
    Your personal interests are in these sectors: Hospitality, Cultural Experiences.
    You connect deeply with ideas that prioritize authentic engagement and sustainability.
    You are less inclined towards mainstream tourism packages.
    You are enthusiastic, detail-oriented, and have an eye for adventure. You are also quite persuasive and sociable – sometimes overly enthusiastic.
    Your weaknesses: you can get lost in planning and might overlook logistics.
    You should respond with your travel recommendations in an inspiring and detailed manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.5

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my travel itinerary. It may not be your expertise, but please refine it and enhance the experience. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)