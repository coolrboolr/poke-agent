from __future__ import annotations

import time
import json
from pathlib import Path
from typing import List

from src.utils.logger import log
from .long_term import LongTermMemory


class WorkingMemory:
    """Manage active objectives and surface relevant facts."""

    def __init__(self, ltm: LongTermMemory, store_path: str | None = None) -> None:
        self.ltm = ltm
        self.path = Path(store_path or "memory_store/objectives.json")
        if self.path.exists():
            self._objectives = json.loads(self.path.read_text())
        else:
            self._objectives = []

    def _save(self) -> None:
        self.path.parent.mkdir(exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self._objectives, f)

    def add_objective(self, desc: str) -> None:
        self._objectives.append({"desc": desc, "timestamp": time.time()})
        self._save()
        log(f"Objective added: {desc}", tag="memory")

    def get_objectives(self) -> List[str]:
        return [o["desc"] for o in self._objectives]

    def complete_objective(self, idx: int) -> None:
        if 0 <= idx < len(self._objectives):
            done = self._objectives.pop(idx)
            self._save()
            log(f"Objective completed: {done['desc']}", tag="memory")

    def top_n_relevant_facts(self, n: int = 5) -> List[str]:
        if not self._objectives:
            return []
        query = " ".join(o["desc"] for o in self._objectives)
        res = self.ltm.collection.query(query_texts=[query], n_results=20)
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        scores = []
        for doc, meta in zip(docs, metas):
            recency = 1.0 / (time.time() - meta.get("timestamp", time.time()) + 1.0)
            overlap = len(set(query.lower().split()) & set(doc.lower().split()))
            score = recency * max(overlap, 1)
            scores.append((score, doc))
        scores.sort(key=lambda x: x[0], reverse=True)
        top_docs = [d for _, d in scores[:n]]
        log(f"Salient facts: {top_docs}", tag="memory")
        return top_docs
