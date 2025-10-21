from chat.models import Conversation, Message
from chat.dtos.message_dto import MessageDTO
from typing import List

class ConversationService:
    """Servicio agnóstico para gestionar conversaciones"""
    
    def create_conversation(self) -> str:
        """Crea una nueva conversación"""
        conversation = Conversation.objects.create()
        return str(conversation.id)
    
    def get_conversation_history(self, conversation_id: str) -> List[MessageDTO]:
        """Obtiene el historial de mensajes"""
        try:
            messages = Message.objects.filter(
                conversation_id=conversation_id
            ).order_by('timestamp')
            
            return [
                MessageDTO(
                    id=str(msg.id),
                    conversation_id=str(msg.conversation_id),
                    sender=msg.sender,
                    content=msg.content,
                    timestamp=msg.timestamp
                )
                for msg in messages
            ]
        except Conversation.DoesNotExist:
            return []
    
    def save_message(self, message_dto: MessageDTO) -> MessageDTO:
        """Guarda un mensaje"""
        message = Message.objects.create(
            conversation_id=message_dto.conversation_id,
            sender=message_dto.sender,
            content=message_dto.content
        )
        
        message_dto.id = str(message.id)
        message_dto.timestamp = message.timestamp
        
        return message_dto