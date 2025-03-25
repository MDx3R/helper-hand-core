from typing import TypeVar
from dataclasses import dataclass

from domain.dto.input.registration import UserRegistrationDTO
from domain.dto.common import UserDTO

@dataclass
class UserRegistrationTestCase:
    input: UserRegistrationDTO
    expected: UserDTO
