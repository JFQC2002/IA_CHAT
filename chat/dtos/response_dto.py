from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ResponseDTO:
    """DTO Canónico para respuestas"""
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    
    def to_dict(self):
        return {
            'success': self.success,
            'message': self.message,
            'data': self.data,
            'error': self.error
        }