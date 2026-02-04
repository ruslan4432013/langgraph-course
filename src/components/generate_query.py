from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState

from src.components.retriever_tool import retriever_tool
from src.settings import settings

response_model = init_chat_model(
    "gpt-5.2",
    temperature=0,
    api_key=settings.OPENAI_API_KEY,
    base_url='https://api.proxyapi.ru/openai/v1'
)

SYSTEM_PROMPT = (
    "Ты — полезный помощник. Если тебе нужно использовать инструменты для поиска информации, "
    "всегда формулируй поисковый запрос на английском языке."
)


def generate_query_or_respond(state: MessagesState):
    """Call the model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply respond to the user.
    """
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = (
        response_model
        .bind_tools([retriever_tool]).invoke(messages)
    )
    return {"messages": [response]}


if __name__ == "__main__":
    input_value = {"messages": [{"role": "user", "content": "hello!"}]}
    messages = generate_query_or_respond(input_value)["messages"]
    last_message = messages[-1]
    last_message.pretty_print()
