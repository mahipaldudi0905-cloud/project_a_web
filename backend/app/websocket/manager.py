from typing import Dict, Set
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage WebSocket connections for real-time auction updates"""
    
    def __init__(self):
        self.active_connections: Dict[int, Set[WebSocket]] = {}
    
    async def connect(self, auction_id: int, websocket: WebSocket):
        """Accept and register a new WebSocket connection"""
        await websocket.accept()
        
        if auction_id not in self.active_connections:
            self.active_connections[auction_id] = set()
        
        self.active_connections[auction_id].add(websocket)
        logger.info(f"Client connected to auction {auction_id}")
    
    def disconnect(self, auction_id: int, websocket: WebSocket):
        """Remove a disconnected client"""
        if auction_id in self.active_connections:
            self.active_connections[auction_id].discard(websocket)
            
            if not self.active_connections[auction_id]:
                del self.active_connections[auction_id]
        
        logger.info(f"Client disconnected from auction {auction_id}")
    
    async def broadcast(self, auction_id: int, message: dict):
        """Broadcast message to all clients in an auction"""
        if auction_id in self.active_connections:
            for connection in self.active_connections[auction_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message: {e}")
    
    async def broadcast_bid(
        self,
        auction_id: int,
        player_id: int,
        amount: float,
        team_name: str
    ):
        """Broadcast a new bid"""
        message = {
            "event": "new_bid",
            "player_id": player_id,
            "amount": amount,
            "team_name": team_name
        }
        await self.broadcast(auction_id, message)
    
    async def broadcast_auction_started(self, auction_id: int, auction_title: str):
        """Broadcast auction started event"""
        message = {
            "event": "auction_started",
            "auction_id": auction_id,
            "title": auction_title
        }
        await self.broadcast(auction_id, message)
    
    async def broadcast_auction_closed(self, auction_id: int):
        """Broadcast auction closed event"""
        message = {
            "event": "auction_closed",
            "auction_id": auction_id
        }
        await self.broadcast(auction_id, message)


# Global connection manager instance
manager = ConnectionManager()
