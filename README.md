# Chat IA con Service Layers Pattern

Sistema de chat inteligente que implementa patrones de arquitectura de servicios y RAG (Retrieval-Augmented Generation) usando Django y HuggingFace.

# Patrones Implementados

1. **Service Layers Pattern**: Organización en capas agnósticas y no agnósticas
2. **Functional Decomposition**: Funciones pequeñas con responsabilidad única
3. **Service Encapsulation**: Interfaces claras que ocultan implementación
4. **Canonical Expression**: DTOs estándar para comunicación entre servicios

##  Instalación
```bash
# Crear entorno virtual
python -m venv venv

# Activar
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos
python manage.py migrate

# Ejecutar servidor
python manage.py runserver

# Acceder a la interfaz web
http://127.0.0.1:8000
```

##  Modelos de HuggingFace Utilizados

1. **sentence-transformers/all-MiniLM-L6-v2**: Embeddings para búsqueda semántica
2. **microsoft/DialoGPT-small**: Generación de respuestas conversacionales
