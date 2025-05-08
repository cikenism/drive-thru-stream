import asyncio
import pyaudio
import traceback
import os
from google import genai
from app.config import *
from app.utils import save_order
from google.genai import types

pya = pyaudio.PyAudio()
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class AudioLoop:
    def __init__(self, websocket):
        self.websocket = websocket
        self.session = None
        self.audio_in_queue = asyncio.Queue()
        self.out_queue = asyncio.Queue(maxsize=5)

    async def send_realtime(self):
        while True:
            data = await self.websocket.receive_bytes()
            await self.session.send(input={"data": data, "mime_type": "audio/pcm"})

    async def receive_audio(self):
        while True:
            turn = self.session.receive()
            async for response in turn:
                if response.text:
                    await self.websocket.send_text(response.text)
                if response.data:
                    await self.websocket.send_bytes(response.data)
                if response.tool_call:
                    function_responses = []
                    for fc in response.tool_call.function_calls:
                        if fc.name == "save_order":
                            result = save_order(fc.args.get("items", []))
                            function_responses.append(
                                types.FunctionResponse(id=fc.id, name=fc.name, response=result)
                            )
                    await self.session.send_tool_response(function_responses=function_responses)

    async def run(self):
        try:
            async with client.aio.live.connect(model=MODEL, config=CONFIG) as session:
                self.session = session
                tasks = [
                    asyncio.create_task(self.send_realtime()),
                    asyncio.create_task(self.receive_audio())
                ]
                await asyncio.gather(*tasks)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
