from typing import TypeVar
from dataclasses import dataclass

from domain.dto.input import UserInputDTO
from domain.dto.common import UserDTO

@dataclass
class UserRegistrationTestCase:
    input: UserInputDTO
    expected: UserDTO
