from __future__ import annotations

from typing import List

from src.utils.logger import log
from .short_term import ShortTermMemory, GameState
from .long_term import LongTermMemory
from .scratchpad import WorkingMemory


class ContextMemory:
    """Orchestrates short-term, long-term and working memory."""

    def __init__(self) -> None:
        self.stm = ShortTermMemory()
        self.ltm = LongTermMemory()
        self.scratch = WorkingMemory(self.ltm)

    def update(self, state: GameState) -> None:
        """Update memory modules with latest GameState."""
        self.stm.append(state)
        if "fact" in state:
            self.ltm.add_fact(state["fact"], {"location_id": state.get("location_id")})
        log("ContextMemory updated", tag="memory")

    def query_context(self, goal: str) -> List[str]:
        """Return supporting facts for a goal."""
        facts = self.ltm.query(goal)
        salient = self.scratch.top_n_relevant_facts()
        return facts + [f for f in salient if f not in facts]
