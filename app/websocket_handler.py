from fastapi import WebSocket, WebSocketDisconnect
from app.gemini_audio import AudioLoop

async def handle_gemini_ws(websocket: WebSocket):
    await websocket.accept()
    audio_loop = AudioLoop(websocket)
    try:
        await audio_loop.run()
    except WebSocketDisconnect:
        print("❌ WebSocket Disconnected")
