from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.websocket_handler import handle_gemini_ws

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti sesuai kebutuhan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/audio")
async def audio_endpoint(websocket: WebSocket):
    await handle_gemini_ws(websocket)
