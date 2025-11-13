import time
from typing import Optional, Any
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI
from tenacity import RetryCallState


class CustomCallback(BaseCallbackHandler):
    def __init__(self, pre_gen_time_ref, start_time_ref, end_time_ref):
        self.pre_gen_time_ref = pre_gen_time_ref
        self.start_time_ref = start_time_ref
        self.end_time_ref = end_time_ref

    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f'LLM start: {serialized}, prompts: {prompts}')

    def on_llm_new_token(self, token: str, **kwargs):
        # Первый токен: фиксируем момент начала генерации и выводим метрики
        if self.start_time_ref["value"] is None:
            first_token_time = time.time()
            self.start_time_ref["value"] = first_token_time
            print(f"Началась генерация: {first_token_time}")
            print(f"Время до начала генерации: {(first_token_time - self.pre_gen_time_ref['value']):.3f} сек")
        print(token, end='')

    def on_llm_end(self, response, **kwargs):
        self.end_time_ref["value"] = time.time()
        print(f'\nLLM end: {response}')

    def on_llm_error(self, error, **kwargs):
        # Фиксируем конец в случае ошибки (если еще не зафиксирован)
        print(error)
        if self.end_time_ref["value"] is None:
            self.end_time_ref["value"] = time.time()
        # Само сообщение об ошибке и метрика "время до исключения" будут напечатаны вне callback, в except

    def on_retry(
            self,
            retry_state: RetryCallState,
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        print(f"Retrying LLM call for run {retry_state}...")


start_time_ref = {"value": None}
end_time_ref = {"value": None}
pre_gen_time_ref = {"value": time.time()}

callback = CustomCallback(pre_gen_time_ref, start_time_ref, end_time_ref)

llm = ChatOpenAI(
    model='gpt-5',
    timeout=2,
    streaming=True,
    max_retries=3,
    callbacks=[callback]
)

whole_start = time.time()

# замер до начала генерации (до получения первого токена)
try_start_time = time.time()  # замер от начала try

# ... existing code ...


try:
    message = llm.invoke("Что ты знаешь про langgraph?")
    print(message)
except Exception as e:
    elapsed_try = time.time() - try_start_time
    print(f'\nВремя до исключения: {elapsed_try:.3f} сек')
    print('Error: ', e)

end_time = end_time_ref["value"] if end_time_ref["value"] is not None else time.time()
start_time = start_time_ref["value"]
if start_time is None:
    # Если исключение произошло до получения первого токена,
    # считаем длительность от начала try до конца обработки
    start_time = try_start_time

print(f'\nWhole time taken = {time.time() - whole_start:.3f} seconds')
print(f"\nTime taken for generation: {(end_time - start_time):.3f} seconds")
