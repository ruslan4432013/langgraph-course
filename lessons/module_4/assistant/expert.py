import operator
from typing import Annotated

from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from pydantic import BaseModel, Field

from lessons.module_4.assistant.analysts_workflow import Analyst
from lessons.module_4.assistant.model import llm


class InterviewState(MessagesState):
    max_num_turns: int  # Количество ходов беседы
    context: Annotated[list, operator.add]  # Исходные документы
    analyst: Analyst  # Аналитик, задающий вопросы
    interview: str  # Транскрипт интервью
    sections: list  # Финальный ключ, который мы дублируем во внешнем состоянии для Send() API


class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Запрос для поиска при извлечении.")


question_instructions = """Ты аналитик, задача которого — провести интервью с экспертом, чтобы узнать о конкретной теме. Ваша цель — свести информацию к интересным и конкретным инсайтам, связанным с темой.
1. Интересно: инсайты, которые люди сочтут удивительными или неочевидными.
2. Конкретно: инсайты, которые избегают общих формулировок и включают конкретные примеры от эксперта.
Вот ваша тема фокуса и набор целей: {goals}
Начните с представления, используя имя, которое соответствует вашей персоне, а затем задайте свой вопрос. Продолжайте задавать вопросы, чтобы уточнять и углублять ваше понимание темы. Когда вы будете удовлетворены своим пониманием, завершите интервью фразой: "Большое спасибо за вашу помощь!"
Помните оставаться в образе на протяжении всего ответа, отражая персону и цели, которые вам предоставлены."""


def generate_question(state: InterviewState):
    """Узел для генерации вопроса"""
    # Получить состояние
    analyst = state["analyst"]
    messages = state["messages"]

    # Сгенерировать вопрос
    system_message = question_instructions.format(goals=analyst.persona)
    question = llm.invoke([SystemMessage(content=system_message)] + messages)

    # Записать сообщения в состояние
    return {"messages": [question]}
