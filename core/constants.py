from enum import Enum
from functools import lru_cache


class JobType(Enum):
    FULL_TIME = "ft"
    PART_TIME = "pt"

    @classmethod
    @lru_cache(maxsize=1)
    def values(cls) -> list[str]:
        return [el.value for el in cls]
