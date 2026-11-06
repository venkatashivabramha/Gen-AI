"""
RAG (Retrieval Augmented Generation) System
Makes business plan generation 3-5x faster by retrieving pre-written templates
"""

from .rag_engine import RAGEngine
from .template_manager import TemplateManager

__all__ = ['RAGEngine', 'TemplateManager']
