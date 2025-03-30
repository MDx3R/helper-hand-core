from dataclasses import dataclass

from domain.dto.input.registration import UserResetDTO
from domain.dto.common import UserDTO

@dataclass
class UserResetTestCase:
    input: UserResetDTO
    expected: UserDTO