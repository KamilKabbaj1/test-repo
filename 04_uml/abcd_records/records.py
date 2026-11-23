"""Daily records file (rule 8): every processed order is saved."""

from pathlib import Path

from .order import Order


class DailyRecords:
    """Appends one line per order to a text file.

    The file path is given to the constructor (dependency injection) instead of
    being hard-coded. WHY: tests can use a temporary file, and the real
    application chooses where the file lives (Dependency Inversion principle).
    """

    SEPARATOR = ";"

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    def save(self, order: Order) -> None:
        fields = [
            order.date.isoformat(),
            order.order_id,
            order.member.member_id,
            f"{order.total:.2f}",
            order.status.value,
        ]
        # Mode "a" (append): earlier orders of the day are never overwritten.
        with self.path.open("a", encoding="utf-8") as file:
            file.write(self.SEPARATOR.join(fields) + "\n")

    def entries(self) -> list[list[str]]:
        if not self.path.exists():
            return []
        text = self.path.read_text(encoding="utf-8")
        return [line.split(self.SEPARATOR) for line in text.splitlines()]
