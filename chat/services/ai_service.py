from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import torch
from typing import List
import os

class AIService:
    """Servicio que usa HuggingFace para RAG"""
    
    def __init__(self, knowledge_base_path: str = None):
        print("🚀 Inicializando AIService con HuggingFace...\n")
        
        # Modelo de embeddings
        print("📦 Cargando modelo de embeddings...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("   ✅ Modelo de embeddings cargado\n")
        
        # Modelo generativo
        print("🤖 Cargando modelo generativo...")
        model_name = "microsoft/DialoGPT-small"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        print("   ✅ Modelo generativo cargado\n")
        
        # Base de conocimiento
        self.knowledge_chunks = []
        self.index = None
        
        if knowledge_base_path:
            self.load_knowledge_base(knowledge_base_path)
        
        print("✅ AIService listo\n")
    
    def load_knowledge_base(self, file_path: str):
        """Carga y indexa la base de conocimiento"""
        print(f"📚 Cargando base de conocimiento: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"⚠️  Archivo no encontrado: {file_path}\n")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            chunks = self._split_into_chunks(text, chunk_size=200)
            self.knowledge_chunks = chunks
            print(f"   ✅ {len(chunks)} fragmentos creados")
            
            print("🔢 Creando embeddings...")
            embeddings = self.embedding_model.encode(chunks, show_progress_bar=True)
            
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(np.array(embeddings).astype('float32'))
            
            print(f"   ✅ Índice creado con {self.index.ntotal} vectores\n")
            
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    def _split_into_chunks(self, text: str, chunk_size: int = 200) -> List[str]:
        """Divide texto en chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    def _retrieve_relevant_chunks(self, query: str, top_k: int = 3) -> List[str]:
        """Búsqueda semántica con FAISS"""
        if self.index is None or len(self.knowledge_chunks) == 0:
            return []
        
        query_embedding = self.embedding_model.encode([query])
        k = min(top_k, len(self.knowledge_chunks))
        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'), 
            k
        )
        
        return [self.knowledge_chunks[idx] for idx in indices[0]]
    
    def generate_response(self, user_message: str, conversation_history: List[str] = None) -> str:
        """Genera respuesta usando RAG"""
        print(f"💬 Generando respuesta para: '{user_message}'")
        
        # Retrieve
        relevant_info = self._retrieve_relevant_chunks(user_message, top_k=2)
        
        context = ""
        if relevant_info:
            context = "Información relevante:\n" + "\n".join(relevant_info) + "\n\n"
        
        # Augment
        if conversation_history:
            history_text = "\n".join(conversation_history[-6:])
            prompt = f"{history_text}\n{context}Usuario: {user_message}\nAsistente:"
        else:
            prompt = f"{context}Usuario: {user_message}\nAsistente:"
        
        # Generate
        inputs = self.tokenizer.encode(prompt, return_tensors='pt', truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=inputs.shape[1] + 50,
                num_return_sequences=1,
                no_repeat_ngram_size=3,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if "Asistente:" in response:
            response = response.split("Asistente:")[-1].strip()
        
        response = response.strip()
        if not response:
            response = "Lo siento, no pude generar una respuesta."
        
        print(f"   ✅ Respuesta: '{response[:100]}...'\n")
        return response