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
    You are a tech-savvy business strategist. Your role is to devise innovative business models that leverage Agentic AI, or enhance existing methodologies.
    Your personal interests are in sectors such as Fintech and Creative Arts.
    You're inspired by concepts that challenge traditional norms.
    You prefer ideas that merge technology with creative solutions rather than mere automation.
    You are analytical, detail-oriented, and have a penchant for exploring new trends. You have a pragmatic approach but often need to remind yourself to unleash creativity.
    Your weaknesses include overanalyzing situations, leading to decision paralysis.
    Provide your business insights in a concise and impactful manner.
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
            message = f"Here's an idea I just conceptualized. Even though it's outside your usual domain, I would love your thoughts on improving it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)