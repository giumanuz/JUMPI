from openai import OpenAI
from openai.types import ChatModel
from openai.types.chat.chat_completion import ChatCompletion

import app.config as config


class _OpenaiClient:
    def __init__(self):
        self._client = OpenAI(api_key=config.APP_CONFIG.OPENAI_API_KEY)


class OpenaiClient(_OpenaiClient):
    def __init__(self,
                 system_prompt: str,
                 max_tokens: int,
                 temperature: float,
                 model: ChatModel):
        super().__init__()
        self.__system_prompt = system_prompt
        self.__max_tokens = max_tokens
        self.__temperature = temperature
        self.__model = model

    def get_completion(self, user_messages: str | list[str]) -> str:
        user_messages = self.__get_user_messages_as_list(user_messages)
        response = self.__get_response(user_messages)
        return _get_content_from_response(response)

    @staticmethod
    def __get_user_messages_as_list(user_messages: str | list[str]) -> list[str]:
        if isinstance(user_messages, str):
            return [user_messages]
        return user_messages

    def __get_response(self, user_messages) -> ChatCompletion:
        encoded_user_messages = _get_encoded_user_messages(user_messages)
        return self._client.chat.completions.create(
            model=self.__model,
            messages=[
                {"role": "system", "content": self.__system_prompt},
                *encoded_user_messages
            ],
            max_tokens=self.__max_tokens,
            temperature=self.__temperature
        )


def _get_content_from_response(response: ChatCompletion) -> str:
    return response.choices[0].message.content


def _get_encoded_user_messages(user_messages: list[str]):
    return [
        {"role": "user", "content": message}
        for message in user_messages
    ]
