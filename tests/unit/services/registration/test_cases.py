from typing import TypeVar
from dataclasses import dataclass

from domain.dto.input.registration import UserRegistrationDTO, UserResetDTO
from domain.dto.context import UserContextDTO
from domain.dto.common import UserDTO

@dataclass
class UserRegistrationTestCase:
    input: UserRegistrationDTO
    expected: UserDTO

@dataclass
class UserResetTestCase:
    input: UserResetDTO
    context: UserContextDTO
    expected: UserDTO