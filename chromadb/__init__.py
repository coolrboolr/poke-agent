from typing import Any, Dict, List, Sequence

class Collection:
    def __init__(self, embedding_function=None):
        self.embedding_function = embedding_function
        self.docs: List[str] = []
        self.metas: List[Dict[str, Any]] = []
        self.ids: List[str] = []

    def add(self, ids: List[str], documents: List[str], metadatas: List[Dict[str, Any]]) -> None:
        for i, doc, meta in zip(ids, documents, metadatas):
            self.ids.append(i)
            self.docs.append(doc)
            self.metas.append(meta)

    def query(self, query_texts: Sequence[str], n_results: int = 3):
        query = query_texts[0].lower()
        scored = []
        for doc, meta in zip(self.docs, self.metas):
            score = sum(word in doc.lower() for word in query.split())
            scored.append((score, doc, meta))
        scored.sort(key=lambda x: x[0], reverse=True)
        docs = [s[1] for s in scored[:n_results]]
        metas = [s[2] for s in scored[:n_results]]
        return {"documents": [docs], "metadatas": [metas]}

class PersistentClient:
    def __init__(self, path: str = "memory_store") -> None:
        self.collections: Dict[str, Collection] = {}

    def get_or_create_collection(self, name: str, embedding_function=None) -> Collection:
        if name not in self.collections:
            self.collections[name] = Collection(embedding_function)
        return self.collections[name]
