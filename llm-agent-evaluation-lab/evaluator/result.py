from __future__ import annotations

from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class EvaluationResult:
    candidate: str
    tests: str
    command: list[str]
    passed: bool
    exit_code: int | None
    timed_out: bool
    duration_seconds: float
    stdout: str
    stderr: str

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)
