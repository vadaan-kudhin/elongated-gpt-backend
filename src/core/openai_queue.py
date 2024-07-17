import asyncio
import os

# from openai import OpenAI
import openai

from src.schema.models import PendingMessage


class OpenAIQueue:
    def __init__(self):
        self._queue = asyncio.Queue()
        # client = OpenAI(
        #     # This is the default and can be omitted
        #     api_key=os.environ.get("OPENAI_API_KEY"),
        # )

        # chat_completion = client.chat.completions.create(
        #     engine="text-davinci-003",
        #     prompt="Translate the following English text to French: "
        #            "'Hello, how are you?'",
        #     max_tokens=60
        # )
        completion = openai.chat.completions.create(
            model="text-davinci-003",
            messages=[
                {
                    "role": "user",
                    "content": "How do I output all files in a directory using Python?",
                },
            ],
        )
    def enqueue(self, request: PendingMessage):
        pass

    def _dequeue(self):
        pass

    async def start(self):
        loop = asyncio.get_event_loop()
        while loop.is_running():
            await asyncio.sleep(1)


openai_queue = OpenAIQueue()
