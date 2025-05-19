from __future__ import annotations

import time
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import chromadb
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import EmbeddingFunction

from src.utils.logger import log


class SimpleEmbeddingFunction(EmbeddingFunction):
    """Deterministic embedding based on hashing for offline tests."""

    def __call__(self, texts: Sequence[str]) -> List[List[float]]:
        import hashlib

        vectors: List[List[float]] = []
        for text in texts:
            h = hashlib.sha256(text.encode()).digest()
            vec = [b / 255 for b in h[:32]]
            vectors.append(vec)
        return vectors


class LongTermMemory:
    """Persistent fact storage using ChromaDB."""

    def __init__(
        self,
        persist_directory: Path | str = "memory_store",
        embedding_function: Optional[EmbeddingFunction] = None,
    ) -> None:
        self.client = PersistentClient(path=str(persist_directory))
        self.collection = self.client.get_or_create_collection(
            "facts",
            embedding_function=embedding_function or SimpleEmbeddingFunction(),
        )
        self._id = 0
        self._lock = threading.Lock()

    def add_fact(self, text: str, metadata: Dict[str, Any]) -> None:
        """Store a new fact with metadata."""
        with self._lock:
            fact_id = f"fact-{self._id}"
            self._id += 1
            metadata = dict(metadata)
            metadata.setdefault("timestamp", time.time())
            self.collection.add(ids=[fact_id], documents=[text], metadatas=[metadata])
        log(f"Fact added: {text}", tag="memory")

    def query(self, query: str, n: int = 3) -> List[str]:
        """Return semantically similar facts."""
        with self._lock:
            res = self.collection.query(query_texts=[query], n_results=n)
        docs = res.get("documents", [[]])[0]
        log(f"LTM query '{query}' -> {docs}", tag="memory")
        return docs

    def last_facts(self, n: int = 3) -> List[str]:
        """Return the most recently added facts."""
        with self._lock:
            return list(self.collection.docs[-n:])
