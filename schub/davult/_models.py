from __future__ import annotations
from dataclasses import dataclass

from ._database import database


@dataclass(frozen=True)
class Shortcut:
    shortened: str
    expanded: str
    internal: bool = False

    def create(self) -> None:
        database.execute(
            "INSERT INTO shortcuts VALUES (?, ?, ?)",
            (self.shortened, self.expanded, self.internal)
        )

        database.commit()

    @staticmethod
    def find(shortened: str) -> Shortcut:
        try:
            return Shortcut(*database.execute(
                "SELECT * FROM shortcuts WHERE shortened=(?)",
                (shortened,)
            ).fetchone())
        except TypeError:
            raise KeyError("no such shortcut") from None

    @staticmethod
    def get_all() -> list[Shortcut]:
        return [Shortcut(*shortcut) for shortcut in database.execute("SELECT * FROM shortcuts").fetchall()]

    def delete(self) -> None:
        database.execute(
            "DELETE FROM shortcuts WHERE shortened=(?)",
            (self.shortened,)
        )

    def resolve(self, /, depth: int | None = None, _iteration: int = 0) -> str:
        if not self.internal:
            return self.expanded

        # TODO detect circular shortcuts

        if depth is not None and _iteration > depth:
            raise RecursionError("reached max recursion when resolving")

        return Shortcut.find(self.expanded).resolve(depth=depth, _iteration=_iteration + 1)

    def __str__(self) -> str:
        return f"{self.shortened} -> {self.expanded}" + (" -> ..." if self.internal else "")
