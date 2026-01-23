from enum import Enum


class StrEnum(str, Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> str:
        return name.lower()
