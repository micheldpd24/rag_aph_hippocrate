from pydantic import BaseModel
from typing import List, Optional

class AppConfig(BaseModel):
    name: str
    debug: bool
    host: str
    port: int
    secret_key: str
    data_dir: str
    cache_dir: str
    question_cache_file: str

class ModelConfig(BaseModel):
    name: str
    normalize_embeddings: bool

class IndexConfig(BaseModel):
    json_path: str
    faiss_path: str
    build_on_startup: bool
    top_k: int

class LLMConfig(BaseModel):
    provider: str
    endpoint: str
    model: str

class RAGConfig(BaseModel):
    model: ModelConfig
    index: IndexConfig
    llm: LLMConfig

class SecurityConfig(BaseModel):
    allowed_tags: List[str]

class GlobalConfig(BaseModel):
    app: AppConfig
    rag: RAGConfig
    security: SecurityConfig
