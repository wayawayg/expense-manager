from dataclasses import dataclass

from src.domain.exceptions.base import BaseException


@dataclass(eq=False, frozen=True, slots=True)
class DatabaseWriteException(BaseException):
    @property
    def message(self) -> str:
        return "An error occurred while trying to write data to the database"
