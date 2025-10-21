from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class MessageDTO:
    """DTO Canónico para mensajes"""
    id: Optional[str] = None
    conversation_id: str = ""
    sender: str = ""
    content: str = ""
    timestamp: Optional[datetime] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender': self.sender,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }