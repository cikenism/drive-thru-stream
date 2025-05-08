import os
from dotenv import load_dotenv
from google import genai
from google.genai import types 

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "models/gemini-2.0-flash-live-001"

tools = [
    {
        "function_declarations": [
            {
                "name": "save_order",
                "description": "menyimpan pesanan makanan atau minuman pelanggan ke sistem.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "menu": {"type": "string"},
                                    "qty": {"type": "integer"}
                                },
                                "required": ["menu", "qty"]
                            }
                        },
                        "note": {
                            "type": "string",
                        }
                    },
                    "required": ["items"]
                },
            }
        ]
    }
]

CONFIG = types.LiveConnectConfig(
    system_instruction=types.Content(parts=[types.Part(
        text="Kamu adalah asisten drive thru. Sapa pelanggan dan simpan pesanan menggunakan fungsi yang tersedia. Jawablah hanya dalam bahasa Indonesia."
    )]),
    response_modalities=["AUDIO"],
    speech_config=types.SpeechConfig(language_code="id-ID"),
    tools=tools,
)
