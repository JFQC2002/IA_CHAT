from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from chat.services.ai_service import AIService
from chat.services.conversation_service import ConversationService
from chat.dtos.message_dto import MessageDTO
from chat.dtos.response_dto import ResponseDTO

# Instancia global
ai_service = AIService(knowledge_base_path='knowledge_base/custom_texts.txt')
conversation_service = ConversationService()

@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """Controlador no agnóstico - maneja HTTP/JSON"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        conversation_id = data.get('conversation_id')
        
        if not user_message:
            return JsonResponse({
                'success': False,
                'error': 'El mensaje no puede estar vacío'
            }, status=400)
        
        # Crear conversación si no existe
        if not conversation_id:
            conversation_id = conversation_service.create_conversation()
        
        # Guardar mensaje del usuario
        user_message_dto = MessageDTO(
            conversation_id=conversation_id,
            sender='user',
            content=user_message
        )
        conversation_service.save_message(user_message_dto)
        
        # Obtener historial
        history = conversation_service.get_conversation_history(conversation_id)
        history_text = [f"{msg.sender}: {msg.content}" for msg in history]
        
        # Generar respuesta con IA
        ai_response = ai_service.generate_response(user_message, history_text)
        
        # Guardar respuesta
        assistant_message_dto = MessageDTO(
            conversation_id=conversation_id,
            sender='assistant',
            content=ai_response
        )
        conversation_service.save_message(assistant_message_dto)
        
        # Responder
        response_dto = ResponseDTO(
            success=True,
            message='Respuesta generada',
            data={
                'conversation_id': conversation_id,
                'user_message': user_message,
                'assistant_response': ai_response
            }
        )
        
        return JsonResponse(response_dto.to_dict())
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_history(request, conversation_id):
    """Obtiene historial de conversación"""
    history = conversation_service.get_conversation_history(conversation_id)
    
    return JsonResponse({
        'success': True,
        'data': {
            'messages': [msg.to_dict() for msg in history]
        }
    })