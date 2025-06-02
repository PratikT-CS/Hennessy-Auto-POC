from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect
 
router = APIRouter(prefix="/ws")
 
connections = {}
 
@router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()  # 👈 REQUIRED
    connections[client_id] = websocket
    try:
        await websocket.send_json({
            "message": f"Upload documents to process them.", 
            "processing_started": False,
            "processing_details": {},
            "client_id": client_id
        })
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")