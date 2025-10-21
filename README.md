# Chat IA con Service Layers Pattern

Sistema de chat inteligente que implementa patrones de arquitectura de servicios y RAG (Retrieval-Augmented Generation) usando Django y HuggingFace.

##  Arquitectura

### Patrones Implementados

1. **Service Layers Pattern**: Organización en capas agnósticas y no agnósticas
2. **Functional Decomposition**: Funciones pequeñas con responsabilidad única
3. **Service Encapsulation**: Interfaces claras que ocultan implementación
4. **Canonical Expression**: DTOs estándar para comunicación entre servicios

### Estructura
```
Capa No Agnóstica (Transporte)
    ├── chat_controller.py
    └── Response handling
              ↓
Capa Agnóstica (Lógica de Negocio)
    ├── AIService (HuggingFace + RAG)
    ├── ConversationService
    └── MessageService
              ↓
Capa de Datos
    ├── Conversation Model
    └── Message Model
```

##  Instalación
```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos
python manage.py migrate

# Ejecutar servidor
python manage.py runserver
```

##  Modelos de HuggingFace Utilizados

1. **sentence-transformers/all-MiniLM-L6-v2**: Embeddings para búsqueda semántica
2. **microsoft/DialoGPT-small**: Generación de respuestas conversacionales

##  Pruebas
```bash
# Prueba completa del sistema
python test_system.py

# Acceder a la interfaz web
http://127.0.0.1:8000
```

##  Base de Conocimiento

El sistema aprende de `knowledge_base/custom_texts.txt`. Modifica este archivo para personalizar las respuestas del asistente.

##  Autor

Alberto Josue Santamaria Morales