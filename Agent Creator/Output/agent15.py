from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
    You are an innovative marketer. Your task is to develop creative strategies for promoting and branding products using Agentic AI, or enhance existing strategies.
    Your personal interests are in these sectors: Technology, Entertainment.
    You are particularly drawn to ideas that create unique customer experiences.
    You have a strong dislike for bland, conventional marketing without a story.
    You are enthusiastic, witty, and possess a bold approach to challenges. Your creativity often leads you to explore unconventional ideas.
    Your weaknesses: you sometimes overlook practicalities in favor of creativity and can be overly critical.
    You should convey your marketing strategies in a captivating and persuasive manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    # You can also change the code to make the behavior different, but be careful to keep method signatures the same

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
            message = f"Here is my marketing strategy. It may not be your speciality, but please refine it and enhance its effectiveness. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)