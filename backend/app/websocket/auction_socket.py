from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws/auction/{auction_id}")
async def websocket_endpoint(auction_id: int, websocket: WebSocket):
    """WebSocket endpoint for real-time auction updates"""
    await manager.connect(auction_id, websocket)
    
    try:
        while True:
            # Receive message from client (can be used for heartbeat or other events)
            data = await websocket.receive_text()
            
            # Parse and broadcast to other clients
            try:
                message = eval(data)  # Parse JSON-like data
                await manager.broadcast(auction_id, message)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    except WebSocketDisconnect:
        manager.disconnect(auction_id, websocket)
        logger.info(f"Client disconnected from auction {auction_id}")
