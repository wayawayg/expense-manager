from dataclasses import dataclass


@dataclass(eq=False, frozen=True, slots=True)
class BaseException(Exception):
    @property
    def message(self) -> str:
        return "There was an error in the program"
